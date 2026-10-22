# Evaluation results

Written reports from running Vixl's agent evals and the tool comparison. Newest first. The raw material is in
[`evals/`](../evals/README.md).

| Report | Vixl | What it covers |
| --- | --- | --- |
| [2026-10-13 blind re-judging](2026-10-13-blind-rejudging.md) | 0.26.0 | **The current scores.** Every lane of the tool comparison rebuilt and scored again, blind, by three judges plus a human calibration set |
| [2026-10-12 evaluation](2026-10-12-vixl-0.26-evaluation.md) | 0.26.0 | The agent eval suite (31 tasks) and the Vixl lane of the tool comparison. Its tool-comparison scores are superseded by 10-13; the runs and timings stand |
| [2026-10-12 gallery](2026-10-12-gallery.md) | 0.26.0 | Every lane's deliverables side by side for all 16 tests, with the previews in [`2026-10-12-gallery/`](2026-10-12-gallery/) |
| [2026-10-06 tool comparison](2026-10-06-vixl-0.20-tool-comparison.md) | 0.20.0 | The Vixl lane re-run |
| [2026-10-05 full evaluation](2026-10-05-full-evaluation.md) | 0.18.0 | The first full run: the agent suite and every agent lane of the tool comparison |
| [`report.md`](report.md), [`results.json`](results.json) | n/a | The offline reference replay of the agent suite (a scripted agent that follows the known-good steps), used as the acceptance baseline |

## The short version

- **Agents finish the work.** On 0.26.0 a live agent passed 31 of 31 tasks, at about 7 tool calls each.
- **Fidelity, editability and honesty are strong in every Vixl run.** Round 2 asks a fresh session to change a
  finished piece; Vixl's median editability is 5 out of 5, and all 16 run reports match the files.
- **Craft is where it loses.** Judged blind, web code (HTML and CSS rendered in a browser) was picked over Vixl
  in 16 of 27 side-by-side calls, mostly by slight margins. Vixl beat the Python lane in 15 of 27. Spacing, rhythm
  and alignment are its weakest sub-scores, and the reports list the specific defects.

The reports keep their original wording and Vixl versions; later releases fixed several of the defects they name.
