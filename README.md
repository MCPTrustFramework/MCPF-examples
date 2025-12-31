# MCPF Examples

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCPF](https://img.shields.io/badge/MCPF-Examples-brightgreen.svg)](https://mcpf.dev)

**Real-world examples of MCPF Trust Framework** - Complete, working implementations across banking, healthcare, customer service, and supply chain domains.

## 🌟 What is MCPF-examples?

This repository contains production-ready examples demonstrating how to use the MCPF Trust Framework in real-world scenarios:

```
Banking Fraud Detection
    ↓
Fraud Detector Agent
    ↓ (verify credentials via MCPF-did-vc)
    ↓ (resolve via MCPF-ans)
    ↓ (check delegation via MCPF-a2a)
Risk Analyzer Agent
    ↓
Risk Assessment Result
```

## 📚 Examples by Domain

### 🏦 Banking & Finance
- **Fraud Detection Chain** - Multi-agent fraud analysis with delegation
- **Transaction Risk Scoring** - Real-time risk assessment pipeline
- **AML Compliance** - Anti-money laundering agent coordination
- **Credit Decision** - Distributed credit approval workflow

### 🏥 Healthcare
- **Diagnostic Agent Chain** - Primary care → Specialist escalation
- **Patient Record Access** - Privacy-preserving medical data sharing
- **Prescription Verification** - Multi-party prescription validation
- **Clinical Trial Coordination** - Research agent collaboration

### 💬 Customer Service
- **L1 to Supervisor Escalation** - Automated ticket routing
- **Chatbot Federation** - Multi-bot problem resolution
- **Knowledge Base Sharing** - Cross-agent information access
- **Sentiment Analysis Pipeline** - Multi-stage customer analysis

### 📦 Supply Chain
- **Shipment Tracking** - Multi-party logistics coordination
- **Quality Control** - Distributed inspection workflow
- **Vendor Verification** - Supplier credential validation
- **Customs Clearance** - Cross-border agent collaboration

### 🔄 Cross-Domain
- **Multi-Organization Workflow** - Bank + Hospital + Insurance
- **Regulatory Compliance** - Multi-jurisdiction agent coordination
- **Emergency Response** - Cross-sector crisis management

## 🚀 Quick Start

### Prerequisites

```bash
# Clone repository
git clone https://github.com/MCPTrustFramework/MCPF-examples.git
cd MCPF-examples

# Install dependencies (Node.js examples)
cd nodejs/fraud-detection
npm install

# Or Python examples
cd python/fraud-detection
pip install -r requirements.txt

# Or TypeScript examples
cd typescript/fraud-detection
npm install
```

### Run an Example

```bash
# Banking fraud detection (Node.js)
cd nodejs/fraud-detection
node index.js

# Healthcare diagnostic chain (Python)
cd python/diagnostic-chain
python main.py

# Customer service escalation (TypeScript)
cd typescript/service-escalation
npm start
```

## 📖 Example Categories

### 1. Complete Workflows
Full end-to-end implementations using all MCPF components.

### 2. Integration Patterns
Specific integration scenarios and best practices.

### 3. Security Scenarios
Advanced security and trust verification examples.

### 4. Performance Optimization
High-throughput and low-latency implementations.

## 🏦 Banking Example: Fraud Detection Chain

**Scenario:** A fraud detection agent needs to delegate to a risk analyzer for complex transactions.

### Architecture

```
┌─────────────────────────┐
│  Transaction Event      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Fraud Detector Agent   │
│  did:web:bank.example   │
│  (MCPF verified)        │
└───────────┬─────────────┘
            │ 1. Check delegation (A2A)
            │ 2. Verify credentials (DID/VC)
            │ 3. Resolve target (ANS)
            ▼
┌─────────────────────────┐
│  Risk Analyzer Agent    │
│  did:web:analytics.bank │
│  (MCPF verified)        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Risk Assessment        │
│  Score + Reasoning      │
└─────────────────────────┘
```

### Implementation (TypeScript)

```typescript
import { MCPF } from 'mcpf-typescript';

async function detectFraud(transaction: Transaction) {
  const mcpf = new MCPF({
    ansUrl: 'https://ans.veritrust.vc',
    a2aUrl: 'https://a2a.bank.example.com'
  });
  
  // 1. Resolve both agents
  const fraudDetector = await mcpf.ans.resolve({
    name: 'fraud-detector.risk.bank.example.agent'
  });
  
  const riskAnalyzer = await mcpf.ans.resolve({
    name: 'risk-analyzer.analytics.bank.example.agent'
  });
  
  // 2. Verify credentials
  const detectorValid = await mcpf.did.verifyAgent(fraudDetector.did);
  const analyzerValid = await mcpf.did.verifyAgent(riskAnalyzer.did);
  
  if (!detectorValid || !analyzerValid) {
    throw new Error('Agent credential verification failed');
  }
  
  // 3. Check delegation permission
  const delegation = await mcpf.a2a!.checkDelegation({
    fromDid: fraudDetector.did,
    toDid: riskAnalyzer.did,
    action: 'analyze-transaction'
  });
  
  if (!delegation.allowed) {
    throw new Error(`Delegation denied: ${delegation.reason}`);
  }
  
  // 4. Execute risk analysis
  const riskScore = await callRiskAnalyzer(
    riskAnalyzer.endpoints.agent,
    transaction
  );
  
  return {
    fraudDetectorDid: fraudDetector.did,
    riskAnalyzerDid: riskAnalyzer.did,
    policyId: delegation.policy?.id,
    riskScore: riskScore,
    decision: riskScore > 0.7 ? 'BLOCK' : 'ALLOW'
  };
}
```

**Full example:** [banking/fraud-detection](./banking/fraud-detection/)

## 🏥 Healthcare Example: Diagnostic Chain

**Scenario:** Primary care AI delegates to specialist AI for complex cases.

### Implementation (Python)

```python
from mcpf import MCPF

async def diagnostic_workflow(patient_data):
    mcpf = MCPF(
        ans_url="https://ans.veritrust.vc",
        a2a_url="https://a2a.hospital.example.com"
    )
    
    # Resolve agents
    primary_care = await mcpf.ans.resolve(
        "primary-diagnostics.hospital.example.agent"
    )
    
    radiology_specialist = await mcpf.ans.resolve(
        "radiology-specialist.imaging.hospital.example.agent"
    )
    
    # Verify both agents
    primary_valid = await mcpf.did.verify_agent(primary_care.did)
    specialist_valid = await mcpf.did.verify_agent(radiology_specialist.did)
    
    if not (primary_valid and specialist_valid):
        raise Exception("Agent verification failed")
    
    # Check delegation (requires approval for sensitive medical data)
    delegation = await mcpf.a2a.check_delegation(
        from_did=primary_care.did,
        to_did=radiology_specialist.did,
        action="analyze-imaging"
    )
    
    if not delegation.allowed:
        raise Exception(f"Delegation denied: {delegation.reason}")
    
    # Check if approval required
    if delegation.policy.constraints.get("requiresApproval"):
        # Get human approval
        approval = await get_physician_approval(patient_data)
        if not approval:
            raise Exception("Physician approval denied")
    
    # Execute specialist analysis
    diagnosis = await call_specialist(
        radiology_specialist.endpoints.agent,
        patient_data
    )
    
    return {
        "primary_care_did": primary_care.did,
        "specialist_did": radiology_specialist.did,
        "policy_id": delegation.policy.id,
        "requires_approval": delegation.policy.constraints.get("requiresApproval"),
        "diagnosis": diagnosis
    }
```

**Full example:** [healthcare/diagnostic-chain](./healthcare/diagnostic-chain/)

## 💬 Customer Service Example: Escalation

**Scenario:** L1 chatbot escalates to supervisor AI when needed.

### Implementation (Node.js)

```javascript
const { MCPF } = require('mcpf-typescript');

async function handleCustomerQuery(query) {
  const mcpf = new MCPF({
    ansUrl: 'https://ans.veritrust.vc',
    a2aUrl: 'https://a2a.company.example.com'
  });
  
  // Resolve agents
  const chatbotL1 = await mcpf.ans.resolve({
    name: 'chatbot-l1.support.company.example.agent'
  });
  
  const supervisorAI = await mcpf.ans.resolve({
    name: 'supervisor-ai.management.company.example.agent'
  });
  
  // Verify credentials
  const l1Valid = await mcpf.did.verifyAgent(chatbotL1.did);
  const supervisorValid = await mcpf.did.verifyAgent(supervisorAI.did);
  
  if (!l1Valid || !supervisorValid) {
    throw new Error('Agent verification failed');
  }
  
  // Attempt L1 resolution
  const l1Response = await queryL1Chatbot(chatbotL1.endpoints.agent, query);
  
  // Check if escalation needed
  if (l1Response.confidence < 0.8 || query.severity === 'high') {
    // Check delegation
    const delegation = await mcpf.a2a.checkDelegation({
      fromDid: chatbotL1.did,
      toDid: supervisorAI.did,
      action: 'escalate'
    });
    
    if (!delegation.allowed) {
      return {
        status: 'escalation_denied',
        reason: delegation.reason,
        l1Response: l1Response
      };
    }
    
    // Check constraints
    const { constraints } = delegation.policy;
    if (constraints.minimumSeverity && 
        query.severity < constraints.minimumSeverity) {
      return {
        status: 'below_threshold',
        l1Response: l1Response
      };
    }
    
    // Escalate to supervisor
    const supervisorResponse = await querySupervisor(
      supervisorAI.endpoints.agent,
      query,
      l1Response
    );
    
    return {
      status: 'escalated',
      l1Did: chatbotL1.did,
      supervisorDid: supervisorAI.did,
      policyId: delegation.policy.id,
      response: supervisorResponse
    };
  }
  
  return {
    status: 'resolved_l1',
    response: l1Response
  };
}
```

**Full example:** [customer-service/escalation](./customer-service/escalation/)

## 📊 All Examples

### By Language

| Language | Examples | Status |
|----------|----------|--------|
| TypeScript | 8 | ✅ Complete |
| Python | 8 | ✅ Complete |
| Node.js | 8 | ✅ Complete |

### By Domain

| Domain | Examples | Use Cases |
|--------|----------|-----------|
| Banking | 4 | Fraud, AML, Credit, Risk |
| Healthcare | 4 | Diagnostics, Records, Rx, Trials |
| Customer Service | 3 | Escalation, Federation, Sentiment |
| Supply Chain | 4 | Tracking, QC, Vendor, Customs |
| Cross-Domain | 3 | Multi-org, Compliance, Emergency |

## 🧪 Testing Examples

Each example includes:
- ✅ Complete working code
- ✅ Test data / fixtures
- ✅ README with setup instructions
- ✅ Integration tests
- ✅ Performance benchmarks

```bash
# Run all tests
npm test

# Run specific domain
npm run test:banking
npm run test:healthcare

# Run integration tests
npm run test:integration

# Benchmark
npm run benchmark
```

## 📝 Documentation

Each example includes:

1. **README.md** - Overview, setup, usage
2. **ARCHITECTURE.md** - System design and flow
3. **DEPLOYMENT.md** - Production deployment guide
4. **SECURITY.md** - Security considerations
5. **API.md** - API reference

## 🔧 Configuration

Examples support multiple environments:

```bash
# Development
cp .env.example .env.development
npm run dev

# Staging
cp .env.example .env.staging
npm run staging

# Production
cp .env.example .env.production
npm start
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Adding new examples
- Improving existing examples
- Testing guidelines
- Documentation standards

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 📞 Contact

- **Website:** https://mcpf.dev
- **GitHub:** https://github.com/MCPTrustFramework/MCPF-examples
- **Issues:** https://github.com/MCPTrustFramework/MCPF-examples/issues
- **Discussions:** https://github.com/MCPTrustFramework/MCPF-examples/discussions

## 🔗 Related Projects

- [MCPF-specification](https://github.com/MCPTrustFramework/MCPF-specification) - SSOT
- [MCPF-python](https://github.com/MCPTrustFramework/MCPF-python) - Python SDK
- [MCPF-typescript](https://github.com/MCPTrustFramework/MCPF-typescript) - TypeScript SDK
- [MCPF-ans](https://github.com/MCPTrustFramework/MCPF-ans) - Agent Name Service
- [MCPF-registry](https://github.com/MCPTrustFramework/MCPF-registry) - MCP Trust Registry
- [MCPF-a2a-registry](https://github.com/MCPTrustFramework/MCPF-a2a-registry) - A2A delegation

---

**Version:** 1.0.0-alpha  
**Last Updated:** December 31, 2025  
**Examples:** 24 complete implementations  
**Status:** Production-ready
