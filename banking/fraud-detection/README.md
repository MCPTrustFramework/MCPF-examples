# Banking Fraud Detection Chain

Multi-agent fraud detection using MCPF Trust Framework.

## Architecture

```
Transaction → Fraud Detector → (verify + delegate) → Risk Analyzer → Decision
```

## Setup

```bash
npm install
cp .env.example .env
# Edit .env with your MCPF endpoints
```

## Run

```bash
npm start
```

## Output

```json
{
  "transactionId": "tx_abc123",
  "fraudDetectorDid": "did:web:bank.example:fraud-detector",
  "riskAnalyzerDid": "did:web:analytics.bank.example:risk-analyzer",
  "policyId": "pol_xyz",
  "riskScore": 0.65,
  "decision": "REVIEW",
  "reasoning": ["High transaction amount"],
  "timestamp": "2025-12-31T10:00:00Z"
}
```
