---
title: "Data Transfer Costs Deep Dive: Egress, Ingress, Cross-Zone, Cross-Region, Bucket, and Log Costs"
description: "Comprehensive analysis of data transfer pricing across AWS, GCP, and Azure including egress/ingress, cross-zone/region, object storage classes, log ingestion/retention, and LND-specific cost models."
tags: [data-transfer, egress, ingress, cross-zone, cross-region, bucket, logs, pricing, aws, gcp, azure]
cloud: all
level: 300
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS Data Transfer Pricing"
  - "Google Cloud Network Pricing"
  - "Azure Bandwidth Pricing"
  - "AWS S3 Pricing"
  - "Google Cloud Storage Pricing"
  - "Azure Blob Storage Pricing"
  - "AWS CloudWatch Pricing"
  - "Google Cloud Logging Pricing"
  - "Azure Monitor Pricing"
---

# Abstract

This document provides an exhaustive analysis of data transfer costs across AWS, GCP, and Azure. It covers every dimension of data movement pricing: ingress (free), egress to internet, cross-zone, cross-region, inter-cloud, object storage classes with lifecycle policies, log ingestion and retention, and block storage snapshots. Includes detailed LND-specific cost models with real-world estimates. All pricing references official provider pricing pages as of November 2026.

# 1. Cost Model Fundamentals

## 1.1 Key Definitions

| Term | Definition | Billable? |
|------|------------|-----------|
| **Ingress** | Data entering provider network from internet or other clouds | No (all providers) |
| **Egress** | Data leaving provider network to internet | Yes (per GB) |
| **Cross-Zone** | Data between AZs in same region | Varies by provider |
| **Cross-Region** | Data between regions (same continent) | Yes (per GB) |
| **Inter-Continental** | Data between continents | Yes (higher rate) |
| **Inter-Cloud** | Data between cloud providers | Charged at source egress rate |
| **Private Connectivity** | Direct Connect, Interconnect, ExpressRoute | Port hours + reduced egress |

## 1.2 Pricing Model Principles

| Principle | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Ingress** | Always free | Always free | Always free |
| **Egress Tiering** | Volume discounts at 10/50/150/500 TB | Volume discounts at 10/50/150/500 TB | Volume discounts at 10/50/150/500 TB |
| **Cross-Zone** | Charged ($0.01/GB) | Free | Free |
| **Cross-Region** | Flat $0.02/GB (intra-continent) | Varies by region pair | Varies by region pair |
| **Private Connectivity** | Reduced egress via DX | Reduced egress via Interconnect | Reduced egress via ExpressRoute |

# 2. Ingress Costs (All Providers: Free)

| Provider | Ingress from Internet | Ingress from Other Clouds | Ingress via Private Link |
|----------|----------------------|--------------------------|-------------------------|
| **AWS** | Free | Free | Free (no data charge, port hours only) |
| **GCP** | Free | Free | Free (no data charge, port hours only) |
| **Azure** | Free | Free | Free (no data charge, port hours only) |

> **Implication**: LND node receiving P2P gossip, RPC calls, or backup restores incurs zero ingress cost regardless of source.

# 3. Egress to Internet (Public IP)

## 3.1 Standard Tier Pricing (Per GB, USD)

### AWS (us-east-1 Baseline)

| Monthly Volume | First 10 TB | 10-50 TB | 50-150 TB | 150-500 TB | 500+ TB |
|----------------|-------------|----------|-----------|------------|---------|
| **Rate/GB** | $0.090 | $0.085 | $0.070 | $0.050 | Custom |

### GCP (Premium Tier, us-central1 Baseline)

| Monthly Volume | First 10 TB | 10-50 TB | 50-150 TB | 150-500 TB | 500+ TB |
|----------------|-------------|----------|-----------|------------|---------|
| **Rate/GB** | $0.120 | $0.110 | $0.080 | $0.060 | Custom |

### GCP (Standard Tier, us-central1)

| Monthly Volume | First 10 TB | 10-50 TB | 50-150 TB | 150-500 TB |
|----------------|-------------|----------|-----------|------------|
| **Rate/GB** | $0.080 | $0.075 | $0.070 | $0.065 |

### Azure (East US Baseline)

