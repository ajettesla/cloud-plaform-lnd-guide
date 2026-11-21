---
title: "Cloud Provider Detailed Comparison: Networking, Data Transfer Costs, HA, and Pricing"
description: "Deep-dive comparison of AWS, GCP, and Azure covering backbone networking, egress/ingress costs, cross-zone/region data transfer, bucket/log storage costs, high availability with evidence, and LND-specific pricing."
tags: [comparison, aws, gcp, azure, networking, egress, ingress, ha, pricing, data-transfer]
cloud: all
level: 300
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS Data Transfer Pricing"
  - "Google Cloud Network Pricing"
  - "Azure Bandwidth Pricing"
  - "AWS Global Infrastructure"
  - "Google Cloud Network Tiers"
  - "Azure Bandwidth Pricing"
---

# Abstract

This document provides a detailed, evidence-based comparison of AWS, GCP, and Azure across four critical dimensions: backbone network architecture, data transfer costs (egress/ingress/cross-zone/cross-region), bucket and log storage costs, and high availability capabilities with documented SLAs and failover times. All claims reference official provider pricing pages and SLAs. For cloud fundamentals, see [§00-cloud-intro.overview]. For LND-specific deployment patterns, see [§00-cloud-intro.architecture-patterns].

# 1. Backbone Network Architecture Comparison

## 1.1 Network Ownership and Topology

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Fiber Ownership** | AWS-owned trans-oceanic and terrestrial fiber | Google-owned subsea cables (Curie, Dunant, Equiano, Grace Hopper) + terrestrial | Microsoft-owned subsea (MAREA, AEC-1) + terrestrial |
| **Backbone Capacity** | Multiple 100-400 Gbps links between regions | 100+ Tbps aggregate capacity | 175+ PoPs, 190+ edge sites |
| **Traffic Path** | Always on AWS backbone for VPC peering, TGW, Direct Connect | Premium Tier: Google backbone; Standard Tier: Public internet | Microsoft backbone for ExpressRoute, VNet peering, Virtual WAN |
| **Inter-Region Latency (Typical)** | us-east-1 to us-west-2: ~70ms | us-central1 to us-west1: ~40ms | East US to West US 2: ~60ms |
| **Anycast Edge Network** | CloudFront (400+ PoPs) | Cloud CDN (100+ PoPs) | Front Door (175+ PoPs) |

## 1.2 Private Connectivity Options

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Dedicated Connection** | Direct Connect (1, 10, 100 Gbps) | Cloud Interconnect (10, 100 Gbps Dedicated; Partner up to 10 Gbps) | ExpressRoute (50 Mbps - 100 Gbps) |
| **VPN** | Site-to-Site VPN (IPsec, up to 1.25 Gbps) | Cloud VPN (HA VPN, 3 Gbps per tunnel, 99.99% SLA) | VPN Gateway (Active/Active, up to 10 Gbps) |
| **Cross-Cloud Interconnect** | Direct Connect + Partner Interconnect | Cloud Interconnect + Partner | ExpressRoute Global Reach + ExpressRoute Direct |
| **Transit Hub** | Transit Gateway (hub-and-spoke, multicast support) | Network Connectivity Center (hub, spoke, mesh) | Virtual WAN (hub, secured hub, ExpressRoute/VPN aggregation) |

## 1.3 VPC/VNet Architecture

| Feature | AWS VPC | GCP VPC | Azure VNet |
|---------|---------|---------|------------|
| **Scope** | Region-scoped | Global (single VPC spans regions) | Region-scoped |
| **Subnet Scope** | AZ-scoped | Region-scoped | Region-scoped |
| **Max CIDR per VPC** | /16 (5 /16s via secondary CIDRs) | /16 (expandable to /8 via add) | /8 |
| **Peering** | Non-transitive; transitive via TGW | Non-transitive (export/import custom routes) | Non-transitive; transitive via Virtual WAN |
| **Max Peering Connections** | 125 per VPC (soft limit) | 25 per VPC (soft limit) | 500 per VNet |
| **Private Service Access** | PrivateLink (interface/gateway endpoints) | Private Service Connect (PSC) | Private Link / Service Endpoints |
| **DNS** | Route 53 (private hosted zones) | Cloud DNS (private zones, DNS forwarding) | Azure Private DNS Zones |

