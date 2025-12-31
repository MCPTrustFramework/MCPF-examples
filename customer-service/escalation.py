#!/usr/bin/env python3
"""
Customer Service Escalation Example

Demonstrates:
- Multi-tier support agents
- Automatic escalation policies
- Context preservation
- Performance tracking
"""

import asyncio
from mcpf import MCPF


async def main():
    print("👥 Customer Service Escalation Example\n")
    
    mcpf = MCPF(
        ans_url="https://ans.veritrust.vc",
        a2a_url="https://a2a.company.example"
    )
    
    # Customer query
    query = {
        "id": "ticket_789",
        "customer": "premium-customer-001",
        "question": "Why was my payment declined?",
        "complexity": "medium"
    }
    
    print("1️⃣  Customer query received...")
    print(f"   Ticket: {query['id']}")
    print(f"   Question: {query['question']}")
    
    print("\n2️⃣  Resolving L1 chatbot agent...")
    l1_chatbot = await mcpf.ans.resolve(
        "chatbot-l1.support.company.example.agent"
    )
    print(f"   ✓ {l1_chatbot.name}")
    
    print("\n3️⃣  L1 attempting to resolve...")
    can_resolve = attempt_resolution(query, level=1)
    
    if not can_resolve:
        print("   ✗ L1 cannot resolve - escalating to L2")
        
        l2_supervisor = await mcpf.ans.resolve(
            "supervisor-l2.support.company.example.agent"
        )
        
        delegation = await mcpf.a2a.check_delegation(
            from_did=l1_chatbot.did,
            to_did=l2_supervisor.did,
            action="escalate"
        )
        
        if delegation.allowed:
            print(f"\n4️⃣  Escalation to L2 allowed")
            print(f"   ✓ Delegating to: {l2_supervisor.name}")
            
            can_resolve_l2 = attempt_resolution(query, level=2)
            if can_resolve_l2:
                print("   ✓ L2 resolved the issue")
            else:
                print("   Note: Would escalate to L3 specialist")
        else:
            print(f"   ✗ Escalation denied: {delegation.reason}")
    else:
        print("   ✓ L1 resolved the issue")
    
    print("\n✅ Workflow complete!")


def attempt_resolution(query, level):
    """Simulate resolution attempt"""
    if query['complexity'] == 'low' and level >= 1:
        return True
    elif query['complexity'] == 'medium' and level >= 2:
        return True
    elif query['complexity'] == 'high' and level >= 3:
        return True
    return False


if __name__ == "__main__":
    asyncio.run(main())