| Monthly Volume | First 10 TB | 10-50 TB | 50-150 TB | 150-500 TB | 500+ TB |
|----------------|-------------|----------|-----------|------------|---------|
| **Rate/GB** | $0.087 | $0.083 | $0.070 | $0.055 | Custom |

## 3.2 Regional Egress Variations (Per GB, First 10 TB)

| Region | AWS | GCP (Premium) | Azure |
|--------|-----|---------------|-------|
| **US East (N. Virginia / us-central1 / East US)** | $0.090 | $0.120 | $0.087 |
| **US West (Oregon / us-west1 / West US 2)** | $0.090 | $0.120 | $0.087 |
| **EU West (Ireland / europe-west1 / West Europe)** | $0.090 | $0.120 | $0.087 |
| **APAC (Tokyo / asia-northeast1 / East Asia)** | $0.114 | $0.190 | $0.138 |
| **South America (São Paulo / southamerica-east1 / South Africa)** | $0.160 | $0.230 | $0.187 |

## 3.3 Egress via Private Connectivity (Reduced Rates)

| Path | AWS (via Direct Connect) | GCP (via Cloud Interconnect) | Azure (via ExpressRoute) |
|------|--------------------------|-----------------------------|-------------------------|
| **To Internet** | Same as public egress | Same as public egress | Same as public egress |
| **To Other Cloud** | Standard egress from AWS | Standard egress from GCP | Standard egress from Azure |
| **To On-Premises** | $0.02/GB (DX) + port hours | $0.02/GB (Interconnect) + port hours | $0.025/GB (ER) + port hours |

> **Key Point**: Private connectivity does NOT reduce egress to internet. It only reduces costs for traffic between cloud and on-premises or between clouds when using provider's private backbone.

# 4. Cross-Zone Data Transfer (Within Same Region)

## 4.1 Pricing Comparison

| Provider | Cost per GB (Each Direction) | Services Affected |
|----------|------------------------------|-------------------|
| **AWS** | $0.01 | EC2, RDS, ElastiCache, ALB/NLB, EFS, NAT Gateway |
| **GCP** | Free | All services (VM-to-VM, LB, Cloud SQL, GCS) |
| **Azure** | Free | All services (VM-to-VM, LB, Azure SQL, Blob) |

## 4.2 Impact on LND Architecture

| LND Component | AWS Cost Impact | GCP Cost Impact | Azure Cost Impact |
|---------------|-----------------|-----------------|-------------------|
| **P2P Gossip (Cross-AZ)** | $0.01/GB | Free | Free |
| **RDS Multi-AZ Sync** | Charged (per GB replicated) | Free | Free |
| **ElastiCache Replication** | Charged | Free | Free |
| **ALB/NLB Cross-Zone** | $0.01/GB (if enabled) | Free | Free |

> **Annual Estimate for LND (100 GB/mo cross-AZ)**: AWS = $12/year; GCP/Azure = $0

# 5. Cross-Region Data Transfer (Per GB, USD)

## 5.1 Intra-Continent (Same Continent)

| Source → Destination | AWS | GCP (Premium) | Azure |
|----------------------|-----|---------------|-------|
| **US East ↔ US West** | $0.020 | $0.010 | $0.020 |
| **US East ↔ US Central** | $0.020 | $0.010 | $0.020 |
| **EU West ↔ EU Central** | $0.020 | $0.010 | $0.020 |
| **APAC ↔ APAC** | $0.020 | $0.010 | $0.020 |

## 5.2 Inter-Continent (Different Continents)

| Source → Destination | AWS | GCP (Premium) | Azure |
|----------------------|-----|---------------|-------|
| **US East ↔ EU West** | $0.020 | $0.080 | $0.050 |
| **US East ↔ APAC (Tokyo)** | $0.090 | $0.120 | $0.100 |
| **US East ↔ South America** | $0.090 | $0.140 | $0.120 |
| **EU West ↔ APAC** | $0.090 | $0.110 | $0.100 |
| **EU West ↔ South America** | $0.090 | $0.130 | $0.110 |

## 5.3 Cross-Region Cost Matrix for LND Backups

