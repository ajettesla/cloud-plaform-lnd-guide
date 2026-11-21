---
title: "Cloud Platform Guides"
description: "Cloud-specific IAM implementation for AWS, GCP, and Azure"
---

# Cloud Platform Guides — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-aws-iam.md](01-aws-iam.md) | **AWS IAM deep dive**: Core model (users, roles, policies, SCPs), IAM Identity Center (SAML+SCIM, Permission Sets, Account Assignments), Direct SAML federation, OIDC federation (GitHub), STS (AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity), IRSA (EKS OIDC provider, pod trust policy, K8s SA annotation), AWS as IdP (Identity Center → GCP) |
| 2 | [02-gcp-iam.md](02-gcp-iam.md) | **GCP IAM deep dive**: Resource hierarchy, Cloud Identity vs Org Resource, IAM model (principals, roles, conditions), Workforce Identity Federation (pools, SAML/OIDC providers, attribute mapping, principal identifiers, sign-in flow), Workload Identity Federation (pools, Azure MI/GitHub/AWS providers, SA impersonation), Service Accounts, monitoring/audit logs |
| 3 | [03-azure-iam.md](03-azure-iam.md) | **Azure IAM deep dive**: Entra ID architecture (two-plane model), **Entra ID vs Azure RBAC separation**, Enterprise Apps (SAML IdP) vs App Registrations (OIDC IdP), SAML config (Entity ID, ACS, RelayState, claims, signing cert), OIDC config, Managed Identities (system/user-assigned, IMDS token), Workload Identity Federation (federated credentials for GitHub/K8s), Entra Workload Identity (AKS), Conditional Access, Entitlement Management, PIM |

**Prerequisites**: Complete [Identity Fundamentals](../04-identity-fundamentals/00-index.md) and [Cloud Architecture](../02-cloud-architecture/00-index.md)

**Next**: [Cross-Cloud Comparison](../06-cross-cloud-comparison/00-index.md) — Side-by-side comparisons