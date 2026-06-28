surfaced: 0

[CONTRACT]
The model-driven depth scan's findings reach the operator view through a committed-trace path. A dedicated watched run assesses the standing architecture-review map and commits its verdict as a depth-scan trace on the tree, under the depth scan's own mechanism name. The operator view reads that committed trace and surfaces the depth findings as their own region, beside the length and mechanical complexity debt — read from the static trace, with the model never running in the render. The deterministic complexity-debt and structural renders stay byte-identical to the architecture review's output, so the watched scan never enters the deterministic view-render and the byte-exact gap/debt/structure checks stay green on merged main. When no depth-scan verdict is committed, the region says so. Scheduling the run in production stays a follow-up; this builds and gates the committed-trace path end to end.

[DELTA]
# delta — surface the watched depth-scan trace into the operator view

## ADDED — self-model
### Requirement: the operator view surfaces the committed depth-scan trace beside the complexity debt
The committed-trace path MUST carry the model-driven depth scan's findings into the operator view. A
dedicated watched run assesses the standing architecture-review map through the injected model
transport. The run commits its verdict as a depth-scan trace on the tree, under the depth scan's own
mechanism name. That committed trace is the durable artifact the view reads. The model runs only in
this dedicated run. The operator view MUST surface that committed trace as its own region, beside the
length-and-mechanical complexity debt. The view reads the static trace and runs no scan. So the
deterministic complexity-debt and structural renders stay byte-identical to the architecture review's
output, and the watched scan stays out of the deterministic view-render. The view reads the trace by the
depth scan's own mechanism name, distinct from the fenced-run and vocabulary verdicts on the same seam.
When no depth-scan verdict is committed, the region says so.

#### Scenario: the dedicated run commits a trace the view surfaces, the deterministic renders unchanged
- WHEN the dedicated watched run commits the depth scan's verdict on the tree and the operator opens the
  view
- THEN the view surfaces that committed finding as its own region beside the complexity debt, read with
  no model run; the complexity-debt and structural renders stay byte-identical to the architecture
  review's deterministic output

  ```check
  depth-run commits-trace
  read view
  depth-region surfaces
  render-deterministic debt structure
  ```
