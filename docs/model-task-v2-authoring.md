# Model task v2: canonical declarations

New candidates should use `representation` with exactly one of `living-reconstruction`,
`fossil-specimen`, `geological-form`, or `trace-concept`. Keep the detailed scientific
scope, reconstruction limits and uncertainty in separate brief fields.

Use `making: COMPLETE` after maker work is complete and `tests: PASS_TECHNICAL_SCOPE`
only when the linked technical evidence supports that scoped result. Neither value
is independent approval. Keep the independent decision and reviewer status separate;
use `PASS` only after the independent review actually passes. Preserve explicit
unrun GPU, scene, user and deployment states. Never replace an old frozen decision
or historical failure to conform to this spelling.

For resolved issues use `reviewer_status: CLOSED` only after independent closure;
retain the original findings and hash-bound closure evidence. An open or failed
current field cannot be superseded by adding a second successful-looking field.

The adapter accepts a finite set of reviewed historical spellings. It preserves
the original declarations and qualifications rather than interpreting a `PASS`
substring or turning technical completion into independent or runtime approval.
New unknown spellings remain on hold until their evidence and meaning are reviewed.
