/**
 * Complete MCPF Workflow Example
 * 
 * Demonstrates all MCPF components working together.
 */

import { MCPF } from 'mcpf-typescript';

async function main() {
  console.log('🚀 Complete MCPF Workflow\n');
  
  const mcpf = new MCPF({
    ansUrl: 'https://ans.veritrust.vc',
    registryUrl: 'https://ans.veritrust.vc/mcp',
    a2aUrl: 'https://a2a.example.com'
  });
  
  // 1. ANS - Resolve agent names
  console.log('1️⃣  ANS: Resolving agent names...');
  const agent = await mcpf.ans.resolve({
    name: 'fraud-detector.risk.bank.example.agent'
  });
  console.log(`   ✓ ${agent.name} → ${agent.did}`);
  
  // 2. DID/VC - Verify credentials
  console.log('\n2️⃣  DID/VC: Verifying credentials...');
  const valid = await mcpf.did.verifyAgent(agent.did);
  console.log(`   ✓ Credential valid: ${valid}`);
  
  // 3. Registry - Find MCP servers
  console.log('\n3️⃣  Registry: Searching for weather servers...');
  const servers = await mcpf.registry.search({
    capability: 'getCurrentWeather'
  });
  console.log(`   ✓ Found ${servers.items.length} servers`);
  
  // 4. A2A - Check delegation
  if (mcpf.a2a) {
    console.log('\n4️⃣  A2A: Checking delegation permission...');
    const delegation = await mcpf.a2a.checkDelegation({
      fromDid: agent.did,
      toDid: 'did:web:analyzer.example',
      action: 'analyze'
    });
    console.log(`   ✓ Delegation allowed: ${delegation.allowed}`);
  }
  
  console.log('\n✅ All components working!');
}

main().catch(console.error);
