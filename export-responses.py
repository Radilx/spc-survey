#!/usr/bin/env python3
"""Download every survey response to responses.csv. Needs `gcloud auth login` as a project owner."""
import csv, json, subprocess, urllib.request

PROJECT = 'spc-debate-survey-2026'
COLS = ['submitted', 'name', 'q1', 'q1Explain', 'q2', 'q3', 'q3Explain', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

token = subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()
base = f'https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/responses?pageSize=300'

def value(v):
    if 'arrayValue' in v:
        return ' > '.join(x.get('stringValue', '') for x in v['arrayValue'].get('values', []))
    return v.get('stringValue', '')

rows, page = [], ''
while True:
    req = urllib.request.Request(base + (f'&pageToken={page}' if page else ''), headers={'Authorization': f'Bearer {token}'})
    data = json.load(urllib.request.urlopen(req))
    for doc in data.get('documents', []):
        row = {k: value(v) for k, v in doc['fields'].items()}
        row['submitted'] = doc['createTime']
        rows.append(row)
    page = data.get('nextPageToken')
    if not page:
        break

rows.sort(key=lambda r: r['submitted'])
with open('responses.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
print(f'{len(rows)} responses → responses.csv')
