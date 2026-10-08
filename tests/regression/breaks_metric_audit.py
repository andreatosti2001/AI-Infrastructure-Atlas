"""The metric-audit layer: the metrics layer plus one break per remediation of the metric audit (D-133 to D-137).

Loads `tests/regression/breaks_metrics.py`, replaces the breaks whose setup text the remediations changed
(named below, with the reason), and adds its own breaks and controls, under the same rules.

A layer of the full harness: run it through `tests/regression/breaks.py`, which replaces the breaks whose
setup text later changes removed. Run alone, some of this layer's breaks no longer apply.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("s15_breaks", REPO / "tests/regression/breaks_metrics.py")
s15 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s15)
edit, ALL, INSIGHT, INSIGHT_BUILD = s15.edit, s15.ALL, s15.INSIGHT, s15.INSIGHT_BUILD
COV, AGE = s15.COV, s15.AGE

# Breaks whose setup text S16 changed, each replaced by the same fault on the S16 tree:
# S15-M3 moved the literal 2026-10-06, which D-137 moved to 2026-10-07.
REPLACED = {
    "S15-M3": ("S15-M3", "the reference date moved, results not rebuilt",
               edit(AGE, "DATE '2026-10-07' AS reference_date", "DATE '2027-10-07' AS reference_date"), [],
               ["is not a fresh run of the current inputs"]),
}

S16 = [
    ("S16-A1", "the retired publishers block put back by the build (rebuilt)",
     edit(INSIGHT_BUILD, '<div class="indicators">{k1}{k2}</div>',
          '<div class="indicators">{k1}{k2}<div class="indicator"><h4>Publishers behind a sourced link</h4><p>{self.derived("pub-min", "1")}</p></div></div>'),
     [INSIGHT_BUILD], ["a retired publishers tally is back"]),
    ("S16-A2", "a row's 'one publisher only' flag removed from the research view by hand",
     edit(INSIGHT, '<span data-derived="sql-flag" data-row="0" data-column="publishers">one publisher only</span>', ""), [],
     ["a row on one publisher lost its flag"]),
    ("S16-A4", "the coverage records count typed by the build instead of copied from its cell (rebuilt)",
     edit(INSIGHT_BUILD, '{self.label("links come from")} {m("records")}', '{self.label("links come from")} {c["records"]}'),
     [INSIGHT_BUILD], ["a records count typed, not copied from its cell"]),
    ("S16-A5", "the age block's note back to 'Dates, not ages' (rebuilt)",
     edit(INSIGHT_BUILD, 'f\'<p class="how">{self.label("Twelve months is a reading aid: the Atlas’s re-check rule applies it only to who fabricates a product and who supplies a part.")} \'',
          'f\'<p class="how">\''),
     [INSIGHT_BUILD], ["the age block reads 'older than twelve months' as 'needs re-checking' for every link"]),
    ("S16-A6", "source age's tutorial states the old, wrong rule again (rebuilt)",
     edit(AGE, """--   Age is not reliability. Past 12 months, the freshness rule asks for newer evidence only on a
--   time-sensitive link, and even then it does not withdraw the link; a stable link (who designs a
--   product, what it incorporates, what a part requires) has no age limit.""",
          """--   Age is not reliability. Past the horizon, the freshness rule asks for newer evidence before the
--   value is used again; it does not withdraw the link."""),
     ALL, ["the old, wrong statement of the rule is back"]),
    ("S16-A7", "coverage's population no longer says which refused relations are rows (rebuilt)",
     edit(COV, """--   an edge (who supplies the part) is a row of its own. A relation the Atlas considered and refused is a
--   row, as a gap, only when its one reason is that its evidence is too old; refused for any other reason,
--   it is in no row. It is""", """--   an edge (who supplies the part) is a row of its own. It is"""),
     ALL, ["coverage's population does not say which refused relations are rows"]),
    ("S16-C1", "control: the reference date moved one day, everything rebuilt (D-137's move)",
     edit(AGE, "DATE '2026-10-07' AS reference_date", "DATE '2026-10-08' AS reference_date"), ALL, []),
]

# S16-A3: the old records line, both its rendering and its labels
S16.insert(2, ("S16-A3", "the coverage records line readers did not understand put back (rebuilt)",
          s15.both(
              edit(INSIGHT_BUILD, """f'<span class="recs">{self.label("The")} {m("links")} {self.label("links come from")} {m("records")} {self.label("records;")} {m("shared")} '
                f'{self.label("record is also counted under another accelerator" if c["shared"] == 1 else "records are also counted under another accelerator")}</span></li>'""",
                   """f'<span class="recs">{self.label("rows drawn from")} {m("records")} {self.label("records, of which shared with another accelerator:")} {m("shared")}</span></li>'"""),
              edit(INSIGHT_BUILD, '        "The", "links come from",', '        "rows drawn from", "records, of which shared with another accelerator:", "The", "links come from",')),
          [INSIGHT_BUILD], ["the records line readers did not understand is back"]))
S16.append(("S16-C2", "control: coverage's population reworded, keeping what WH-15 requires, everything rebuilt",
           edit(COV, "It is a census of what the Atlas has recorded, not of the world's supply chain.",
                "It counts what the Atlas has recorded, not the world's supply chain."), ALL, []))


S15_BREAKS = s15.breaks


def breaks():
    return [REPLACED.get(b[0], b) for b in S15_BREAKS()] + S16


if __name__ == "__main__":
    s15.breaks = breaks
    args = [a for a in sys.argv[2:] if a != "--setup-only"]
    sys.exit(1 if s15.run(Path(sys.argv[1]), set(args), "--setup-only" in sys.argv) else 0)
