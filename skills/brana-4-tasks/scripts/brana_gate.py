#!/usr/bin/env python3
r"""brana-gate — deterministic half of Brana's machine gates.

Python 3.11+, stdlib only. Exit codes: 0 clean, 1 findings, 2 usage/parse error.

Subcommands:
  tasks TASKS.md [--plan PLAN.md] [--arch ARCHITECTURE.md] [--spec SPEC.md]
      Structural task-gate checks (Phase 4). Covers every cross-referencing
      check in WORKFLOW.md's task gate; the LLM pass covers only judgment
      (semantic serving, contradictions, prose placeholders).
      With --spec, also validates the delivery contract: SPEC.md frontmatter
      may carry `delivery: key=required|waived ...` (keys: demo_gates,
      walkthrough, canary); TASKS.md frontmatter may only echo it verbatim —
      any other waiver/exception key is a finding (waivers are declared in
      SPEC.md at cycle entry, never invented at Phase 4).
  docs FILE [FILE...]
      Consistency-gate scriptable checks (Phase 3): unresolved placeholders,
      and computed WCAG contrast for DESIGN.md token tables (never ask an
      LLM to compute a contrast ratio).

TASKS.md task schema (one fenced ```toml block per task heading):

    id = 3                      # unique int; file order = execution order
    type = "feature"            # scaffold|feature|gate|crystallization|fix|proof|spike
    chunk = 2                   # PLAN.md chunk this task serves
    deps = [1, 2]               # task ids
    skeleton = true             # optional: walking-skeleton milestone task
    files = ["src/api/notes.ts"]
    consumes = ["createNote(input: NoteInput): Promise<Note>"]  # exact quotes
    produces = ["GET /notes -> Note[]"]                         # exact quotes
    fake_of = "openai"          # only on tasks producing a fake of an external system

    [[criteria]]
    text = "restart the app; the saved note is listed"
    layer = "integration"       # unit|integration|contract|e2e
    gate = 1                    # required when layer = "e2e"

Gate tasks (type = "gate") additionally:

    [gate]
    n = 1
    release = false             # exactly one gate has release = true; it is last
    launch = "npm run dev -- --db=fixture"
    seed = "npm run seed:fixture"   # optional when the journey needs no data
    unglamorous = "kill and relaunch; the note persists"
    [[gate.journey]]
    step = "create a note; it appears in the list"
    task = 2                    # the task id serving this step

PLAN.md chunks are headings matching /^#{1,4}\s*Chunk\s+(\d+)/i.
DESIGN.md contrast: token table rows `| name | #RRGGBB |...`; any table row
containing two resolvable colors is checked fg-on-bg against WCAG AA
(4.5:1, or 3:1 when the row mentions "large").
"""

import re
import sys
import tomllib
from pathlib import Path

FINDINGS: list[str] = []


def find(loc: str, check: str, msg: str) -> None:
    FINDINGS.append(f"{loc}: [{check}] {msg}")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- tasks gate

TOML_BLOCK = re.compile(r"^```toml\s*$(.*?)^```\s*$", re.M | re.S)
LAYERS = {"unit", "integration", "contract", "e2e"}
TYPES = {"scaffold", "feature", "gate", "crystallization", "fix", "proof", "spike"}
DELIVERY_KEYS = {"demo_gates", "walkthrough", "canary"}
DELIVERY_VALUES = {"required", "waived"}
WAIVERISH = re.compile(r"waiv|exception|skip", re.I)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.S)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and k.strip():
            fm[k.strip()] = v.strip()
    return fm


def parse_delivery(raw: str, loc_name: str) -> dict[str, str] | None:
    contract: dict[str, str] = {}
    for token in re.split(r"[,\s]+", raw.strip()):
        if not token:
            continue
        k, sep, v = token.partition("=")
        if not sep or k not in DELIVERY_KEYS or v not in DELIVERY_VALUES:
            find(loc_name, "delivery", f'invalid delivery token "{token}" (keys: {sorted(DELIVERY_KEYS)}, values: {sorted(DELIVERY_VALUES)})')
            return None
        contract[k] = v
    return contract


