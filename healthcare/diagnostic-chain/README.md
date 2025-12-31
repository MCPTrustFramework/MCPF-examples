# Healthcare Diagnostic Chain

Multi-agent diagnostic workflow with privacy controls.

## Features

- Medical credential verification
- Privacy-preserving data access
- Physician approval workflows
- Specialist delegation

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Flow

1. Resolve primary care and specialist agents
2. Verify medical licenses (credentials)
3. Check delegation policy
4. Get physician approval (if required)
5. Perform specialist analysis
6. Return diagnosis with audit trail
