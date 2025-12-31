# Healthcare Examples

## Diagnostic Imaging

AI-assisted diagnostic workflow with specialist review.

### Setup

```bash
pip install mcpf-python
python diagnostic-imaging.py
```

### HIPAA Compliance

- All delegations logged in audit trail
- Requires specialist approval for abnormalities
- Time-based access (business hours only)
- Encrypted data transmission (constraint)

### A2A Policy Constraints

- Requires approval: `true`
- Allowed days: Mon-Fri
- Allowed hours: 8AM-5PM
- Minimum certification: board-certified-radiologist
- Encryption required: `true`
