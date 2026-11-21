# LND Cloud Platform Guide

Professional technical documentation for deploying and operating Lightning Network Daemon (LND) on AWS, GCP, and Azure.

## Documentation Structure — Category-First, Then Cloud

```
docs/
├── 01-cloud-architecture/          # Per-cloud architecture (START HERE)
│   ├── 01-cloud-overview.md        # Cloud basics, service models, global infrastructure, HA
│   ├── 02-prerequisites.md         # Free trials (AWS/GCP/Azure), required knowledge, CLI setup
│   ├── 03-service-mapping.md       # Service mapping across clouds
│   ├── 04-architecture-comparison.md # CSPM, M365 vs Workspace, Governance, Compliance
│   └── 02-resource-hierarchy.md    # Azure (Entra→Mgmt→Sub→RG), GCP (Workspace→Org→Folder→Proj), AWS (Mgmt→OU→Acct)
├── 02-networking/                  # Networking category (by function, then cloud)
│   ├── 00-index.md                 # Reading order
│   ├── 01-backbone.md              # Global fiber, subsea cables, network tiers, private connectivity, latency
│   ├── 02-network-security.md      # VPN, SD-WAN, MPLS, peering, PrivateLink/PSC/Private Endpoint
│   ├── 03-network-components.md    # Router, Switch, NAT, Shared VPC
│   ├── 04-dns.md                   # Route 53, Cloud DNS, Azure DNS
│   ├── 05-load-balancing.md        # L4/L7, global anycast, TLS termination, WAF integration
│   └── 06-vpc-peering.md           # VPC peering, PrivateLink/PSC/Private Endpoint
├── 03-iam/                         # IAM category (by governance level, then cloud)
│   ├── 00-index.md                 # Reading order
│   ├── 01-iam-at-levels.md         # IAM at EACH layer: Entra ID vs Azure RBAC, Cloud Identity vs Org/Folder/Proj
│   ├── 02-aws.md                   # AWS IAM: Core, Identity Center, SAML/OIDC, STS, IRSA
│   ├── 03-gcp.md                   # GCP IAM: Cloud Identity, WIF (workforce/workload), Service Accounts
│   └── 04-azure.md                 # Azure IAM: Entra ID vs Azure RBAC, Enterprise Apps vs App Regs, Conditional Access
├── 04-security/                    # Security category (by function)
│   ├── 00-index.md                 # Reading order
│   └── 01-security-services.md     # DDoS, WAF, NGFW, Bastion/IAP, CSPM, vendors (Palo Alto, Fortinet, Check Point)
├── 05-compute/                     # Compute category
│   └── 00-index.md                 # VM, K8s, Serverless (content in service-mapping & deployment)
├── 06-storage/                     # Storage category
│   └── 00-index.md                 # Block, Object, File, Backup/DR
├── 07-billing/                     # Billing category
│   ├── 00-index.md                 # Reading order
│   └── 01-data-transfer-costs.md   # Egress/ingress, cross-zone/region, inter-cloud, bucket/log costs
├── 08-deployment/                  # Deployment patterns & tutorials
│   ├── 00-index.md                 # Reading order
│   ├── 01-patterns.md              # Standalone, HA, K8s, Serverless, Multi-cloud
│   ├── 02-aws.md                   # EC2 + EBS + NLB tutorial
│   ├── 03-gcp.md                   # Compute Engine + PD + ILB tutorial
│   └── 04-azure.md                 # VM + Managed Disks + LB tutorial
├── 09-identity-fundamentals/       # SAML/OIDC fundamentals
│   ├── 00-index.md                 # Reading order
│   └── 01-saml-oidc.md             # SAML 2.0/OIDC architecture, flows, certs, tokens, mapping
├── 10-cross-cutting/               # Federation, compliance, cost optimization
│   ├── 00-index.md                 # Reading order
│   └── 01-federation-patterns.md   # Cross-cloud workforce/workload federation, Patterns A/B/C
└── 11-reference/                   # Reference
    ├── 00-index.md                 # Reading order
    └── 01-cli-cheatsheet.md        # Unified AWS/GCP/Azure CLI
```

## Cross-Reference System

Documents use standardized notation:
- `[§XX.Y]` — Section reference (e.g., `[§02.1]` → Backbone Network)
- `[Figure N]` — Diagram reference
- `[Table N]` — Table reference
- `[Listing N]` — Code listing reference

## Running Example

All guides use a consistent **Acme Corp** scenario:
- **Primary IdP**: Microsoft Entra ID
- **User**: Alice (`alice@acmecorp.com`) → accesses GCP/AWS/Azure consoles
- **Workload**: `collector.py` on Azure VM (Managed Identity) → writes to GCS bucket

## Quick Start

```bash
# Clone and serve locally
git clone https://github.com/ajettesla/cloud-plaform-lnd-guide
cd cloud-plaform-lnd-guide
# No Python dependencies needed — pure markdown documentation
```

## Recommended Reading Order

| Phase | Section | Start With |
|-------|---------|------------|
| **1. Cloud Basics** | 01-cloud-architecture | 01-cloud-overview → 02-prerequisites |
| **2. Category Deep Dives** | 02-networking → 03-iam → 04-security → 05-compute → 06-storage → 07-billing | Each category's 00-index.md |
| **3. Identity Fundamentals** | 09-identity-fundamentals | 01-saml-oidc.md |
| **4. Cloud-Specific IAM** | 03-iam | 02-aws → 03-gcp → 04-azure |
| **5. Deployment** | 08-deployment | 01-patterns → tutorials |
| **6. Cross-Cutting** | 10-cross-cutting | 01-federation-patterns.md |

## License

CC BY-SA 4.0 — see individual documents for citations.