References: [AWS VPC](https://docs.aws.amazon.com/vpc/latest/userguide/), [GCP VPC](https://cloud.google.com/vpc/docs), [Azure VNet](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview)

# 2. Data Transfer Costs: Egress, Ingress, Cross-Zone, Cross-Region

## 2.1 Definitions

- **Ingress**: Data entering the cloud provider network (typically free)
- **Egress**: Data leaving the cloud provider network to internet (charged per GB)
- **Cross-Zone**: Data transfer between AZs within same region
- **Cross-Region**: Data transfer between regions (same or different continent)
- **Inter-Cloud**: Data transfer between different cloud providers

## 2.2 Ingress Costs (All Providers: Free)

| Provider | Ingress Cost | Notes |
|----------|--------------|-------|
| AWS | Free | All services |
| GCP | Free | All services |
| Azure | Free | All services |

## 2.3 Egress to Internet (Per GB, USD, Premium Tier / Standard Tier)

### First 10 TB / Month (Standard Pricing)

| Destination | AWS | GCP (Premium) | GCP (Standard) | Azure |
|-------------|-----|---------------|----------------|-------|
| **us-east-1 / us-central1 / East US** | $0.09 | $0.12 | $0.08 | $0.087 |
| **us-west-2 / us-west1 / West US 2** | $0.09 | $0.12 | $0.08 | $0.087 |
| **eu-west-1 / europe-west1 / West Europe** | $0.09 | $0.12 | $0.08 | $0.087 |
| **ap-northeast-1 / asia-northeast1 / East Asia** | $0.114 | $0.19 | $0.12 | $0.138 |

### Volume Discounts (Per TB/Month)

| Monthly Volume | AWS | GCP (Premium) | Azure |
|----------------|-----|---------------|-------|
| 10 - 50 TB | $0.085 | $0.11 | $0.083 |
| 50 - 150 TB | $0.070 | $0.08 | $0.070 |
| 150 - 500 TB | $0.050 | $0.06 | $0.055 |
| 500+ TB | Custom | Custom | Custom |

> **Critical**: GCP Standard Tier uses public internet for egress (cheaper, higher latency). Premium Tier uses Google backbone. AWS and Azure always use their private backbone.

References: [AWS Data Transfer](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer), [GCP Network Pricing](https://cloud.google.com/vpc/network-pricing), [Azure Bandwidth](https://azure.microsoft.com/pricing/details/bandwidth/)

## 2.4 Cross-Zone Data Transfer (Within Same Region)

| Provider | Cost | Notes |
|----------|------|-------|
| **AWS** | $0.01/GB (each direction) | Charged for traffic between AZs via private IPs. Applies to EC2, RDS, ElastiCache, ALB/NLB cross-zone. |
| **GCP** | Free | No charge for VM-to-VM traffic between zones in same region (uses Google backbone). |
| **Azure** | Free | No charge for VM-to-VM traffic between zones in same region. |

> **Impact for LND**: AWS cross-zone replication (RDS Multi-AZ, EBS replication) incurs cost. GCP and Azure do not charge.

## 2.5 Cross-Region Data Transfer (Per GB, USD)

| Source → Destination | AWS | GCP (Premium) | Azure |
|----------------------|-----|---------------|-------|
| **US East → US West** | $0.02 | $0.01 | $0.02 |
| **US → EU** | $0.02 | $0.08 | $0.05 |
| **US → Asia Pacific** | $0.09 | $0.12 | $0.10 |
| **EU → Asia Pacific** | $0.09 | $0.11 | $0.10 |

> **Note**: AWS charges same rate for all cross-region ($0.02/GB within continent, $0.09 inter-continent). GCP and Azure vary by region pair.

## 2.6 Inter-Cloud Data Transfer (Egress from Source + Ingress to Destination)

| Path | Effective Cost (Source Egress) | Notes |
|------|-------------------------------|-------|
| **AWS → GCP** | AWS egress rate ($0.09/GB) | GCP ingress free |
| **AWS → Azure** | AWS egress rate ($0.09/GB) | Azure ingress free |
| **GCP → AWS** | GCP Premium egress ($0.12/GB) | AWS ingress free |
| **GCP → Azure** | GCP Premium egress ($0.12/GB) | Azure ingress free |
| **Azure → AWS** | Azure egress ($0.087/GB) | AWS ingress free |
| **Azure → GCP** | Azure egress ($0.087/GB) | GCP ingress free |

## 2.7 Data Transfer Cost Summary for LND (1 TB/Month Egress)

| Scenario | AWS | GCP (Premium) | Azure |
|----------|-----|---------------|-------|
| **LND P2P gossip (cross-zone, 500 GB)** | $5.00 | $0.00 | $0.00 |
| **LND backups to cross-region bucket (500 GB)** | $10.00 | $5.00 (US) / $40.00 (US→EU) | $10.00 (US) / $25.00 (US→EU) |
| **LND RPC/API egress to internet (500 GB)** | $45.00 | $60.00 (Premium) / $40.00 (Standard) | $43.50 |
| **Total (typical LND node)** | **~$60/mo** | **~$65/mo (Premium) / ~$40/mo (Standard)** | **~$53.50/mo** |

# 3. Object Storage (Bucket) Costs

## 3.1 Storage Class Pricing (Per GB/Month, USD)

| Class | AWS S3 | GCP Cloud Storage | Azure Blob |
|-------|--------|-------------------|------------|
| **Hot/Standard** | $0.023 | $0.026 | $0.0184 |
| **Cool/IA (30d min)** | $0.0125 (IA) | $0.010 (Nearline) | $0.01 (Cool) |
| **Cold (90d min)** | $0.004 (Glacier) | $0.004 (Coldline) | $0.0036 (Cold) |
| **Archive (180d min)** | $0.00099 (Deep Archive) | $0.0012 (Archive) | $0.00099 (Archive) |

## 3.2 LND Backup Storage Costs (100 GB Channel Backups + 50 GB Logs)

| Storage Pattern | AWS S3 | GCP Cloud Storage | Azure Blob |
|-----------------|--------|-------------------|------------|
| **Standard (Hot)** | $3.45/mo | $3.90/mo | $2.76/mo |
| **IA/Nearline (30d)** | $1.88/mo | $1.50/mo | $1.50/mo |
| **Glacier/Coldline (90d)** | $0.60/mo | $0.60/mo | $0.54/mo |
| **Lifecycle: Hot 30d → IA 90d → Archive 365d** | ~$1.20/mo | ~$1.00/mo | ~$0.90/mo |

## 3.3 Object Operations (Per 10,000 Requests)

| Operation | AWS S3 | GCP Cloud Storage | Azure Blob |
|-----------|--------|-------------------|------------|
| **PUT/POST/LIST** | $0.005 | $0.05 | $0.05 |
| **GET/HEAD** | $0.0004 | $0.004 | $0.004 |
| **Lifecycle Transition** | $0.01 | $0.01 | $0.01 |

# 4. Log Storage and Retention Costs

## 4.1 Log Ingestion and Retention (Per GB/Month)

| Service | AWS CloudWatch Logs | GCP Cloud Logging | Azure Log Analytics |
|---------|---------------------|-------------------|---------------------|
| **Ingestion** | $0.50/GB | $0.50/GB (first 50 GB free) | $2.30/GB (pay-as-you-go) |
| **Retention (Standard)** | $0.03/GB/mo (first 30 days free) | $0.03/GB/mo | Included in ingestion |
| **Retention (Extended)** | $0.01/GB/mo (after 30 days) | $0.01/GB/mo (after 30 days) | $0.10/GB/mo (archive) |
| **Query/Analysis** | $0.005/GB scanned (Insights) | Free (Logging) / $5/TB (BigQuery) | $2.30/GB (query) |

## 4.2 LND Log Volume Estimate

Typical LND node generates ~50-200 MB/day of structured logs (JSON):
- **Low activity**: 50 MB/day = 1.5 GB/month
- **High activity**: 200 MB/day = 6 GB/month

| Volume | AWS CloudWatch | GCP Cloud Logging | Azure Log Analytics |
|--------|----------------|-------------------|---------------------|
| **1.5 GB/mo** | ~$0.75/mo (ingest) + $0.045/mo (retention) | ~$0.75/mo (ingest) + $0.045/mo | ~$3.45/mo |
| **6 GB/mo** | ~$3.00/mo + $0.18/mo | ~$3.00/mo + $0.18/mo | ~$13.80/mo |

## 4.3 Cost Optimization for Logs

| Strategy | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **Reduce retention** | Set 7-30 day retention | Set 7-30 day retention | Set 30-90 day retention |
| **Export to object storage** | CloudWatch → S3 (Kinesis Firehose) | Logging sink → GCS/BigQuery | Diagnostic settings → Blob/ADX |
| **Filter at source** | Log group filter patterns | Log router exclusions | DCR transformations |
| **Compress before ingest** | CloudWatch agent compression | Fluent Bit compression | AMA compression |

References: [AWS CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/), [GCP Logging Pricing](https://cloud.google.com/logging/pricing), [Azure Monitor Pricing](https://azure.microsoft.com/pricing/details/monitor/)

# 5. Block Storage (Disk) Costs

## 5.1 Disk Type Pricing (Per GB/Month, USD)

| Type | AWS EBS | GCP Persistent Disk | Azure Managed Disks |
|------|---------|---------------------|---------------------|
| **General Purpose (gp3 / Balanced / Premium v2)** | $0.08 (gp3) + $0.005/IOPS | $0.10 (Balanced) | $0.075 (Premium v2) |
| **High Performance (io2 / Extreme / Premium)** | $0.125 (io2) + $0.065/IOPS | $0.17 (Extreme) | $0.15 (Premium) |
| **Throughput Optimized (st1)** | $0.045 | N/A | N/A |
| **Cold HDD (sc1)** | $0.025 | $0.04 (Standard HDD) | $0.018 (Standard HDD) |

## 5.2 LND Disk Cost (100 GB gp3/Balanced/Premium v2, 3000 IOPS)

| Provider | Disk Cost | IOPS Cost | Total/Month |
|----------|-----------|-----------|-------------|
| **AWS (gp3)** | $8.00 | $15.00 (3000 × $0.005) | $23.00 |
| **GCP (Balanced)** | $10.00 | Included (up to 80K IOPS) | $10.00 |
| **Azure (Premium v2)** | $7.50 | Included (up to 80K IOPS) | $7.50 |

> **Note**: gp3 includes 3000 IOPS free; additional IOPS $0.005 each. Balanced PD and Premium v2 include high IOPS baseline.

## 5.3 Snapshot Costs (Per GB/Month)

| Type | AWS EBS | GCP Persistent Disk | Azure Managed Disks |
|------|---------|---------------------|---------------------|
| **Incremental** | $0.05 | $0.05 | $0.05 |
| **Cross-Region Copy** | $0.01/GB + storage | $0.01/GB + storage | $0.01/GB + storage |

# 6. Load Balancer Costs

| Type | AWS | GCP | Azure |
|------|-----|-----|-------|
| **L4 (Network/TCP/UDP)** | NLB: $0.0225/hr + $0.008/LCU | Cloud LB (External TCP/UDP): $0.025/hr + $0.008/GB | Standard LB: $0.025/hr + $0.008/GB |
| **L7 (Application/HTTP/HTTPS)** | ALB: $0.0225/hr + $0.008/LCU | Cloud LB (External HTTP/S): $0.025/hr + $0.008/GB | Application Gateway v2: $0.025/hr + $0.008/GB |
| **Global Anycast** | Global Accelerator: $0.025/hr + $0.015/GB | Cloud LB (Premium Tier): included | Front Door: $0.018/hr + $0.008/GB |

## Monthly Cost (730 hours, moderate traffic)

| LB Type | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **NLB / TCP LB** | ~$18 + LCU | ~$18 + GB | ~$18 + GB |
| **ALB / HTTP LB** | ~$18 + LCU | ~$18 + GB | ~$18 + GB (App Gateway) |

# 7. High Availability Comparison with Evidence

## 7.1 SLA Commitments

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Compute (Multi-AZ/Zone)** | 99.99% | 99.99% (Regional MIG) | 99.99% (Zonal) |
| **Managed DB (RDS/Cloud SQL/Azure SQL)** | 99.95% (Multi-AZ) | 99.95% (Regional HA) | 99.99% (Zone-redundant) |
| **Object Storage** | 99.99% (S3 Standard) | 99.99% (Standard) | 99.99% (Hot/Cool) |
| **Load Balancer** | 99.99% (NLB/ALB) | 99.99% (Cloud LB) | 99.99% (LB/Front Door) |
| **Kubernetes Control Plane** | 99.95% (EKS) | 99.95% (GKE) | 99.95% (AKS) |

## 7.2 Documented Failover Times

| Scenario | AWS | GCP | Azure | Source |
|----------|-----|-----|-------|--------|
| **RDS Multi-AZ Failover** | 60-120 seconds | < 60 seconds (Cloud SQL) | < 30 seconds (Azure SQL) | [1][2][3] |
| **Cross-Region DB Failover** | Minutes (manual/promote) | Minutes (Cross-region replica) | Minutes (Geo-replication) | [1][2][3] |
| **VM Restart (Host Failure)** | < 5 minutes (Auto Recovery) | < 5 minutes (Live Migration) | < 5 minutes (Auto-heal) | [4][5][6] |
| **Global LB Failover** | < 30 seconds (Health checks) | < 30 seconds (Health checks) | < 60 seconds (Front Door) | [7][8][9] |

## 7.3 HA Architecture Evidence

### AWS
- **RDS Multi-AZ**: Synchronous replication to standby in different AZ. Automatic failover with DNS switch. [AWS RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
- **S3 Cross-Region Replication**: Async, configurable, SLA 99.99% durability. [S3 CRR](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)
- **Global Accelerator**: Anycast IPs, health checks every 10s, failover < 30s. [Global Accelerator](https://aws.amazon.com/global-accelerator/)

### GCP
- **Cloud SQL Regional HA**: Synchronous replication across zones, automatic failover < 60s. [Cloud SQL HA](https://cloud.google.com/sql/docs/mysql/high-availability)
- **Cloud Spanner**: Multi-region, 99.999% SLA, strong consistency. [Spanner](https://cloud.google.com/spanner)
- **Cloud Load Balancing**: Global anycast, health checks, seamless failover. [Cloud LB](https://cloud.google.com/load-balancing)

### Azure
- **Azure SQL Zone-Redundant**: Synchronous replication, automatic failover < 30s. [Azure SQL HA](https://learn.microsoft.com/azure/azure-sql/database/high-availability-sla)
- **Cosmos DB**: 99.999% SLA, multi-region, 5 consistency levels. [Cosmos DB HA](https://learn.microsoft.com/azure/cosmos-db/high-availability)
- **Front Door**: Global anycast, health probes, instant failover. [Front Door](https://learn.microsoft.com/azure/frontdoor/)

## 7.4 HA Capability Matrix for LND

| Requirement | AWS | GCP | Azure | Best Choice |
|-------------|-----|-----|-------|-------------|
| **Single-node VM HA** | Auto Recovery + Multi-AZ ASG | Live Migration + Regional MIG | Availability Zones + VMSS | Azure (99.99% VM SLA) |
| **Managed DB HA** | RDS Multi-AZ (60-120s) | Cloud SQL Regional HA (<60s) | Azure SQL Zone-redundant (<30s) | Azure (fastest failover) |
| **Global LND RPC Access** | Global Accelerator | Cloud LB (Premium) | Front Door | GCP (true anycast) |
| **Cross-Region DR** | S3 CRR + RDS Read Replica | Cloud Storage Dual-Region + Spanner | Cosmos DB + GRS | GCP (strong consistency) |
| **Strong Consistency Multi-Region** | DynamoDB Global Tables (eventual) | Cloud Spanner (strong) | Cosmos DB (5 levels) | GCP Spanner |

# 8. LND-Specific Cost Model (Monthly, us-east-1/us-central1/East US)

## 8.1 Self-Managed VM (m6i.large / n2-standard-2 / Standard_D4s_v3)

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| Compute (730h, on-demand) | $67.89 | $52.56 | $63.51 |
| EBS / PD / Disk (100 GB, 3000 IOPS) | $23.00 | $10.00 | $7.50 |
| Snapshots (daily, 30-day retention) | $5.00 | $5.00 | $5.00 |
| NLB / TCP LB / Standard LB | $18.00 | $18.00 | $18.00 |
| Data Transfer (1 TB egress) | $90.00 | $120.00 (Premium) / $80.00 (Standard) | $87.00 |
| CloudWatch / Cloud Logging / Log Analytics (6 GB) | $3.20 | $3.20 | $13.80 |
| S3 / GCS / Blob (100 GB backups, lifecycle) | $1.20 | $1.00 | $0.90 |
| **Total (On-Demand)** | **$208.29** | **$209.76 (Premium) / $169.76 (Standard)** | **$195.71** |
| **With 1-Year Savings/Commit** | **~$155** | **~$155 / ~$115** | **~$145** |

## 8.2 Kubernetes (EKS/GKE/AKS) Control Plane + 3 Worker Nodes

| Component | AWS EKS | GCP GKE | Azure AKS |
|-----------|---------|---------|-----------|
| Control Plane | $73.00 | $73.00 (Standard) / ~$10-20/pod (Autopilot) | Free |
| Worker Nodes (3× m6i.large) | $203.67 | $157.68 | $190.53 |
| Load Balancer | $18.00 | $18.00 | $18.00 |
| Data Transfer (1 TB) | $90.00 | $120.00 / $80.00 | $87.00 |
| **Total** | **$384.67** | **$368.68 / $328.68** | **$295.53** |

# 9. Decision Matrix by Priority

| Priority | Recommended | Rationale |
|----------|-------------|-----------|
| **Lowest Total Cost** | GCP (Standard Tier) | Lowest egress, free cross-zone, competitive disk |
| **Lowest Egress Cost** | GCP Standard Tier | $0.08/GB vs $0.09 (AWS) vs $0.087 (Azure) |
| **Best HA (VM + DB)** | Azure | 99.99% VM SLA, <30s SQL failover, zone-redundant storage |
| **Best Global Anycast** | GCP (Premium) | True anycast Cloud LB, Cloud CDN on Google backbone |
| **Strong Consistency Multi-Region** | GCP | Cloud Spanner (unique offering) |
| **Enterprise Hybrid** | Azure | Arc, ExpressRoute, Entra ID, Windows integration |
| **Most Services/Maturity** | AWS | Broadest portfolio, most regions, Graviton ARM |
| **Kubernetes (Free Control Plane)** | Azure / GKE Autopilot | AKS free; GKE Autopilot per-pod |
| **ARM/Graviton Price/Performance** | AWS | Graviton4, 40% better price/performance |

# 10. Reading Order

1. [§00-cloud-intro.overview] — Cloud fundamentals, global infrastructure, HA principles
2. [§00-cloud-intro.cloud-comparison] (this document) — Detailed networking, costs, HA evidence
3. [§00-cloud-intro.backbone-network] — Deep dive on backbone architecture
4. [§00-cloud-intro.data-transfer-costs] — Detailed egress/ingress/cross-zone/region costs
5. [§00-cloud-intro.ha-comparison] — HA capabilities with failover evidence
6. [§00-cloud-intro.architecture-patterns] — LND deployment patterns
7. [§01-aws.iam], [§02-gcp.iam], [§03-azure.iam] — Cloud-specific IAM
8. [§01-aws.aws-lnd-vm], [§02-gcp.gcp-lnd-vm], [§03-azure.azure-lnd-vm] — Tutorials
9. [§04-cross-cloud.*] — Cross-cloud patterns

# References

[1] AWS, "RDS Multi-AZ Deployments," https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html
[2] Google Cloud, "Cloud SQL High Availability," https://cloud.google.com/sql/docs/mysql/high-availability
[3] Microsoft, "Azure SQL Database High Availability," https://learn.microsoft.com/azure/azure-sql/database/high-availability-sla
[4] AWS, "EC2 Instance Auto Recovery," https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html
[5] Google Cloud, "Live Migration," https://cloud.google.com/compute/docs/instances/live-migration
[6] Microsoft, "Virtual Machine Automatic Repair," https://learn.microsoft.com/azure/virtual-machines/automatic-repair
[7] AWS, "Global Accelerator," https://aws.amazon.com/global-accelerator/
[8] Google Cloud, "Cloud Load Balancing," https://cloud.google.com/load-balancing
[9] Microsoft, "Azure Front Door," https://learn.microsoft.com/azure/frontdoor/
[10] AWS, "Data Transfer Pricing," https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer
[11] Google Cloud, "Network Pricing," https://cloud.google.com/vpc/network-pricing
[12] Microsoft, "Bandwidth Pricing," https://azure.microsoft.com/pricing/details/bandwidth/
[13] AWS, "S3 Pricing," https://aws.amazon.com/s3/pricing/
[14] Google Cloud, "Cloud Storage Pricing," https://cloud.google.com/storage/pricing
[15] Microsoft, "Blob Storage Pricing," https://azure.microsoft.com/pricing/details/storage/blobs/
[16] AWS, "CloudWatch Pricing," https://aws.amazon.com/cloudwatch/pricing/
[17] Google Cloud, "Logging Pricing," https://cloud.google.com/logging/pricing
[18] Microsoft, "Monitor Pricing," https://azure.microsoft.com/pricing/details/monitor/