# South Park Debating survey

Live at https://radilx.github.io/spc-survey/

Responses are saved to Firestore (project `spc-debate-survey-2026`, collection `responses`). Security rules let the page create responses but nobody can read them from the browser.

To download all responses: `./export-responses.py` (writes `responses.csv`; needs `gcloud auth login` as a project owner). Or browse them in the Firebase console.
