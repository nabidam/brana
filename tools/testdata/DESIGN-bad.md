# Contrast regression fixture (must FAIL brana-gate docs)

CI runs the gate against this file and asserts a non-zero exit — proving the
contrast parser still computes ratios and rejects WCAG AA violations. If the
gate ever passes this file, the parser regressed.

| token | value |
|---|---|
| text-muted | #777777 |
| bg-base | #FFFFFF |

| fg | bg | contrast |
|---|---|---|
| text-muted | bg-base | 4.6:1 |
