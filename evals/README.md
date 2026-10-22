# Evals

Two kinds of evidence about how well agents can drive Vixl. The harness that produces them lives in the Vixl
repository ([`evals/`](https://github.com/jxburros/Vixl/blob/main/evals/README.md)); this folder holds the
recordings and the hand-run kit. The write-ups that interpret them are in [`eval-results/`](../eval-results/README.md).

| Folder | What it is |
| --- | --- |
| [`tool-comparison/`](tool-comparison/README.md) | A kit for running the same 16 briefs through Vixl and the other ways an AI can make the same thing (web code, Python, command-line tools, image generation, Claude Design), then judging the results blind |
| [`live-runs/`](live-runs/) | Workspaces from live agent runs on Vixl's task suite: each task folder holds the prompt and the files the agent produced |

## Live runs

A live run gives an agent one task from Vixl's agent-eval suite (for example "export a CMYK TIFF" or "fix the
spacing in this layout") and grades what it left behind.

| Folder | Vixl | Tasks | Notes |
| --- | --- | ---: | --- |
| [`live-runs/`](live-runs/) (the task folders next to `grades.json`) | 0.18.0, 2026-10-05 | 18 | `agent-log-a.json` and `agent-log-b.json` are the agents' notes per task |
| [`live-runs/2026-10-12/`](live-runs/2026-10-12/) | 0.26.0, 2026-10-12 | 31 | The same layout, with the 13 tasks added since |

The call budgets in Vixl's offline baseline are based on these recordings. Each task folder has a `PROMPT.txt`;
open the `.vixl` files in it to see the agent's work.