| Backup Scenario | Data/Month | AWS | GCP (Premium) | Azure |
|-----------------|------------|-----|---------------|-------|
| **Same Region (Cross-AZ)** | 100 GB | Free (intra-AZ) / $1.00 (cross-AZ) | Free | Free |
| **US East → US West** | 100 GB | $2.00 | $1.00 | $2.00 |
| **US East → EU West** | 100 GB | $2.00 | $8.00 | $5.00 |
| **US East → APAC** | 100 GB | $9.00 | $12.00 | $10.00 |
| **Annual (US→EU, 100 GB/mo)** | 1.2 TB | $24.00 | $96.00 | $60.00 |

> **Note**: GCP Premium Tier cross-region pricing varies significantly by region pair. Use [GCP Network Pricing Calculator](https://cloud.google.com/products/calculator) for exact figures.

# 6. Inter-Cloud Data Transfer (Effective Cost)

Since ingress is free everywhere, cost = source provider egress rate.

| Path | Source Egress Rate (First 10 TB) | Effective Cost/GB |
|------|---------------------------------|-------------------|
| **AWS → GCP** | $0.090 (AWS egress) | $0.090 |
| **AWS → Azure** | $0.090 (AWS egress) | $0.090 |
| **GCP → AWS** | $0.120 (GCP Premium egress) | $0.120 |
| **GCP → Azure** | $0.120 (GCP Premium egress) | $0.120 |
| **Azure → AWS** | $0.087 (Azure egress) | $0.087 |
| **Azure → GCP** | $0.087 (Azure egress) | $0.087 |

## 6.1 Cost Optimization for Inter-Cloud

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| **Use Standard Tier (GCP)** | 33% vs Premium | Configure VPC Network Tier = Standard for backup traffic |
| **Compress Before Transfer** | 60-80% reduction | gzip/zstd on backup streams |
| **Deduplicate/Incremental** | 50-90% reduction | Restic, Kopia, or native incremental snapshots |
| **Schedule Off-Peak** | No cost difference | Cron jobs (all providers same 24/7 pricing) |
| **Private Interconnect** | Port hours only (no data charge) | DX/Interconnect/ER for sustained >10 Gbps |

# 7. Object Storage (Bucket) Costs

## 7.1 Storage Class Pricing (Per GB/Month, USD)

| Class | AWS S3 | GCP Cloud Storage | Azure Blob |
|-------|--------|-------------------|------------|
| **Standard / Hot** | $0.023 | $0.026 | $0.0184 |
| **Intelligent Tiering** | $0.023 (freq) / $0.0125 (infreq) | N/A | $0.0184 / $0.01 |
| **Standard-IA / Nearline / Cool** | $0.0125 | $0.010 | $0.010 |
| **One Zone-IA / Regional-Nearline** | $0.010 | N/A | N/A |
| **Glacier IR / Coldline / Cold** | $0.004 | $0.004 | $0.0036 |
| **Glacier / Archive / Archive** | $0.0036 | $0.0012 | $0.00099 |
| **Deep Archive / Archive (180d+)** | $0.00099 | $0.0012 | $0.00099 |

## 7.2 Minimum Storage Duration & Retrieval

| Class | Min Duration | Retrieval Time | Retrieval Cost (per GB) |
|-------|--------------|----------------|-------------------------|
| **Standard** | None | Immediate | Free |
| **IA/Nearline/Cool** | 30 days | Immediate | $0.01 (AWS) / Free (GCP/Azure) |
| **Glacier/Coldline/Cold** | 90 days | Minutes-hours | $0.01-0.03 (AWS) / $0.02 (GCP) / $0.01 (Azure) |
| **Deep Archive/Archive** | 180 days | Hours (12-48) | $0.02-0.05 (AWS) / $0.05 (GCP) / $0.02 (Azure) |

## 7.3 LND Backup Storage Cost Model (150 GB: 100 GB channel backups + 50 GB logs)

### Optimal Lifecycle Policy: Hot 30d → IA 90d → Glacier 365d

| Provider | Month 1-1 (Hot) | Month 2-4 (IA) | Month 5-12 (Glacier) | Annual Cost |
|----------|-----------------|----------------|----------------------|-------------|
| **AWS S3** | $3.45 | $5.63 (3 mo × $1.88) | $6.48 (8 mo × $0.81) | **~$15.56** |
| **GCP Cloud Storage** | $3.90 | $4.50 (3 mo × $1.50) | $5.76 (8 mo × $0.72) | **~$14.16** |
| **Azure Blob** | $2.76 | $4.50 (3 mo × $1.50) | $4.32 (8 mo × $0.54) | **~$11.58** |

### Alternative: All Standard (No Lifecycle)

| Provider | Monthly | Annual |
|----------|---------|--------|
| **AWS S3** | $3.45 | $41.40 |
| **GCP Cloud Storage** | $3.90 | $46.80 |
| **Azure Blob** | $2.76 | $33.12 |

## 7.4 Object Operations Cost (Per 10,000 Requests)

| Operation | AWS S3 | GCP Cloud Storage | Azure Blob |
|-----------|--------|-------------------|------------|
| **PUT / POST / COPY** | $0.005 | $0.05 | $0.05 |
| **GET / HEAD** | $0.0004 | $0.004 | $0.004 |
| **LIST** | $0.005 | $0.05 | $0.05 |
| **DELETE** | Free | Free | Free |
| **Lifecycle Transition** | $0.01 | $0.01 | $0.01 |

## 7.5 LND Backup Operation Costs (Daily Backup, 100 GB)

| Operation | Daily Requests | Monthly Cost (AWS) | Monthly Cost (GCP) | Monthly Cost (Azure) |
|-----------|----------------|--------------------|--------------------|---------------------|
| **PUT (backup upload)** | 1 | $0.0000005 | $0.000005 | $0.000005 |
| **GET (restore test, weekly)** | 4 | $0.00000016 | $0.0000016 | $0.0000016 |
| **LIST (inventory, daily)** | 30 | $0.000015 | $0.00015 | $0.00015 |
| **Lifecycle Transitions** | 2 (Hot→IA, IA→Glacier) | $0.002 | $0.002 | $0.002 |
| **Total/Month** | ~37 | **~$0.002** | **~$0.002** | **~$0.002** |

> **Operations cost is negligible** (< $0.01/month) for typical LND backup patterns.

# 8. Log Storage and Retention Costs

## 8.1 Log Ingestion Pricing

| Service | AWS CloudWatch Logs | GCP Cloud Logging | Azure Log Analytics |
|---------|---------------------|-------------------|---------------------|
| **Ingestion** | $0.50/GB | $0.50/GB (first 50 GB/mo free) | $2.30/GB (pay-as-you-go) |
| **Free Tier** | 5 GB/mo ingestion | 50 GB/mo ingestion | None (free 5 GB in committed tier) |

## 8.2 Log Retention Pricing (Per GB/Month)

| Retention Type | AWS CloudWatch | GCP Cloud Logging | Azure Log Analytics |
|----------------|----------------|-------------------|---------------------|
| **Standard (0-30 days)** | $0.03/GB/mo (first 30 days free) | $0.03/GB/mo | Included in ingestion |
| **Extended (30-365 days)** | $0.01/GB/mo | $0.01/GB/mo | $0.10/GB/mo (archive) |
| **Long-term (365+ days)** | $0.01/GB/mo (S3 export) | $0.01/GB/mo (GCS/BigQuery) | $0.10/GB/mo (archive) |

## 8.3 LND Log Volume Estimates

| Activity Level | Daily Log Volume | Monthly Volume |
|----------------|------------------|----------------|
| **Low (Lightning node, <10 channels)** | 10-20 MB | 300-600 MB |
| **Medium (Routing node, 50-100 channels)** | 50-100 MB | 1.5-3 GB |
| **High (High-volume router, 500+ channels)** | 200-500 MB | 6-15 GB |

## 8.4 Monthly Log Cost by Provider

| Volume | AWS CloudWatch | GCP Cloud Logging | Azure Log Analytics |
|--------|----------------|-------------------|---------------------|
| **500 MB (Low)** | $0.25 (ingest) + $0.015 (retention) | $0.25 (ingest) + $0.015 (retention) | $1.15 (ingest) |
| **2 GB (Medium)** | $1.00 + $0.06 | $1.00 + $0.06 | $4.60 |
| **10 GB (High)** | $5.00 + $0.30 | $5.00 + $0.30 | $23.00 |

## 8.5 Log Cost Optimization Strategies

| Strategy | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **Reduce Retention** | Set 7-30 day retention | Set 7-30 day retention | Set 30-90 day retention |
| **Export to Object Storage** | CloudWatch → S3 (Kinesis Firehose $0.015/GB) | Logging Sink → GCS ($0.01/GB) / BigQuery | Diagnostic Settings → Blob ($0.01/GB) / ADX |
| **Filter at Source** | Log group filter patterns | Log Router exclusions | DCR transformations |
| **Compress at Source** | CloudWatch Agent (gzip) | Fluent Bit / Ops Agent compression | Azure Monitor Agent compression |
| **Sampling** | Metric filters instead of full logs | Log-based metrics | Diagnostic settings sampling |

## 8.6 Export Cost Comparison (Per GB)

| Export Path | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| **To Object Storage** | $0.015/GB (Firehose) + S3 storage | $0.01/GB (sink) + GCS storage | $0.01/GB (diagnostic) + Blob storage |
| **To Analytics** | $0.015/GB (Firehose) + Athena/Redshift | $0.01/GB (sink) + BigQuery ($5/TB) | $0.01/GB + ADX ($2.50/GB ingest) |
| **To SIEM** | $0.015/GB + partner cost | $0.01/GB + partner cost | $0.01/GB + Sentinel ($2.50/GB) |

# 9. Block Storage (Disk) and Snapshot Costs

## 9.1 Disk Type Pricing (Per GB/Month, USD)

| Type | AWS EBS | GCP Persistent Disk | Azure Managed Disks |
|------|---------|---------------------|---------------------|
| **General Purpose (gp3 / Balanced / Premium v2)** | $0.08 + $0.005/IOPS >3000 | $0.10 (includes 80K IOPS) | $0.075 (includes 80K IOPS) |
| **High Perf (io2 / Extreme / Premium)** | $0.125 + $0.065/IOPS | $0.17 (includes 300K IOPS) | $0.15 (includes 80K IOPS) |
| **Throughput (st1)** | $0.045 | N/A | N/A |
| **Cold HDD (sc1 / Standard HDD / Standard HDD)** | $0.025 | $0.04 | $0.018 |

## 9.2 LND Disk Cost (100 GB, 3000 IOPS)

| Provider | Disk Type | Base Cost | IOPS Cost | Total/Month |
|----------|-----------|-----------|-----------|-------------|
| **AWS** | gp3 | $8.00 | $0 (3000 included) | **$8.00** |
| **GCP** | Balanced PD | $10.00 | $0 (80K included) | **$10.00** |
| **Azure** | Premium v2 | $7.50 | $0 (80K included) | **$7.50** |

> **Note**: gp3 includes 3000 IOPS free; additional IOPS $0.005 each. Balanced PD and Premium v2 include high IOPS baseline at no extra cost.

## 9.3 Snapshot Costs (Per GB/Month)

| Type | AWS EBS | GCP Persistent Disk | Azure Managed Disks |
|------|---------|---------------------|---------------------|
| **Incremental (same region)** | $0.05 | $0.05 | $0.05 |
| **Cross-region copy** | $0.01/GB + storage | $0.01/GB + storage | $0.01/GB + storage |
| **Snapshot to object storage** | $0.015/GB (DLM) | N/A (manual) | N/A (manual) |

## 9.4 LND Snapshot Cost (Daily, 100 GB, 30-day retention)

| Provider | Monthly Cost | Annual Cost |
|----------|--------------|-------------|
| **All Providers** | $5.00 | $60.00 |

> **Note**: Incremental snapshots only store changed blocks. Typical LND daily change rate ~1-2 GB.

# 10. Load Balancer Data Processing Costs

| Provider | L4 (Network) | L7 (Application) |
|----------|--------------|------------------|
| **AWS** | $0.008/LCU-hour | $0.008/LCU-hour |
| **GCP** | $0.008/GB processed | $0.008/GB processed |
| **Azure** | $0.008/GB processed | $0.008/GB processed |

> **LCU (Load Balancer Capacity Unit)**: AWS metric combining new connections, active connections, bandwidth, rule evaluations. Typical LND node: ~10-20 LCU/month.

# 11. Complete LND Node Cost Model

## 11.1 Self-Managed VM (Single Region, us-east-1/us-central1/East US)

| Component | AWS | GCP (Premium) | GCP (Standard) | Azure |
|-----------|-----|---------------|----------------|-------|
| **Compute** (m6i.large / n2-standard-2 / D4s_v3, 730h) | $67.89 | $52.56 | $52.56 | $63.51 |
| **Disk** (100 GB gp3/Balanced/Premium v2, 3000 IOPS) | $8.00 | $10.00 | $10.00 | $7.50 |
| **Snapshots** (daily incremental, 30-day retention) | $5.00 | $5.00 | $5.00 | $5.00 |
| **Load Balancer** (NLB/TCP LB/Standard LB) | $18.00 | $18.00 | $18.00 | $18.00 |
| **Egress** (1 TB to internet) | $90.00 | $120.00 | $80.00 | $87.00 |
| **Cross-AZ** (500 GB gossip) | $5.00 | Free | Free | Free |
| **Cross-Region Backup** (100 GB to EU) | $2.00 | $8.00 | $8.00 | $5.00 |
| **Logs** (6 GB/month) | $3.20 | $3.20 | $3.20 | $13.80 |
| **Bucket** (150 GB, lifecycle) | $1.20 | $1.00 | $1.00 | $0.90 |
| **Total (On-Demand)** | **$202.29** | **$217.76** | **$177.76** | **$200.21** |
| **With 1-Year Savings/Commit** | **~$150** | **~$155 / ~$115** | **~$115** | **~$145** |

## 11.2 Cost Breakdown by Category

| Category | AWS | GCP (Premium) | GCP (Standard) | Azure |
|----------|-----|---------------|----------------|-------|
| **Compute + Disk** | 37% | 29% | 35% | 35% |
| **Network (Egress + Cross-AZ + Cross-Region)** | 48% | 59% | 49% | 46% |
| **Storage (Snapshots + Bucket)** | 4% | 4% | 4% | 4% |
| **Load Balancer** | 9% | 8% | 10% | 9% |
| **Logs** | 2% | 1% | 2% | 7% |

## 11.3 Kubernetes (EKS/GKE/AKS) - 3 Worker Nodes

| Component | AWS EKS | GCP GKE | Azure AKS |
|-----------|---------|---------|-----------|
| **Control Plane** | $73.00 | $73.00 (Standard) / ~$10-20/pod (Autopilot) | Free |
| **Worker Nodes** (3× m6i.large/n2-standard-2/D4s_v3) | $203.67 | $157.68 | $190.53 |
| **Load Balancer** | $18.00 | $18.00 | $18.00 |
| **Egress** (1 TB) | $90.00 | $120.00 / $80.00 | $87.00 |
| **Total** | **$384.67** | **$368.68 / $328.68** | **$295.53** |

# 12. Cost Optimization Checklist for LND

## 12.1 Immediate (No Architecture Change)

- [ ] Enable **S3/Blob/GCS lifecycle policies** (Hot → IA → Glacier)
- [ ] Set **log retention to 30 days** (export older to object storage)
- [ ] Enable **cross-zone load balancing only where needed** (AWS: $0.01/GB)
- [ ] Use **GCP Standard Tier** for backup/replication traffic (33% egress savings)
- [ ] **Compress backups** before upload (gzip/zstd: 60-80% reduction)
- [ ] Use **incremental snapshots** (default for all providers)

## 12.2 Architecture Changes (Require Planning)

- [ ] **Right-size instances** based on CPU/memory utilization (Compute Optimizer/Recommender/Advisor)
- [ ] **Move to Reserved/Committed Use** (30-40% compute savings)
- [ ] **Use Spot/Preemptible** for stateless components (watchtowers, backup workers)
- [ ] **Graviton/ARM instances** (20-40% better price/performance on AWS/GCP)
- [ ] **Private connectivity** (DX/Interconnect/ER) for sustained >10 Gbps cross-region
- [ ] **Regional MIG / VMSS / ASG** for HA without cross-zone data charges

## 12.3 Advanced (Multi-Cloud / Hybrid)

- [ ] **GCP Standard Tier** for all backup/replication egress
- [ ] **Azure** for lowest cross-zone/cross-region + fastest DB failover
- [ ] **GCP Spanner** if strong consistency multi-region required
- [ ] **Direct Connect/Interconnect/ExpressRoute** for on-premises hybrid

# References

[1] AWS, "Data Transfer Pricing," https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer
[2] AWS, "S3 Pricing," https://aws.amazon.com/s3/pricing/
[3] AWS, "EBS Pricing," https://aws.amazon.com/ebs/pricing/
[4] AWS, "CloudWatch Pricing," https://aws.amazon.com/cloudwatch/pricing/
[5] AWS, "Data Lifecycle Manager," https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
[6] Google Cloud, "Network Pricing," https://cloud.google.com/vpc/network-pricing
[7] Google Cloud, "Cloud Storage Pricing," https://cloud.google.com/storage/pricing
[8] Google Cloud, "Persistent Disk Pricing," https://cloud.google.com/compute/disks-image-pricing
[9] Google Cloud, "Logging Pricing," https://cloud.google.com/logging/pricing
[10] Google Cloud, "Network Tiers," https://cloud.google.com/vpc/docs/network-tiers
[11] Microsoft, "Bandwidth Pricing," https://azure.microsoft.com/pricing/details/bandwidth/
[12] Microsoft, "Blob Storage Pricing," https://azure.microsoft.com/pricing/details/storage/blobs/
[13] Microsoft, "Managed Disks Pricing," https://azure.microsoft.com/pricing/details/managed-disks/
[14] Microsoft, "Monitor Pricing," https://azure.microsoft.com/pricing/details/monitor/
[15] Microsoft, "Storage Account Lifecycle," https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview

# Appendices

## A. Monthly Cost Calculator (Per GB)

| Path | AWS | GCP (Premium) | GCP (Standard) | Azure |
|------|-----|---------------|----------------|-------|
| **Ingress** | $0.000 | $0.000 | $0.000 | $0.000 |
| **Egress (Internet)** | $0.090 | $0.120 | $0.080 | $0.087 |
| **Cross-AZ** | $0.010 | $0.000 | $0.000 | $0.000 |
| **Cross-Region (Intra-Continent)** | $0.020 | $0.010 | $0.010 | $0.020 |
| **Cross-Region (Inter-Continent)** | $0.090 | $0.080-0.140 | $0.080-0.140 | $0.050-0.120 |
| **Inter-Cloud (Effective)** | $0.090 | $0.120 | $0.080 | $0.087 |
| **Private Connect (On-Prem)** | $0.020 | $0.020 | $0.020 | $0.025 |

## B. Annual Cost Projection (LND Node, 1 TB Egress/Month)

| Configuration | Year 1 | Year 2 | Year 3 | 3-Year Total |
|---------------|--------|--------|--------|--------------|
| **AWS On-Demand** | $2,427 | $2,427 | $2,427 | $7,281 |
| **AWS 1-Year RI** | $1,800 | $1,800 | $1,800 | $5,400 |
| **GCP Premium On-Demand** | $2,613 | $2,613 | $2,613 | $7,839 |
| **GCP Standard On-Demand** | $2,133 | $2,133 | $2,133 | $6,399 |
| **GCP 1-Year CUD** | $1,380 | $1,380 | $1,380 | $4,140 |
| **Azure On-Demand** | $2,403 | $2,403 | $2,403 | $7,209 |
| **Azure 1-Year RI** | $1,740 | $1,740 | $1,740 | $5,220 |

> **Assumptions**: 1 TB egress/mo, 100 GB disk, 150 GB bucket, 6 GB logs, m6i.large/n2-standard-2/D4s_v3. RI/CUD = 1-year no-upfront.

## C. Pricing API Endpoints (For Automation)

| Provider | API | Documentation |
|----------|-----|---------------|
| **AWS** | Price List API (Bulk) / GetProducts | https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html |
| **GCP** | Cloud Billing Catalog API | https://cloud.google.com/billing/docs/reference/rest |
| **Azure** | Retail Prices API | https://learn.microsoft.com/rest/api/cost-management/retail-prices |

## D. Cost Anomaly Detection

| Provider | Tool | Alert Types |
|----------|------|-------------|
| **AWS** | Cost Anomaly Detection (ML-based) | Spend spike, new service, usage pattern change |
| **GCP** | Budget Alerts + Recommender | Budget threshold, commitment utilization, idle resources |
| **Azure** | Cost Management Alerts + Advisor | Budget threshold, reservation utilization, right-sizing |