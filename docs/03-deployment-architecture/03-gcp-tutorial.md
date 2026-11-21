---
title: "Tutorial: Deploy LND on GCP Compute Engine with Persistent Disk and ILB"
description: "Step-by-step tutorial: Deploy production LND on GCP Compute Engine with encrypted Persistent Disk, Internal Load Balancer, Cloud Monitoring, and automated GCS backups in ~30 minutes."
tags: [tutorial, gcp, compute-engine, persistent-disk, ilb, lnd, production]
cloud: gcp
level: 200
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
estimated_time: "30 minutes"
prerequisites:
  - "Google Cloud SDK (gcloud) installed and authenticated"
  - "Terraform >= 1.9 installed"
  - "Git installed"
  - "GCP project with Compute Engine, Cloud Storage, Cloud KMS, Cloud Monitoring APIs enabled"
  - "SSH key pair generated"
references:
  - "GCP LND Terraform Module"
  - "LND Operations Guide"
  - "Compute Engine Documentation"
---

# Tutorial: Deploy LND on GCP Compute Engine

> **Goal**: Deploy a production-ready LND node on GCP Compute Engine with encrypted Persistent Disk, Internal Load Balancer, Cloud Monitoring, and automated GCS backups in ~30 minutes.
>
> **Architecture**: Single VM in private subnet, ILB for internal access, encrypted PD for channel state, GCS for backups. Reference [Figure 1].

## Architecture Overview [Figure 1]

```mermaid
graph TB
    subgraph GCP[GCP us-central1]
        subgraph VPC[VPC Network]
            subgraph Private[Private Subnets]
                VM[Compute Engine n2-standard-2<br/>Debian 12]
                PD1[Persistent Disk SSD 20GB<br/>Boot - CMEK Encrypted]
                PD2[Persistent Disk Balanced 100GB<br/>Data - CMEK Encrypted]
            end
        end
        subgraph Services[GCP Services]
            ILB[Internal Load Balancer<br/>Ports: 9735, 10009, 8080]
            GCS[Cloud Storage Bucket<br/>Channel Backups]
            KMS[Cloud KMS Key<br/>PD/GCS Encryption]
            CM[Cloud Monitoring<br/>Logs + Metrics]
            SM[Secret Manager<br/>Macaroon/TLS]
        end
    end
    VPN[Cloud VPN / Interconnect] --> ILB
    ILB --> VM
    VM --> PD1
    VM --> PD2
    VM -.-> GCS
    VM --> KMS
    VM --> CM
    VM --> SM
```

**Figure 1:** Tutorial architecture - GCP Compute Engine LND deployment.

## Step-by-Step Instructions

*This tutorial follows the same structure as [§12.1] (AWS) with GCP-specific commands and services. Full implementation coming soon.*

## Validation Checklist

- [ ] LND service running and synced to chain tip
- [ ] Peers connected (> 3)
- [ ] Channels open (> 1)
- [ ] RPC accessible via ILB
- [ ] Metrics appearing in Cloud Monitoring
- [ ] Backup bucket receiving channel backups daily
- [ ] Alert policies configured

## References

- [GCP LND Terraform Module](https://github.com/ajettesla/lnd-terraform-modules/tree/main/gcp/compute-lnd)
- [LND Operations Guide](https://github.com/lightningnetwork/lnd/blob/master/docs/operation_guide.md)
- [Compute Engine Documentation](https://cloud.google.com/compute/docs)
