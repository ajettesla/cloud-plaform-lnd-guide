# LND Cloud Platform Guide

Professional technical documentation for deploying and operating Lightning Network Daemon (LND) on AWS, GCP, and Azure.

## Documentation Structure

```
docs/
├── 01-getting-started/     # Foundation: overview, prerequisites, cloud comparison, architecture patterns
├── 02-identity-access/     # Identity & Access: SAML/OIDC, GCP/AWS/Azure IAM, cross-cloud federation
├── 11-reference/           # Reference: CLI cheatsheet, service limits, pricing
└── 12-tutorials/           # Tutorials: Step-by-step deployments for each cloud
```

## Cross-Reference System

Documents use standardized notation:
- `[§XX.Y]` — Section reference (e.g., `[§02.4]` → GCP Workforce Federation)
- `[Figure N]` — Diagram reference
- `[Table N]` — Table reference
- `[Listing N]` — Code listing reference

## Running Example

All guides use a consistent **Acme Corp** scenario:
- **Primary IdP**: Microsoft Entra ID
- **User**: Alice (`alice@acmecorp.com`) → accesses GCP/AWS/Azure consoles
- **Workload**: `collector.py` on Azure VM (Managed Identity) → writes to GCS bucket

## Topics Covered

### Identity & Access (02-identity-access)
- **idp-sp-fundamentals.md** — SAML 2.0 / OIDC architecture, flows, attribute mapping
- **gcp-iam.md** — Cloud Identity, Workforce/Workload Identity Federation, service accounts
- **aws-iam.md** — IAM Core, Identity Center, SAML/OIDC, STS, IRSA
- **azure-ad.md** — Enterprise Apps vs App Registrations, Managed Identities, Workload Identity, Conditional Access
- **cross-cloud-federation.md** — Directionality matrix, 6 workforce + 8 workload directions, Patterns A/B/C

### Getting Started (01-getting-started)
- Overview, prerequisites, cloud comparison, architecture patterns

### Reference (11-reference)
- CLI cheatsheet for AWS/GCP/Azure

### Tutorials (12-tutorials)
- AWS EC2 + EBS + NLB deployment
- GCP Compute Engine + Persistent Disk + ILB deployment
- Azure VM + Managed Disks + Load Balancer deployment

## License

CC BY-SA 4.0 — see individual documents for citations.