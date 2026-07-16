# Dally — UX (lite)

CLI app: "screens" are command output surfaces rendered by Rich to stdout (errors to stderr).

## Screen inventory

| id | Surface | Purpose | Entry point |
|----|---------|---------|-------------|
| S1 | Add confirmation | Confirm a saved mood entry: date, mood (number + color), note if given | `dally mood add <1-5> [--note TEXT] [--date YYYY-MM-DD]` |
| S2 | Entry list | Recent entries as a Rich table (date, mood, note), newest first | `dally mood list` |
| S3 | Report | Period average + breakdown table (per-day for week/month, per-month for year) | `dally report week\|month\|year` |
| S4 | Error message | One-line actionable error on stderr, non-zero exit | Any command with invalid input |
| S5 | Help | Typer-generated usage/help | `dally --help`, `dally mood --help`, bare/unknown command |

## Kernel flow

1. User runs `dally mood add 4 --note "good run"` → system creates DB/schema if missing, saves entry → S1 shows confirmation: today's date, mood **4** (green), note "good run".
2. User runs `dally mood add 2 --date 2026-07-14` → system validates date (not future, well-formed), saves → S1 confirms with the backdated date and mood **2** (dim).
3. User runs `dally mood list` → S2 table shows both entries, newest date first, mood color-coded 1→5 (red → dim → neutral → green → bright green), note column intact (unicode/emoji preserved).
4. User closes terminal, opens a new one, runs `dally mood list` → S2 shows the same two entries (persistence).
5. User runs `dally report week` → S3 shows current ISO week (Mon–Sun): header line with period + average (1 decimal, mean of daily averages), then per-day table — logged days show their daily average, unlogged days show as empty and are excluded from the average.

## Empty / error states (one line per screen)

- **S1**: invalid mood (`0`, `6`, `abc`) or bad/future `--date` → S4 error naming the valid range/format, exit non-zero, nothing written.
- **S2**: no entries → friendly empty state ("No moods logged yet — try `dally mood add 4`"), exit 0.
- **S3**: period with zero entries → friendly "no data for this <period>" message, exit 0; days with no entries render as empty cells, not zeros.
- **S4**: always stderr, one line, names what was wrong and what valid looks like; never a stack trace.
- **S5**: unknown command/args → Typer usage message + hint, exit non-zero.

## Density & color notes

- Airy: one table per invocation, generous padding, quiet color (`gh`-style).
- Mood color scale identical in S1/S2/S3; mood always shown as the number too (never color-only); respects `NO_COLOR`.
