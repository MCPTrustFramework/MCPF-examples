# Banking Examples

## Fraud Detection

Multi-level fraud detection with delegation.

### Setup

```bash
pip install mcpf-python
python fraud-detection.py
```

### Architecture

```
Transaction → Fraud Detector (L1) → Risk Analyzer (L2) → Decision
```

### A2A Policy

The fraud detector can delegate to risk analyzer with these constraints:
- Max duration: 3600 seconds
- Scope: transaction-data only
- No approval required
- Max 10 concurrent delegations
