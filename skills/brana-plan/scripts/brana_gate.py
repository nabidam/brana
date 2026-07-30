#!/usr/bin/env python3
r"""brana-gate — deterministic checks for the Brana v2 workflow.

Python 3.11+, stdlib only. Exit codes: 0 clean, 1 findings, 2 usage/parse error.

Subcommands:
  docs FILE [FILE...]
      Plan self-review scriptable checks: unresolved placeholders in every
      file passed, and computed WCAG contrast for DESIGN.md token tables
      (never ask an LLM to compute a contrast ratio). Contrast runs only on
      files whose name contains "DESIGN" — when the UI-heavy risk module is
      active, invoke as: brana-gate docs PLAN.md DESIGN.md

      Contrast table shape DESIGN.md must use:
        - token definitions: any table row `| name | #RRGGBB | ... |`
        - checked rows: rows of a table whose header mentions fg/bg or
          "contrast"; the first two colors in the row (hex or defined token
          names) are checked fg-on-bg against WCAG AA (4.5:1, or 3:1 when
          the row mentions "large"). A stated `N:1` ratio in the row is
          verified against the computed one.

  claims FILE [FILE...] [--root DIR]
      Doc-grounding check (doc sync after every merge): every backticked
      repo-relative path a doc cites must exist in the working tree. Run
      AFTER implementation — planning docs legitimately cite future files.
      Tokens are checked only when path-shaped (a known code extension, or
      the first segment is an existing directory under --root, default CWD);
      slash-delimited identifiers (branch names, git refs, routes,
      signatures) are skipped, as are fenced code blocks.

The v1 `tasks` subcommand (TOML task schema, gate anatomy, done-mark
integrity) was removed in v2.0 with the TASKS.md artifact it checked.
"""

import re
import sys
from pathlib import Path

FINDINGS: list[str] = []


def find(loc: str, check: str, msg: str) -> None:
    FINDINGS.append(f"{loc}: [{check}] {msg}")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


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


# ---------------------------------------------------------------- claims gate

BACKTICK_TOKEN = re.compile(r"`([^`\n]+)`")
CODE_EXTS = {
    "py", "ts", "tsx", "js", "jsx", "mjs", "cjs", "rs", "go", "rb", "java", "kt",
    "swift", "c", "h", "cpp", "hpp", "cs", "sh", "bash", "zsh", "sql", "css",
    "scss", "html", "vue", "svelte", "md", "json", "toml", "yaml", "yml", "txt",
    "csv", "env", "lock", "cfg", "ini", "prisma", "proto",
}
SEGMENT = re.compile(r"^[\w.@\[\]-]+$")


def claim_status(token: str, doc: Path, root: Path) -> str:
    """'exists' | 'missing' (path-shaped, nowhere on disk) | 'skip' (not a path claim)."""
    tok = token.strip().rstrip("/")
    if (
        "/" not in tok
        or any(ch in tok for ch in " \t*?{}<>|()=:$~,")
        or tok.startswith(("http", "/", "-", "."))
        or "NNN" in tok
        or "\\" in tok
    ):
        return "skip"
    for base in (root, doc.parent):
        if (base / tok).exists():
            return "exists"
    segs = tok.split("/")
    if not all(SEGMENT.match(s) for s in segs if s):
        return "skip"
    ext = segs[-1].rsplit(".", 1)[-1].lower() if "." in segs[-1] else ""
    first_is_dir = (root / segs[0]).is_dir() or (doc.parent / segs[0]).is_dir()
    return "missing" if ext in CODE_EXTS or first_is_dir else "skip"


def check_claims(paths: list[Path], root: Path) -> None:
    for p in paths:
        text = p.read_text(encoding="utf-8")
        fenced = False
        seen: set[str] = set()
        for i, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            for m in BACKTICK_TOKEN.finditer(line):
                tok = m.group(1)
                if tok in seen:
                    continue
                seen.add(tok)
                if claim_status(tok, p, root) == "missing":
                    find(f"{p.name}:{i}", "claims", f'cited path "{tok}" does not exist in the working tree')


# ----------------------------------------------------------------------- cli

def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2 if len(argv) < 2 else 0
    cmd, args = argv[1], argv[2:]
    try:
        if cmd == "docs":
            if not args:
                print("usage: brana-gate docs FILE [FILE...]", file=sys.stderr)
                return 2
            check_docs([Path(a) for a in args])
        elif cmd == "claims":
            root = Path.cwd()
            files = []
            it = iter(args)
            for a in it:
                if a == "--root":
                    root = Path(next(it))
                else:
                    files.append(Path(a))
            if not files:
                print("usage: brana-gate claims FILE [FILE...] [--root DIR]", file=sys.stderr)
                return 2
            check_claims(files, root)
        elif cmd == "tasks":
            print("brana-gate: the v1 `tasks` subcommand was removed in v2.0 "
                  "(the TASKS.md artifact it checked no longer exists); "
                  "use `docs` and `claims`", file=sys.stderr)
            return 2
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
