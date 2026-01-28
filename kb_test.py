#!/usr/bin/env python3
import urllib.request
import json

prompts = [
    "What is complexity? Give a short definition.",
    "How does a rugged landscape differ from a dancing landscape?",
    "Give a 5-step checklist to prepare an organization for tipping-point monitoring.",
    "When should I use an agent-based model?",
    "Name 3 indicators of growing systemic vulnerability.",
    "How to balance explore vs exploit in a product team?",
    "What is self-organized criticality in practical terms?",
    "Which network metrics should I monitor monthly?",
    "How to implement staged rollouts for policy changes?",
    "What monitoring metrics indicate non-stationarity?",
    "How to write a governance rule for tipping points?",
    "Provide a minimal ABM skeleton for an evacuation simulation.",
    "When is diversity counterproductive?",
    "Explain simulated annealing in 3 sentences.",
    "What is a dancing landscape and how to respond?",
    "Which measures increase organizational resilience?",
    "How to detect path dependence in projects?",
    "List 5 further reading references.",
    "How to generate early indicators from log data?",
    "Explain difference between emergence and randomness."
]

url = 'http://127.0.0.1:5001/ask'
headers = {'Content-Type': 'application/json'}

results = []
for p in prompts:
    data = json.dumps({'message': p}).encode('utf-8')
    req = urllib.request.Request(url, data, headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode('utf-8')
            results.append({'prompt': p, 'status': r.getcode(), 'response': text})
    except Exception as e:
        results.append({'prompt': p, 'error': str(e)})

print(json.dumps(results, indent=2))
