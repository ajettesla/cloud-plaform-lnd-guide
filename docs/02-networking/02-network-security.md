---
title: "Network Security: VPN, SD-WAN, Peering, PrivateLink"
description: "Network security comparison: VPN, SD-WAN, MPLS, VPC peering, PrivateLink/PSC/Private Endpoint across AWS, GCP, Azure"
tags: [vpn, sdwan, mpls, peering, privatelink, psc, private-endpoint, network-security]
cloud: all
level: 300
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS VPN Documentation"
  - "Google Cloud VPN Documentation"
  - "Azure VPN Gateway Documentation"
---

# Abstract

Network security comparison covering VPN (Site-to-Site, Client), SD-WAN, MPLS/private connectivity, VPC peering, and private service access across AWS, GCP, and Azure.

# 1. VPN Services

## 1.1 AWS VPN

| Type | Specification |
|------|---------------|
| **Site-to-Site VPN** | IPsec (IKEv1/v2), AES-128/256, SHA-1/2, DH Groups 2/14/24. 1.25 Gbps per tunnel. Active/Active (BGP). $0.05/hour/tunnel + data out. |
| **Client VPN** | OpenVPN-based, SAML/OIDC/AD auth, MFA, split-tunnel, $0.10/hour/connection + $0.05/GB. |
| **VPN CloudHub** | Hub-and-spoke for multiple on-prem sites. |

## 1.2 GCP Cloud VPN

| Type | Specification |
|------|---------------|
| **HA VPN** | 99.99% SLA, 2 VPN gateways per region, 3 Gbps per tunnel, BGP/Static routing, IPsec (IKEv2). $0.06/hour/gateway + data out. |
| **Classic VPN** | Single gateway, 3 Gbps, static routes only. Deprecated for new deployments. |
| **Partner Interconnect** | VPN as a service via partners (e.g., Cisco, Fortinet). |

## 1.3 Azure VPN Gateway

| Type | Specification |
|------|---------------|
| **Site-to-Site** | IPsec/IKEv2, Active/Active (BGP), up to 10 Gbps (VpnGw1-5). $0.04-$0.86/hour + data out. |
| **Point-to-Site** | OpenVPN, IKEv2, SSTP. RADIUS/Entra ID auth. $0.03/hour/connection. |
| **ExpressRoute + VPN** | Failover, encryption over ExpressRoute. |

# 2. SD-WAN Integration

| Provider | Native SD-WAN | Partner Integration |
|----------|---------------|---------------------|
| **AWS** | AWS Cloud WAN (managed WAN) | Transit Gateway Connect (Cisco, Aviatrix, Aruba, Fortinet, Versa) |
| **GCP** | Network Connectivity Center (hub/spoke) | Partner Interconnect (Cisco, Fortinet, Palo Alto, Versa) |
| **Azure** | Virtual WAN (hub, secured hub) | Virtual WAN partners (Cisco, Fortinet, Palo Alto, Aruba, Versa, Barracuda) |

### AWS Cloud WAN
- **Core Network**: Global network backbone managed by AWS
- **Segments**: Logical isolation (prod, dev, security)
- **Attachments**: VPC, VPN, Direct Connect, Cloud WAN Connect (SD-WAN)
- **Routing**: Centralized policy, segment routing
- **Cost**: $0.075/hour per attachment + $0.02/GB

### Azure Virtual WAN
- **Hub Types**: Basic (VPN only), Standard (VPN + ExpressRoute + P2S + Firewall + NVA)
- **Secured Hub**: Azure Firewall + Firewall Manager policy
- **Routing**: BGP, custom routes, NVA integration
- **Global**: Hub-to-hub mesh across regions
- **Cost**: Standard hub $0.25/hour + $0.02/GB

### GCP Network Connectivity Center
- **Hub-and-Spoke**: VPC spokes, hybrid spokes (VPN, Interconnect, third-party)
- **Mesh**: Spoke-to-spoke via hub
- **Policy**: Route advertisement, firewall integration
- **Cost**: $0.01/hour per spoke + data processing

# 3. MPLS and Private Connectivity

| Feature | AWS Direct Connect | GCP Cloud Interconnect | Azure ExpressRoute |
|---------|-------------------|------------------------|-------------------|
| **Layer** | Layer 2 (VLAN) / Layer 3 (BGP) | Layer 2 (VLAN) / Layer 3 (BGP) | Layer 3 (BGP) |
| **Bandwidth** | 1/10/100 Gbps (Dedicated), 50 Mbps-10 Gbps (Hosted) | 10/100 Gbps (Dedicated), 50 Mbps-10 Gbps (Partner) | 50 Mbps - 100 Gbps (Direct: 10/100 Gbps) |
| **Redundancy** | Dual connections, diverse paths | Dual connections, diverse paths | Active/Active (ExpressRoute), Zone-redundant |
| **Global Reach** | DX Gateway + TGW | NCC + Interconnect | ExpressRoute Global Reach |
| **Encryption** | MACsec (10/100 Gbps), IPsec over DX | MACsec (Dedicated), IPsec over Partner | MACsec (Direct), IPsec over ExpressRoute |
| **SLA** | 99.99% (Dedicated) | 99.99% (Dedicated HA) | 99.95% (Standard), 99.99% (Direct) |
| **Cost Model** | Port-hour + data out | Port-hour + data out | Port-hour + data out |

# 4. VPC Peering and Private Connectivity

See [06-vpc-peering.md](06-vpc-peering.md) for detailed VPC peering and PrivateLink/PSC/Private Endpoint comparison.

# References

[1] AWS, "VPN Documentation," https://docs.aws.amazon.com/vpn/
[2] Google Cloud, "Cloud VPN Documentation," https://cloud.google.com/vpn/docs
[3] Microsoft, "VPN Gateway Documentation," https://learn.microsoft.com/azure/vpn-gateway/
[4] AWS, "Cloud WAN Documentation," https://docs.aws.amazon.com/cloudwan/
[5] Microsoft, "Virtual WAN Documentation," https://learn.microsoft.com/azure/virtual-wan/
[6] Google Cloud, "Network Connectivity Center," https://cloud.google.com/network-connectivity/docs/network-connectivity-center/overview
