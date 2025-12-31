#!/usr/bin/env python3
"""
Healthcare Diagnostic Imaging Example

Demonstrates:
- Healthcare-specific A2A policies
- Time-based constraints
- Approval requirements
- HIPAA-compliant audit logging
"""

import asyncio
from mcpf import MCPF


async def main():
    print("🏥 Healthcare Diagnostic Imaging Example\n")
    
    mcpf = MCPF(
        ans_url="https://ans.veritrust.vc",
        a2a_url="https://a2a.hospital.example"
    )
    
    # Simulate patient case
    case = {
        "patient_id": "P12345",
        "exam_type": "chest-xray",
        "image_url": "https://hospital.example/images/xray_001.dcm",
        "timestamp": "2025-12-31T09:30:00Z"
    }
    
    print("1️⃣  Resolving diagnostic AI agent...")
    diagnostic_ai = await mcpf.ans.resolve(
        "diagnostic-ai.imaging.hospital.example.agent"
    )
    print(f"   ✓ {diagnostic_ai.name}")
    
    print("\n2️⃣  Analyzing chest X-ray...")
    findings = analyze_image(case)
    print(f"   Findings: {findings['description']}")
    print(f"   Confidence: {findings['confidence']}")
    
    if findings['abnormality_detected']:
        print("\n3️⃣  Abnormality detected - checking specialist delegation...")
        
        specialist = await mcpf.ans.resolve(
            "radiology-specialist.imaging.hospital.example.agent"
        )
        
        delegation = await mcpf.a2a.check_delegation(
            from_did=diagnostic_ai.did,
            to_did=specialist.did,
            action="generate-report"
        )
        
        if delegation.allowed:
            print(f"   ✓ Delegation to specialist allowed")
            print(f"     Note: Requires human approval (constraint)")
            print(f"     Working hours only: Mon-Fri, 8AM-5PM")
            
            print("\n4️⃣  Awaiting specialist review...")
            # In real scenario, wait for human specialist
            print("   ✓ Specialist report generated")
        else:
            print(f"   ✗ Delegation denied: {delegation.reason}")
    else:
        print("\n3️⃣  No abnormalities - routine report generated")
    
    print("\n✅ Workflow complete!")


def analyze_image(case):
    """Simulate AI diagnostic analysis"""
    return {
        "description": "Possible infiltrate in right lower lobe",
        "confidence": 0.85,
        "abnormality_detected": True
    }


if __name__ == "__main__":
    asyncio.run(main())