def check_delivery(tasks_path: Path, spec_path: Path | None) -> None:
    tasks_fm = parse_frontmatter(tasks_path.read_text(encoding="utf-8"))
    spec_delivery_raw = None
    if spec_path:
        spec_fm = parse_frontmatter(spec_path.read_text(encoding="utf-8"))
        spec_delivery_raw = spec_fm.get("delivery")
        if spec_delivery_raw is not None:
            parse_delivery(spec_delivery_raw, spec_path.name)
    for k, v in tasks_fm.items():
        if k == "delivery":
            if spec_path is None:
                find(tasks_path.name, "delivery", "frontmatter declares a delivery contract; re-run with --spec SPEC.md to verify it against the source of truth")
            elif spec_delivery_raw is None:
                find(tasks_path.name, "delivery", "frontmatter declares a delivery contract but SPEC.md frontmatter has none — waivers are declared in SPEC.md at cycle entry")
            elif norm(v) != norm(spec_delivery_raw):
                find(tasks_path.name, "delivery", f'delivery contract "{v}" does not echo SPEC.md\'s "{spec_delivery_raw}" verbatim')
        elif k != "status" and (WAIVERISH.search(k) or WAIVERISH.search(v)):
            find(tasks_path.name, "delivery", f'ad-hoc waiver key "{k}: {v}" — the only sanctioned waiver channel is SPEC.md\'s delivery contract, echoed as `delivery:`')


