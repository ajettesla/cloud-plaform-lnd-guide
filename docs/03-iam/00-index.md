---
title: "Identity & Access Management (IAM)"
description: "IAM category — IAM at each governance level, cloud-specific IAM (AWS, GCP, Azure), SAML/OIDC fundamentals"
---

# IAM — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-iam-at-levels.md](01-iam-at-levels.md) | **IAM at each governance layer**: What you configure at Entra ID vs Azure RBAC vs Mgmt Group vs Subscription vs RG. GCP: Cloud Identity vs Org vs Folder vs Project IAM. AWS: IAM Identity Center vs Account IAM vs SCPs. Conditional Access, Entitlement Management, PIM |
| 2 | [02-aws.md](02-aws.md) | **AWS IAM deep dive**: Core model (users, roles, policies, SCPs), IAM Identity Center (SAML+SCIM, Permission Sets, Account Assignments), Direct SAML federation, OIDC federation (GitHub), STS (AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity), IRSA (EKS OIDC provider, pod trust policy, K8s SA annotation), AWS as IdP (Identity Center → GCP) |
| 3 | [03-gcp.md](03-gcp.md) | **GCP IAM deep dive**: Resource hierarchy, Cloud Identity vs Org Resource, IAM model (principals, roles, conditions), Workforce Identity Federation (pools, SAML/OIDC providers, attribute mapping, principal identifiers, sign-in flow), Workload Identity Federation (pools, Azure MI/GitHub/AWS providers, SA impersonation), Service Accounts, monitoring/audit logs |
| 4 | [04-azure.md](04-azure.md) | **Azure IAM deep dive**: Entra ID architecture (two-plane model), **Entra ID vs Azure RBAC separation**, Enterprise Apps (SAML IdP) vs App Registrations (OIDC IdP), SAML config (Entity ID, ACS, RelayState, claims, signing cert), OIDC config, Managed Identities (system/user-assigned, IMDS token), Workload Identity Federation (federated credentials for GitHub/K8s), Entra Workload Identity (AKS), Conditional Access, Entitlement Management, PIM |

**Cross-references**: SAML/OIDC fundamentals in [09-identity-fundamentals](../09-identity-fundamentals/00-index.md), Cloud architecture in [01-cloud-architecture](../01-cloud-architecture/00-index.md), Federation in [10-cross-cutting](../10-cross-cutting/00-index.md)
