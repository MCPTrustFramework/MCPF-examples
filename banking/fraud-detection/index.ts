/**
 * Banking Fraud Detection Chain
 * 
 * Demonstrates:
 * - Agent credential verification
 * - ANS name resolution
 * - A2A delegation checking
 * - Multi-agent workflow
 */

import { MCPF } from 'mcpf-typescript';

interface Transaction {
  id: string;
  amount: number;
  currency: string;
  from: string;
  to: string;
  timestamp: string;
  metadata: Record<string, any>;
}

interface FraudDetectionResult {
  transactionId: string;
  fraudDetectorDid: string;
  riskAnalyzerDid: string;
  policyId: string;
  riskScore: number;
  decision: 'ALLOW' | 'BLOCK' | 'REVIEW';
  reasoning: string[];
  timestamp: string;
}

export async function detectFraud(transaction: Transaction): Promise<FraudDetectionResult> {
  console.log(`🔍 Analyzing transaction ${transaction.id}...`);
  
  // Initialize MCPF
  const mcpf = new MCPF({
    ansUrl: process.env.MCPF_ANS_URL || 'https://ans.veritrust.vc',
    registryUrl: process.env.MCPF_REGISTRY_URL || 'https://ans.veritrust.vc/mcp',
    a2aUrl: process.env.MCPF_A2A_URL || 'https://a2a.bank.example.com'
  });
  
  // Step 1: Resolve agents via ANS
  console.log('1️⃣  Resolving agents...');
  const fraudDetector = await mcpf.ans.resolve({
    name: 'fraud-detector.risk.bank.example.agent'
  });
  console.log(`   ✓ Fraud Detector: ${fraudDetector.did}`);
  
  const riskAnalyzer = await mcpf.ans.resolve({
    name: 'risk-analyzer.analytics.bank.example.agent'
  });
  console.log(`   ✓ Risk Analyzer: ${riskAnalyzer.did}`);
  
  // Step 2: Verify agent credentials
  console.log('2️⃣  Verifying credentials...');
  const detectorValid = await mcpf.did.verifyAgent(fraudDetector.did);
  const analyzerValid = await mcpf.did.verifyAgent(riskAnalyzer.did);
  
  if (!detectorValid || !analyzerValid) {
    throw new Error('Agent credential verification failed');
  }
  console.log('   ✓ All credentials verified');
  
  // Step 3: Check delegation permission
  console.log('3️⃣  Checking delegation permission...');
  const delegation = await mcpf.a2a!.checkDelegation({
    fromDid: fraudDetector.did,
    toDid: riskAnalyzer.did,
    action: 'analyze-transaction'
  });
  
  if (!delegation.allowed) {
    throw new Error(`Delegation denied: ${delegation.reason}`);
  }
  console.log(`   ✓ Delegation allowed (Policy: ${delegation.policy?.id})`);
  
  // Step 4: Perform risk analysis
  console.log('4️⃣  Performing risk analysis...');
  const riskScore = calculateRiskScore(transaction);
  const reasoning = generateReasoning(transaction, riskScore);
  
  const decision = riskScore > 0.8 ? 'BLOCK' 
                 : riskScore > 0.5 ? 'REVIEW' 
                 : 'ALLOW';
  
  console.log(`   ✓ Risk Score: ${riskScore.toFixed(2)}`);
  console.log(`   ✓ Decision: ${decision}`);
  
  return {
    transactionId: transaction.id,
    fraudDetectorDid: fraudDetector.did,
    riskAnalyzerDid: riskAnalyzer.did,
    policyId: delegation.policy!.id,
    riskScore,
    decision,
    reasoning,
    timestamp: new Date().toISOString()
  };
}

function calculateRiskScore(tx: Transaction): number {
  let score = 0;
  
  // Amount-based risk
  if (tx.amount > 10000) score += 0.3;
  if (tx.amount > 50000) score += 0.2;
  
  // Velocity check (simulated)
  const recentTxCount = tx.metadata.recentTxCount || 0;
  if (recentTxCount > 5) score += 0.2;
  
  // Geographic risk (simulated)
  const isHighRiskCountry = tx.metadata.toCountry === 'XX';
  if (isHighRiskCountry) score += 0.3;
  
  return Math.min(score, 1.0);
}

function generateReasoning(tx: Transaction, score: number): string[] {
  const reasons: string[] = [];
  
  if (tx.amount > 10000) {
    reasons.push('High transaction amount');
  }
  if (tx.metadata.recentTxCount > 5) {
    reasons.push('High transaction velocity');
  }
  if (tx.metadata.toCountry === 'XX') {
    reasons.push('High-risk destination country');
  }
  if (score < 0.3) {
    reasons.push('Normal transaction pattern');
  }
  
  return reasons;
}

// Example usage
if (require.main === module) {
  const exampleTransaction: Transaction = {
    id: 'tx_' + Math.random().toString(36).substr(2, 9),
    amount: 15000,
    currency: 'USD',
    from: 'account_12345',
    to: 'account_67890',
    timestamp: new Date().toISOString(),
    metadata: {
      recentTxCount: 3,
      toCountry: 'US'
    }
  };
  
  detectFraud(exampleTransaction)
    .then(result => {
      console.log('\n✅ Fraud Detection Complete:');
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(error => {
      console.error('\n❌ Fraud Detection Failed:', error.message);
      process.exit(1);
    });
}
