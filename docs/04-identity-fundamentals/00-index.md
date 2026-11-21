---
title: "Identity Fundamentals"
description: "SAML 2.0 and OIDC architecture deep dive — required for federation setup"
---

# Identity Fundamentals — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-saml-oidc-fundamentals.md](01-saml-oidc-fundamentals.md) | **SAML 2.0 & OIDC architecture**: IdP/SP roles, three SAML URLs (IdP SSO, SP ACS, SP Entity ID), metadata exchange, SP-initiated vs IdP-initiated flows, signing vs encryption certs, OIDC Auth Code + PKCE, discovery/JWKS, token types, attribute mapping (stable identifiers, groups), CEL conditions, sync-less vs provisioned, two gates (IdP app assignment vs SP IAM), troubleshooting matrix |

**Prerequisites**: Read [Cloud Architecture](../02-cloud-architecture/00-index.md) first — federation builds on cloud IAM

**Next**: [Cloud Platform Guides](../05-cloud-platform-guides/00-index.md) — Cloud-specific IAM implementation