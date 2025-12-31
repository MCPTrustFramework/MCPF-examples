#!/usr/bin/env python3
"""
Complete MCPF Workflow Example

Demonstrates all MCPF components working together.
"""

import asyncio
from mcpf import MCPF


async def main():
    print("🚀 Complete MCPF Workflow\n")
    
    mcpf = MCPF(
        ans_url="https://ans.veritrust.vc",
        registry_url="https://ans.veritrust.vc/mcp",
        a2a_url="https://a2a.example.com"
    )
    
    # 1. ANS - Resolve agent names
    print("1️⃣  ANS: Resolving agent names...")
    agent = await mcpf.ans.resolve(
        "fraud-detector.risk.bank.example.agent"
    )
    print(f"   ✓ {agent.name} → {agent.did}")
    
    # 2. DID/VC - Verify credentials
    print("\n2️⃣  DID/VC: Verifying credentials...")
    valid = await mcpf.did.verify_agent(agent.did)
    print(f"   ✓ Credential valid: {valid}")
    
    # 3. Registry - Find MCP servers
    print("\n3️⃣  Registry: Searching for weather servers...")
    servers = await mcpf.registry.search(capability="getCurrentWeather")
    print(f"   ✓ Found {len(servers.items)} servers")
    
    # 4. A2A - Check delegation
    if mcpf.a2a:
        print("\n4️⃣  A2A: Checking delegation permission...")
        delegation = await mcpf.a2a.check_delegation(
            from_did=agent.did,
            to_did="did:web:analyzer.example",
            action="analyze"
        )
        print(f"   ✓ Delegation allowed: {delegation.allowed}")
    
    print("\n✅ All components working!")


if __name__ == "__main__":
    asyncio.run(main())
