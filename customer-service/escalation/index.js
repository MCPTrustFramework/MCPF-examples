/**
 * Customer Service Escalation
 * L1 Chatbot → Supervisor AI delegation
 */

const { MCPF } = require('mcpf-typescript');

async function handleCustomerQuery(query) {
  console.log(`💬 Handling query: "${query.message}"`);
  
  const mcpf = new MCPF({
    ansUrl: process.env.MCPF_ANS_URL || 'https://ans.veritrust.vc',
    a2aUrl: process.env.MCPF_A2A_URL || 'https://a2a.company.example.com'
  });
  
  // Resolve agents
  const chatbotL1 = await mcpf.ans.resolve({
    name: 'chatbot-l1.support.company.example.agent'
  });
  
  const supervisorAI = await mcpf.ans.resolve({
    name: 'supervisor-ai.management.company.example.agent'
  });
  
  // Attempt L1 resolution
  const l1Response = await simulateL1Response(query);
  
  // Check if escalation needed
  if (l1Response.confidence < 0.8 || query.severity === 'high') {
    console.log('   → Escalating to supervisor...');
    
    const delegation = await mcpf.a2a.checkDelegation({
      fromDid: chatbotL1.did,
      toDid: supervisorAI.did,
      action: 'escalate'
    });
    
    if (delegation.allowed) {
      const supervisorResponse = await simulateSupervisorResponse(query);
      return {
        status: 'escalated',
        response: supervisorResponse,
        policyId: delegation.policy.id
      };
    }
  }
  
  return { status: 'resolved_l1', response: l1Response };
}

function simulateL1Response(query) {
  return {
    message: 'I can help with that!',
    confidence: query.severity === 'high' ? 0.5 : 0.9
  };
}

function simulateSupervisorResponse(query) {
  return {
    message: 'Supervisor: I\'ll handle this personally.',
    confidence: 0.95
  };
}

// Example
const query = {
  customerId: 'cust_123',
  message: 'My account was charged twice',
  severity: 'high'
};

handleCustomerQuery(query).then(console.log);
