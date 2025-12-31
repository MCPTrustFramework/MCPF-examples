"""
Healthcare Diagnostic Chain

Demonstrates:
- Primary care AI delegating to specialist
- Privacy-preserving data access
- Approval workflows
- Medical credential verification
"""

import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from mcpf import MCPF

@dataclass
class PatientData:
    patient_id: str
    imaging_type: str
    images: List[str]
    symptoms: List[str]
    medical_history: Dict[str, Any]
    privacy_level: str  # 'standard' | 'sensitive'

@dataclass
class DiagnosticResult:
    patient_id: str
    primary_care_did: str
    specialist_did: str
    policy_id: str
    requires_approval: bool
    diagnosis: Dict[str, Any]
    confidence: float
    timestamp: str

async def diagnostic_workflow(patient_data: PatientData) -> DiagnosticResult:
    """Execute diagnostic workflow with MCPF verification"""
    
    print(f"🏥 Analyzing patient {patient_data.patient_id}...")
    
    # Initialize MCPF
    mcpf = MCPF(
        ans_url="https://ans.veritrust.vc",
        a2a_url="https://a2a.hospital.example.com"
    )
    
    # Step 1: Resolve agents
    print("1️⃣  Resolving medical agents...")
    primary_care = await mcpf.ans.resolve(
        "primary-diagnostics.hospital.example.agent"
    )
    print(f"   ✓ Primary Care: {primary_care.did}")
    
    radiology_specialist = await mcpf.ans.resolve(
        "radiology-specialist.imaging.hospital.example.agent"
    )
    print(f"   ✓ Radiology Specialist: {radiology_specialist.did}")
    
    # Step 2: Verify medical licenses (credentials)
    print("2️⃣  Verifying medical credentials...")
    primary_valid = await mcpf.did.verify_agent(primary_care.did)
    specialist_valid = await mcpf.did.verify_agent(radiology_specialist.did)
    
    if not (primary_valid and specialist_valid):
        raise Exception("Medical credential verification failed")
    print("   ✓ Medical licenses verified")
    
    # Step 3: Check delegation policy
    print("3️⃣  Checking delegation policy...")
    delegation = await mcpf.a2a.check_delegation(
        from_did=primary_care.did,
        to_did=radiology_specialist.did,
        action="analyze-imaging"
    )
    
    if not delegation.allowed:
        raise Exception(f"Delegation denied: {delegation.reason}")
    
    requires_approval = delegation.policy.constraints.get("requiresApproval", False)
    print(f"   ✓ Delegation allowed (Approval required: {requires_approval})")
    
    # Step 4: Get approval if required
    if requires_approval or patient_data.privacy_level == 'sensitive':
        print("4️⃣  Requesting physician approval...")
        approval = await get_physician_approval(patient_data, delegation.policy)
        if not approval:
            raise Exception("Physician approval denied")
        print("   ✓ Physician approval granted")
    
    # Step 5: Perform specialist analysis
    print("5️⃣  Performing specialist analysis...")
    diagnosis = await analyze_imaging(patient_data)
    
    print(f"   ✓ Diagnosis: {diagnosis['condition']}")
    print(f"   ✓ Confidence: {diagnosis['confidence']:.2f}")
    
    return DiagnosticResult(
        patient_id=patient_data.patient_id,
        primary_care_did=primary_care.did,
        specialist_did=radiology_specialist.did,
        policy_id=delegation.policy.id,
        requires_approval=requires_approval,
        diagnosis=diagnosis,
        confidence=diagnosis['confidence'],
        timestamp=asyncio.get_event_loop().time()
    )

async def get_physician_approval(
    patient_data: PatientData,
    policy: Any
) -> bool:
    """Simulate physician approval workflow"""
    # In production, this would:
    # 1. Send notification to physician
    # 2. Display patient data securely
    # 3. Wait for approval decision
    # 4. Log approval in audit trail
    
    print("   → Notifying supervising physician...")
    await asyncio.sleep(0.1)  # Simulate approval time
    print("   → Physician reviewed case")
    
    # Auto-approve for demo
    return True

async def analyze_imaging(patient_data: PatientData) -> Dict[str, Any]:
    """Simulate specialist imaging analysis"""
    # In production, this would call actual specialist AI
    
    await asyncio.sleep(0.2)  # Simulate analysis time
    
    # Simulated diagnosis based on symptoms
    if 'chest_pain' in patient_data.symptoms:
        return {
            'condition': 'Possible cardiac abnormality',
            'confidence': 0.78,
            'recommendations': [
                'Further cardiac evaluation recommended',
                'ECG and stress test suggested'
            ],
            'imaging_findings': 'Mild cardiac enlargement observed'
        }
    else:
        return {
            'condition': 'Normal findings',
            'confidence': 0.92,
            'recommendations': ['No further action needed'],
            'imaging_findings': 'No abnormalities detected'
        }

# Example usage
async def main():
    example_patient = PatientData(
        patient_id="patient_12345",
        imaging_type="chest_xray",
        images=["xray_001.dcm", "xray_002.dcm"],
        symptoms=["chest_pain", "shortness_of_breath"],
        medical_history={
            "age": 55,
            "conditions": ["hypertension"],
            "medications": ["lisinopril"]
        },
        privacy_level="sensitive"
    )
    
    try:
        result = await diagnostic_workflow(example_patient)
        
        print("\n✅ Diagnostic Workflow Complete:")
        print(f"   Patient: {result.patient_id}")
        print(f"   Diagnosis: {result.diagnosis['condition']}")
        print(f"   Confidence: {result.confidence:.2%}")
        print(f"   Policy ID: {result.policy_id}")
        print(f"   Approval Required: {result.requires_approval}")
        
    except Exception as error:
        print(f"\n❌ Diagnostic Workflow Failed: {error}")

if __name__ == "__main__":
    asyncio.run(main())
