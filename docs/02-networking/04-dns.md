---
title: "DNS Services"
description: "DNS services comparison: Route 53, Cloud DNS, Azure DNS — private zones, split horizon, health checks, traffic routing, hybrid DNS"
tags: [dns, route53, cloud-dns, azure-dns, private-zones, split-horizon, hybrid-dns]
cloud: all
level: 300
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS Route 53 Documentation"
  - "Google Cloud DNS Documentation"
  - "Azure DNS Documentation"
---

# Abstract

Comparison of DNS services across AWS Route 53, Google Cloud DNS, and Azure DNS including public/private zones, split horizon, health checks, traffic routing, and hybrid DNS.

# 1. DNS Service Comparison

| Feature | AWS Route 53 | GCP Cloud DNS | Azure DNS |
|---------|--------------|---------------|-----------|
| **Type** | Authoritative + Recursive (Resolver) | Authoritative | Authoritative + Recursive (Private Resolver) |
| **Public Zones** | Yes | Yes | Yes |
| **Private Zones** | Yes (VPC-associated) | Yes (VPC networks) | Yes (VNet-linked) |
| **Split Horizon** | Yes (views) | Yes (private zones + forwarding) | Yes (private resolver) |
| **Health Checks** | Yes (TCP/HTTP/HTTPS, CloudWatch) | Yes (integrated with Cloud LB) | Yes (Private Resolver + Front Door) |
| **Traffic Routing** | Latency, Geo, Weighted, Failover, Multivalue | Geo, Weighted (via LB) | Priority, Weighted, Geographic (Front Door) |
| **DNSSEC** | Yes (signing + validation) | Yes (signing + validation) | Yes (signing + validation) |
| **Logging** | Query Logging (CloudWatch, S3) | Query Logging (Cloud Logging) | Diagnostic Logs (Log Analytics) |
| **Private Resolver** | Route 53 Resolver (inbound/outbound endpoints) | Cloud DNS Forwarding (peering + policies) | Azure Private Resolver (inbound/outbound) |
| **Hybrid DNS** | Resolver + DHCP Options | DNS Forwarding + Peering | Private Resolver + Custom DNS |
| **Cost (per zone/month)** | $0.50 | $0.20 | $0.50 |
| **Cost (per million queries)** | $0.40 | $0.40 | $0.40 |

# 2. Private DNS Resolution Patterns

## 2.1 AWS Route 53 Resolver

- **Inbound Endpoint**: On-premises → AWS private zones
- **Outbound Endpoint**: AWS → on-premises / external DNS
- **Rules**: Conditional forwarding (domain → target IPs)
- **Cost**: $0.125/hour/endpoint + $0.0004/million queries

## 2.2 GCP Cloud DNS Forwarding

- **Forwarding Zones**: Domain → target name servers (via VPN/Interconnect)
- **Peering Zones**: Private zone peering (send queries to peer VPC)
- **Server Policies**: Alternative name servers for VPC
- **Cost**: Included in Cloud DNS pricing

## 2.3 Azure Private Resolver

- **Inbound Endpoint**: On-premises → Azure private zones
- **Outbound Endpoint**: Azure → on-premises / external DNS
- **Rulesets**: Forwarding rules (domain → DNS servers)
- **Cost**: $0.10/hour/endpoint + $0.0004/million queries

# References

[1] AWS, "Route 53 Documentation," https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/
[2] Google Cloud, "Cloud DNS Documentation," https://cloud.google.com/dns/docs
[3] Microsoft, "Azure DNS Documentation," https://learn.microsoft.com/azure/dns/
