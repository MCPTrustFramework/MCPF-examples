#!/usr/bin/env python3
"""
Banking Fraud Detection Example

Demonstrates:
- ANS name resolution
- DID/VC verification
- A2A delegation
- Multi-level analysis
"""

import asyncio
from mcpf import MCPF


async def main():
    print("🏦 Banking Fraud Detection Example\n")
    
    # Initialize MCPF
    mcpf = MCPF(
        ans_url="https://ans.veritrust.vc",
        a2a_url="https://a2a.dbs.example"
    )
    
    # Simulate transaction
    transaction = {
        "id": "txn_12345",
        "amount": 15000.00,
        "currency": "USD",
        "merchant": "Online Electronics Store",
        "location": "Foreign Country",
        "time": "2025-12-31T14:30:00Z"
    }
    
    # 1. Resolve fraud detector agent
    print("1️⃣  Resolving fraud detector agent...")
    fraud_detector = await mcpf.ans.resolve(
        "fraud-detector.risk.dbs.example.agent"
    )
    print(f"   ✓ {fraud_detector.name}")
    print(f"     DID: {fraud_detector.did}")
    
    # 2. Verify fraud detector credentials
    print("\n2️⃣  Verifying credentials...")
    detector_valid = await mcpf.did.verify_agent(fraud_detector.did)
    print(f"   ✓ Fraud detector credential: {'Valid' if detector_valid else 'Invalid'}")
    
    # 3. Analyze transaction (Level 1)
    print("\n3️⃣  Analyzing transaction (Level 1)...")
    risk_score = analyze_transaction(transaction)
    print(f"   Transaction: {transaction['id']}")
    print(f"   Amount: ${transaction['amount']:,.2f}")
    print(f"   Risk Score: {risk_score} ({'HIGH' if risk_score > 0.7 else 'LOW'})")
    
    # 4. If high risk, delegate to risk analyzer
    if risk_score > 0.7:
        print("\n4️⃣  High risk detected - checking delegation...")
        
        # Resolve risk analyzer
        risk_analyzer = await mcpf.ans.resolve(
            "risk-analyzer.analytics.dbs.example.agent"
        )
        print(f"   ✓ Risk analyzer: {risk_analyzer.name}")
        
        # Check delegation permission
        delegation = await mcpf.a2a.check_delegation(
            from_did=fraud_detector.did,
            to_did=risk_analyzer.did,
            action="analyze"
        )
        
        if delegation.allowed:
            print(f"   ✓ Delegation allowed")
            print(f"     Policy ID: {delegation.policy.id}")
            print(f"     Max Duration: {delegation.policy.constraints.get('maxDuration')}s")
            
            # Delegate analysis
            print("\n5️⃣  Delegating to risk analyzer...")
            final_score = perform_deep_analysis(transaction, risk_score)
            print(f"   ✓ Deep analysis complete")
            print(f"     Final Risk Score: {final_score}")
            print(f"     Recommendation: {'BLOCK' if final_score > 0.9 else 'REVIEW'}")
        else:
            print(f"   ✗ Delegation denied: {delegation.reason}")
    else:
        print("\n4️⃣  Low risk - transaction approved")
    
    print("\n✅ Workflow complete!")


def analyze_transaction(txn):
    """Simulate Level 1 fraud analysis"""
    # Simple rule-based scoring
    score = 0.0
    
    if txn['amount'] > 10000:
        score += 0.4
    if 'Foreign' in txn['location']:
        score += 0.3
    if 'Online' in txn['merchant']:
        score += 0.2
    
    return min(score, 1.0)


def perform_deep_analysis(txn, initial_score):
    """Simulate Level 2 deep analysis"""
    # Advanced ML-based scoring
    final_score = initial_score + 0.1  # Simulated increase
    return min(final_score, 1.0)


if __name__ == "__main__":
    asyncio.run(main())
