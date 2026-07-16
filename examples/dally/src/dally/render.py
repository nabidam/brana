"""Rendering — Rich tables, confirmations, empty states, mood color scale.

Pure formatting: takes plain data / ``Entry`` and prints Rich renderables to
stdout; imports no ``cli`` (ARCHITECTURE.md §Module layout). The mood palette is
defined once here and reused by every surface (CONVENTIONS.md §Output style).
Never color-only — mood is always printed as its number; Rich handles ``NO_COLOR``
natively, so no manual ANSI is emitted. Free text (notes, messages) is rendered
via ``Text`` so brackets/emoji can never be mistaken for Rich markup.
"""

from __future__ import annotations

import calendar

from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

from dally.reports import HeatCell, Heatmap, Report
from dally.storage import Entry

console = Console()

# The single mood palette (SPEC.md §Design direction; UX.md §Density & color):
# 1→5 red → dim → neutral → green → bright green. "default" is the terminal's
# own foreground (the neutral middle). No other module defines mood colors.
_MOOD_STYLES: dict[int, str] = {
    1: "red",
    2: "dim",
    3: "default",
    4: "green",
    5: "bright_green",
}


def mood_style(mood: int) -> str:
    """Return the Rich style for a 1–5 mood. Raises ValueError outside range."""
    try:
        return _MOOD_STYLES[mood]
    except KeyError:
        raise ValueError(f"mood must be between 1 and 5, got {mood}") from None


def confirmation(entry: Entry) -> None:
    """S1 — a one-line confirmation: check, date, mood (number + color), note."""
    text = Text()
    text.append("✓ ", style="green")
    text.append(entry.date.isoformat())
    text.append("  mood ")
    text.append(str(entry.mood), style=mood_style(entry.mood))
    if entry.note:
        text.append("  ")
        text.append(entry.note)
    console.print(text)


def entries_table(entries: list[Entry]) -> None:
    """S2 — one Rich table, one row per entry in the order given (newest first).

    Data uses the terminal's default foreground; color lands only on the mood
    value, which is always shown as its number.
    """
    table = Table(box=box.SIMPLE, padding=(0, 2), header_style="bold")
    table.add_column("Date")
    table.add_column("Mood", justify="right")
    table.add_column("Note")
    for entry in entries:
        mood_cell = Text(str(entry.mood), style=mood_style(entry.mood))
        table.add_row(entry.date.isoformat(), mood_cell, entry.note or "")
    console.print(table)


def _nearest_mood(average: float) -> int:
    """Clamp a fractional average onto the 1–5 palette for color only."""
    return max(1, min(5, round(average)))


def _average_cell(average: float) -> Text:
    """An average shown as its number, colored via the shared mood palette."""
    return Text(f"{average:.1f}", style=mood_style(_nearest_mood(average)))


def report_table(report: Report) -> None:
    """S3 — a period header (name, range, average) then a breakdown table.

    Day buckets for week/month, month buckets for year. Averages always print as
    numbers (never color-only) on the single mood palette; buckets with no
    entries render as empty cells, not zeros.
    """
    header = Text()
    header.append(f"{report.period.capitalize()}  ")
    header.append(f"{report.start.isoformat()} – {report.end.isoformat()}")
    header.append("   average ")
    header.append("—" if report.average is None else _average_cell(report.average))
    console.print(header)

    is_year = report.period == "year"
    table = Table(box=box.SIMPLE, padding=(0, 2), header_style="bold")
    table.add_column("Month" if is_year else "Day")
    table.add_column("Average", justify="right")
    for bucket in report.buckets:
        cell = "" if bucket.average is None else _average_cell(bucket.average)
        table.add_row(bucket.label, cell)
    console.print(table)


def empty_state(message: str) -> None:
    """A friendly one-line empty state (the caller decides the exit code)."""
    console.print(Text(message))


# S6 — heatmap. 7 day-of-week rows (Sunday..Saturday) × week columns, `gh`-style.
# Glyphs are chosen so an empty windowed day (`·`) is distinct from every mood
# color (all `■`) and from a padding slot (blank) — never color alone.
_DAY_LABELS = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
_CELL = "■"
_EMPTY_CELL = "·"


def _cell_text(cell: HeatCell) -> Text:
    """One grid glyph: colored mood square, empty-day dot, or blank padding."""
    if cell.day is None:  # padding slot outside the window
        return Text(" ")
    if cell.average is None:  # windowed day with no entry
        return Text(_EMPTY_CELL, style="dim")
    return Text(_CELL, style=mood_style(_nearest_mood(cell.average)))


def _month_header(weeks: list[list[HeatCell]]) -> Text:
    """Month abbreviations placed above the column where each month first starts.

    Abbreviations overflow rightward into later (blank) slots, GitHub-style —
    columns are one glyph wide, so a 3-letter label spans three columns.
    """
    slots = [" "] * (len(weeks) + 3)
    previous_month: int | None = None
    next_free_column = 0  # earliest column a label may start, so labels never collide
    for column, week in enumerate(weeks):
        first_day = next((cell.day for cell in week if cell.day is not None), None)
        if first_day is None:
            continue
        if first_day.month != previous_month:
            previous_month = first_day.month
            if column < next_free_column:  # too close to the last label — skip it
                continue
            abbreviation = calendar.month_abbr[first_day.month]
            for offset, char in enumerate(abbreviation):
                slots[column + offset] = char
            next_free_column = column + len(abbreviation)
    return Text("     " + "".join(slots).rstrip())  # 5-space day-label gutter


def _legend(label: str) -> Text:
    """Label plus a 1–5 color key (numbers always shown) and the empty marker."""
    text = Text()
    text.append(f"{label}   ", style="bold")
    text.append("mood ")
    for mood in range(1, 6):
        text.append(str(mood))
        text.append(_CELL, style=mood_style(mood))
        text.append(" ")
    text.append("  ")
    text.append(_EMPTY_CELL, style="dim")
    text.append(" no entry")
    return text


def heatmap_grid(heatmap: Heatmap) -> None:
    """S6 — a GitHub-style mood calendar: month header, 7 day rows, legend.

    Cells reuse the single 1–5 mood palette (`mood_style`); an empty windowed day
    and a padding slot render distinct from every mood color. Mood is never
    conveyed by color alone — the legend names the numbers. Rich handles
    `NO_COLOR` natively, so the grid still reads without color.
    """
    console.print(_month_header(heatmap.weeks))
    for row in range(7):
        line = Text(f"{_DAY_LABELS[row]:<5}")
        for week in heatmap.weeks:
            line.append_text(_cell_text(week[row]))
        console.print(line)
    console.print(_legend(heatmap.label))