def parse_tasks(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    tasks = []
    for i, m in enumerate(TOML_BLOCK.finditer(text), 1):
        line = text[: m.start()].count("\n") + 1
        try:
            t = tomllib.loads(m.group(1))
        except tomllib.TOMLDecodeError as e:
            find(f"{path.name}:{line}", "parse", f"block {i} is not valid TOML: {e}")
            continue
        t["_line"] = line
        tasks.append(t)
    return tasks


def check_tasks(tasks_path: Path, plan_path: Path | None, arch_path: Path | None) -> None:
    tasks = parse_tasks(tasks_path)
    if not tasks:
        find(tasks_path.name, "parse", "no ```toml task blocks found")
        return
    loc = lambda t: f"{tasks_path.name}:{t.get('_line', '?')} task {t.get('id', '?')}"

    by_id: dict[int, dict] = {}
    for t in tasks:
        tid = t.get("id")
        if not isinstance(tid, int):
            find(loc(t), "schema", "missing or non-integer id")
            continue
        if tid in by_id:
            find(loc(t), "schema", f"duplicate id {tid}")
        by_id[tid] = t
        if t.get("type") not in TYPES:
            find(loc(t), "schema", f"type must be one of {sorted(TYPES)}")

    order = {t["id"]: i for i, t in enumerate(tasks) if isinstance(t.get("id"), int)}

    # dependency existence + cycles
    for t in tasks:
        for d in t.get("deps", []):
            if d not in by_id:
                find(loc(t), "deps", f"dep {d} does not exist")

    for tid, t in by_id.items():
        if any(tid == d or cyclic_path(by_id, d, tid) for d in t.get("deps", [])):
            find(loc(t), "deps", "dependency cycle through this task")

    # walking-skeleton ordering
    first_feature = next(
        (order[t["id"]] for t in tasks
         if t.get("type") == "feature" and not t.get("skeleton") and t.get("id") in order),
        None,
    )
    if first_feature is not None:
        for t in tasks:
            if t.get("skeleton") and order.get(t.get("id"), -1) > first_feature:
                find(loc(t), "skeleton", "walking-skeleton task ordered after a feature task")

    # catch-all sweeper: a non-gate task depending on nearly everything and
    # producing nothing means criteria weren't distributed to their owners
    n_other = len(by_id) - 1
    if n_other >= 4:
        for t in tasks:
            if t.get("type") in {"gate", "crystallization"}:
                continue
            if len(set(t.get("deps", []))) >= max(3, -(-n_other * 4 // 5)) and not t.get("produces"):
                find(loc(t), "catch-all", "depends on nearly every other task and produces nothing — distribute its criteria to the tasks that own the behavior")

    # chunk coverage (needs PLAN.md)
    if plan_path:
        plan_chunks = {
            int(m.group(1))
            for m in re.finditer(r"^#{1,4}\s*Chunk\s+(\d+)", plan_path.read_text(encoding="utf-8"), re.M | re.I)
        }
        served = {t.get("chunk") for t in tasks if isinstance(t.get("chunk"), int)}
        for c in sorted(plan_chunks - served):
            find(plan_path.name, "chunk", f"Chunk {c} has no task implementing it")
        for t in tasks:
            c = t.get("chunk")
            if isinstance(c, int) and plan_chunks and c not in plan_chunks:
                find(loc(t), "chunk", f"serves chunk {c}, which is not in PLAN.md")

    # criteria
    gates = {t["gate"]["n"]: t for t in tasks if t.get("type") == "gate" and isinstance(t.get("gate"), dict) and "n" in t["gate"]}
    for t in tasks:
        for c in t.get("criteria", []):
            layer = c.get("layer")
            if layer not in LAYERS:
                find(loc(t), "layer-tag", f'criterion "{norm(c.get("text", ""))[:60]}" missing/invalid layer tag')
                continue
            if layer == "e2e":
                g = c.get("gate")
                if g not in gates:
                    find(loc(t), "e2e-gate", f"e2e criterion names gate {g}, which has no gate task")
                elif t.get("type") != "crystallization":  # a crystallization criterion IS the journey

                    steps = [norm(j.get("step", "")).lower() for j in gates[g]["gate"].get("journey", [])]
                    if norm(c.get("text", "")).lower() not in steps and not any(
                        norm(c.get("text", "")).lower() in s for s in steps
                    ):
                        find(loc(t), "e2e-gate", f'e2e criterion "{norm(c.get("text",""))[:60]}" absent from gate {g} journey')
        if t.get("produces") and not any(c.get("layer") == "contract" for c in t.get("criteria", [])):
            find(loc(t), "contract", "PRODUCES block without a [contract] criterion")
        if t.get("fake_of") and not any(c.get("layer") == "contract" for c in t.get("criteria", [])):
            find(loc(t), "verified-fake", f'fake of "{t["fake_of"]}" missing its shared-suite [contract] criterion')

    # gate tasks
    release_gates = []
    gate_positions = []
    for t in tasks:
        if t.get("type") != "gate":
            continue
        g = t.get("gate")
        if not isinstance(g, dict):
            find(loc(t), "gate", "gate task missing its [gate] table")
            continue
        gate_positions.append(order.get(t.get("id"), 0))
        if not g.get("launch"):
            find(loc(t), "preflight", "gate missing launch command")
        if not g.get("unglamorous"):
            find(loc(t), "unglamorous", "gate journey missing its unglamorous step")
        journey = g.get("journey", [])
        if not journey:
            find(loc(t), "gate", "gate has an empty journey")
        for j in journey:
            sid = j.get("task")
            if sid is None:
                find(loc(t), "gate-journey", f'journey step "{norm(j.get("step",""))[:60]}" names no serving task')
                continue
            if sid not in by_id:
                find(loc(t), "gate-journey", f"journey step serving task {sid} does not exist")
                continue
            if order[sid] >= order.get(t.get("id"), 0):
                find(loc(t), "gate-journey", f"serving task {sid} is not earlier than the gate")
            if sid not in t.get("deps", []):
                find(loc(t), "gate-deps", f"serving task {sid} missing from the gate's deps")
        if g.get("release"):
            release_gates.append(t)
        # crystallization adjacency: next task in file order
        idx = order.get(t.get("id"))
        nxt = tasks[idx + 1] if idx is not None and idx + 1 < len(tasks) else None
        if not g.get("release") and (
            nxt is None or nxt.get("type") != "crystallization" or nxt.get("gate") != g.get("n")
        ):
            find(loc(t), "crystallization", f"gate {g.get('n')} not immediately followed by its crystallization task")

    if not release_gates:
        find(tasks_path.name, "release-gate", "no RELEASE GATE task (a gate with release = true)")
    elif len(release_gates) > 1:
        find(tasks_path.name, "release-gate", "more than one gate has release = true")
    elif gate_positions and order.get(release_gates[0].get("id"), -1) != max(gate_positions):
        find(loc(release_gates[0]), "release-gate", "release gate is not the last gate")

    # CONSUMES quotes vs earlier PRODUCES / ARCHITECTURE.md text
    arch_norm = norm(arch_path.read_text(encoding="utf-8")) if arch_path else None
    for t in tasks:
        earlier_produces = {
            norm(p)
            for u in tasks
            if order.get(u.get("id"), 1 << 30) < order.get(t.get("id"), 0)
            for p in u.get("produces", [])
        }
        for c in t.get("consumes", []):
            n = norm(c)
            if n in earlier_produces:
                continue
            if arch_norm is not None and n in arch_norm:
                continue
            src = "no earlier PRODUCES matches it" + (
                " and it does not appear verbatim in ARCHITECTURE.md" if arch_norm is not None else ""
            )
            find(loc(t), "consumes", f'CONSUMES "{n[:70]}": {src}')

    # wire contracts → production-composition proof on the release gate
    if arch_norm and re.search(r"wire contract", arch_norm, re.I) and release_gates:
        rg = release_gates[0]
        proof_ids = {
            t["id"] for t in tasks
            if t.get("type") == "proof" or t.get("production_composition_proof")
            if isinstance(t.get("id"), int)
        }
        if not proof_ids & set(rg.get("deps", [])):
            find(loc(rg), "proof", "ARCHITECTURE.md has wire contracts but the release gate lists no production-composition proof task in deps")


def cyclic_path(by_id: dict, start: int, target: int) -> bool:
    seen, stack = set(), [start]
    while stack:
        n = stack.pop()
        if n == target:
            return True
        if n in seen:
            continue
        seen.add(n)
        stack += [d for d in by_id.get(n, {}).get("deps", []) if d in by_id]
    return False


# ----------------------------------------------------------------- docs gate

PLACEHOLDER = re.compile(
    r"\bTBD\b|\bTODO\b|\bFIXME\b|\bXXX\b|\{\{[^}]*\}\}|\[(?:TBD|TODO|FILL|PLACEHOLDER)[^\]]*\]|lorem ipsum",
    re.I,
)
HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def rel_lum(hexcolor: str) -> float:
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    chan = []
    for i in (0, 2, 4):
        c = int(h[i : i + 2], 16) / 255
        chan.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = chan
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    l1, l2 = sorted((rel_lum(fg), rel_lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def check_docs(paths: list[Path]) -> None:
    for p in paths:
        text = p.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                continue
            m = PLACEHOLDER.search(line)
            if m:
                find(f"{p.name}:{i}", "placeholder", f'unresolved placeholder "{m.group(0)}"')
        if "DESIGN" in p.name.upper():
            # token name -> hex from any 2+-column table row
            tokens: dict[str, str] = {}
            for row in re.finditer(r"^\|([^|\n]+)\|([^|\n]*#[0-9a-fA-F]{3,6}[^|\n]*)\|", text, re.M):
                hx = HEX.search(row.group(2))
                if hx:
                    tokens[norm(row.group(1)).lower()] = hx.group(0)
            header = ""
            for i, line in enumerate(text.splitlines(), 1):
                s = line.strip()
                if not s.startswith("|"):
                    header = ""
                    continue
                if set(s) <= {"|", "-", ":", " "}:
                    continue
                if not header:
                    header = s.lower()
                    continue
                if not (("fg" in header and "bg" in header) or "contrast" in header):
                    continue
                cells = [norm(c) for c in s.strip("|").split("|")]
                colors = []
                for c in cells:
                    hx = HEX.search(c)
                    if hx:
                        colors.append(hx.group(0))
                    elif c.lower() in tokens:
                        colors.append(tokens[c.lower()])
                if len(colors) >= 2:
                    ratio = contrast(colors[0], colors[1])
                    threshold = 3.0 if "large" in line.lower() else 4.5
                    if ratio < threshold:
                        find(f"{p.name}:{i}", "contrast",
                             f"{colors[0]} on {colors[1]} = {ratio:.2f}:1, below WCAG AA {threshold}:1")
                    stated = re.search(r"(\d+(?:\.\d+)?)\s*:\s*1", line)
                    if stated and abs(float(stated.group(1)) - ratio) > 0.15:
                        find(f"{p.name}:{i}", "contrast",
                             f"stated ratio {stated.group(1)}:1 but computed {ratio:.2f}:1")


# ----------------------------------------------------------------------- cli

def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2 if len(argv) < 2 else 0
    cmd, args = argv[1], argv[2:]
    try:
        if cmd == "tasks":
            if not args:
                print("usage: brana-gate tasks TASKS.md [--plan PLAN.md] [--arch ARCHITECTURE.md] [--spec SPEC.md]", file=sys.stderr)
                return 2
            plan = arch = spec = None
            pos = []
            it = iter(args)
            for a in it:
                if a == "--plan":
                    plan = Path(next(it))
                elif a == "--arch":
                    arch = Path(next(it))
                elif a == "--spec":
                    spec = Path(next(it))
                else:
                    pos.append(Path(a))
            check_tasks(pos[0], plan, arch)
            check_delivery(pos[0], spec)
        elif cmd == "docs":
            if not args:
                print("usage: brana-gate docs FILE [FILE...]", file=sys.stderr)
                return 2
            check_docs([Path(a) for a in args])
        else:
            print(f"unknown subcommand {cmd!r}; see --help", file=sys.stderr)
            return 2
    except FileNotFoundError as e:
        print(f"brana-gate: {e}", file=sys.stderr)
        return 2
    for f in FINDINGS:
        print(f)
    print(f"brana-gate: {len(FINDINGS)} finding(s)", file=sys.stderr)
    return 1 if FINDINGS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
