# AGENTS.md - LND Cloud Platform Guide

## Purpose
Professional technical documentation (IEEE/Overleaf style) for deploying Lightning Network Daemon on AWS, GCP, and Azure. Every document follows structured format with cross-references, diagrams, and validated code.

---

## Developer Commands

```bash
# Environment setup
make setup              # Install Python deps, pre-commit hooks
make dev                # mkdocs serve --dev-addr=0.0.0.0:8000
make build              # mkdocs build --strict --clean
make lint               # markdownlint + vale + cspell + linkcheck
make test               # Run all lint checks
make deploy             # mkdocs gh-deploy --force (GitHub Pages)
make deploy-preview     # Deploy to preview (Netlify/Cloudflare)

# Content validation
make check-refs         # Validate cross-references [§XX.Y]
make check-figures      # Verify Mermaid diagrams render
make check-listings     # Validate code blocks have language tags
make check-frontmatter  # Ensure all docs have required frontmatter
```

---

## Document Conventions

### Frontmatter (Required on Every Page)

```yaml
---
title: "[Descriptive Title: Cloud + Service + Context]"
description: "[One sentence, <160 chars, includes cloud, service, outcome]"
tags: [cloud, service, lnd, pattern, level]  # lowercase, hyphenated
cloud: [aws|gcp|azure|all]                   # Target cloud(s)
level: [100|200|300|400]                     # 100=intro, 400=expert
version: "1.0"                               # Semantic version
date: YYYY-MM-DD                             # ISO 8601
authors: ["Author Name"]                     # Array
references:                                  # Numbered refs for IEEE style
  - "Official Doc URL"
  - "LND Guide vX.Y"
---
```

### Heading Hierarchy

- `#` Document title (auto from frontmatter)
- `##` Major sections (1-10)
- `###` Subsections
- `####` Details (max depth)
- Never skip levels

### Cross-Reference Notation (Mandatory)

| Target | Syntax | Example |
|--------|--------|---------|
| Section | `[§XX.Y]` | `[§04.2]` → AWS EC2 |
| Figure | `[Figure N]` | `[Figure 3]` |
| Table | `[Table N]` | `[Table 2]` |
| Equation | `[Eq. N]` | `[Eq. 1]` |
| Code Listing | `[Listing N]` | `[Listing 4]` |
| Algorithm | `[Algorithm N]` | `[Algorithm 1]` |
| Appendix | `[Appendix X]` | `[Appendix A]` |

**Rule**: Every cross-reference must resolve to an existing anchor. Run `make check-refs` before commit.

### Code Blocks

```markdown
```bash
# Always specify language
command --flag value
```

```hcl
# Terraform/HCL
resource "type" "name" { }
```

```yaml
# YAML/Config
key: value
```

```mermaid
# Diagrams - always include caption
graph TB
    A --> B
```
**Figure N:** Caption describing diagram.
```

### Tabbed Code (Multi-Cloud)

```markdown
=== "AWS"
    ```bash
    aws ec2 describe-instances
    ```

=== "GCP"
    ```bash
    gcloud compute instances list
    ```

=== "Azure"
    ```bash
    az vm list
    ```
```

### Admonitions

```markdown
!!! note "Prerequisite"
    Required before proceeding.

!!! warning "Production Only"
    Do not run in production without review.

!!! danger "Data Loss Risk"
    Irreversible operation.

!!! tip "Cost Optimization"
    Use spot instances for 70% savings.
```

---

## Content Templates

Use templates in `templates/`:
- `guide-template.md` - Full IEEE guide (architecture → implementation → ops)
- `tutorial-template.md` - Step-by-step with validation checkpoints
- `reference-template.md` - Quick reference (limits, pricing, CLI, Terraform)

**Never create new docs from scratch.** Copy template, rename, fill in.

---

## Git Workflow

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Documentation | `docs/<section>-<topic>` | `docs/04-compute-aws-ec2-gp3` |
| Feature | `feat/<section>-<topic>` | `feat/10-lnd-watchtower-gcp` |
| Fix | `fix/<section>-<issue>` | `fix/03-networking-nlb-health-check` |
| Refactor | `refactor/<section>-<topic>` | `refactor/11-reference-cli-update` |

### Commit Messages (Conventional Commits)

```
<type>(<section>): <description>

[optional body]

[optional footer]
```

Types: `docs`, `feat`, `fix`, `refactor`, `style`, `test`, `chore`

Examples:
```
docs(04-compute): add GCP Confidential VM guide
feat(10-lnd): implement watchtower deployment for AWS
fix(03-networking): correct NLB health check path
refactor(11-reference): update pricing tables for 2026
```

### Pull Requests

- Target: `main` (protected)
- Required checks: `lint`, `build`, `linkcheck`
- Preview deployment auto-created
- Minimum 1 approval for docs, 2 for architecture changes
- Squash merge, delete branch

---

## Quality Gates (Pre-Commit)

```yaml
# .pre-commit-config.yaml (enforced)
repos:
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.41.0
    hooks:
      - id: markdownlint
        args: ["--config", ".markdownlint.json"]
  - repo: https://github.com/errata-ai/vale
    rev: v3.5.0
    hooks:
      - id: vale
  - repo: https://github.com/codespell-project/codespell
    rev: v2.2.6
    hooks:
      - id: codespell
        args: ["--skip", ".git,assets"]
  - repo: local
    hooks:
      - id: check-refs
        name: Validate Cross-References
        entry: python scripts/check_refs.py
        language: system
        files: \.md$
      - id: check-frontmatter
        name: Validate Frontmatter
        entry: python scripts/check_frontmatter.py
        language: system
        files: \.md$
```

---

## Style Guide (Vale)

```ini
# .vale/styles/LNDCloud/vale.ini
StylesPath = .
MinAlertLevel = warning

[*] 
BasedOnStyles = write-good, proselint
IgnoredClasses = [comment, code, math]

# Custom rules
LNDCloud.TechnologyNames = YES
LNDCloud.CrossRefFormat = YES
LNDCloud.MetricUnits = YES
LNDCloud.CloudTerminology = YES
```

Key rules:
- Use "LND" not "lnd" or "Lnd"
- Use "AWS", "GCP", "Azure" (not "Amazon", "Google Cloud", "Microsoft Azure")
- SI units: "100 GB", "3,000 IOPS", "99.99%"
- Cross-refs: `[§XX.Y]` format mandatory
- No "click here" links - use descriptive text

---

## Diagram Standards (Mermaid)

- Use `graph TB` (top-bottom) for architecture
- Use `sequenceDiagram` for data flows
- Use `flowchart LR` for pipelines
- Nodes: PascalCase, max 20 chars
- Subgraphs for logical grouping (VPC, AZ, Service)
- Colors: Cloud-branded (AWS orange, GCP blue, Azure blue)
- Always include caption: `**Figure N:** Description.`

---

## Table Standards

- Markdown tables with header row
- Align numbers right: `|---:|`
- Units in header: `| IOPS | Cost/mo (USD) |`
- Max 8 columns for readability
- Caption: `**Table N:** Description.`

---

## Image/Screenshot Standards

- Path: `assets/screenshots/<cloud>/<feature>.png`
- Max width: 1600px
- Format: PNG (diagrams), WebP (photos)
- Naming: `<cloud>-<service>-<action>.png`
- Alt text: Descriptive, includes cloud and action
- Reference: `![AWS EC2 LND Deployment](assets/screenshots/aws/ec2-lnd-deploy.png)`

---

## Cloud CLI Versions (Pin in CI)

| Tool | Version | Install |
|------|---------|---------|
| aws-cli | 2.15+ | `pip install awscli` |
| gcloud | 480+ | `curl https://sdk.cloud.google.com | bash` |
| az | 2.55+ | `curl -sL https://aka.ms/InstallAzureCLIDeb | bash` |
| terraform | 1.9+ | `https://releases.hashicorp.com/terraform/` |
| kubectl | 1.29+ | Cloud SDK or standalone |

---

## Review Checklist

Before merging any doc:

- [ ] Frontmatter complete and accurate
- [ ] All cross-references resolve (`make check-refs`)
- [ ] Mermaid diagrams render (`make check-figures`)
- [ ] Code blocks have language tags (`make check-listings`)
- [ ] Tables have captions and aligned numbers
- [ ] Screenshots optimized and in `assets/`
- [ ] Vale passes (`make lint`)
- [ ] Links valid (`make linkcheck`)
- [ ] Spelling clean (`cspell docs/`)
- [ ] Tutorial validated end-to-end (if applicable)

---

## Directory Structure

```
docs/
├── 01-getting-started/     # Foundation
├── 02-identity-access/     # IdP/SP, IAM
├── 03-networking/          # VPC, LB, DNS
├── 04-compute/             # VM, Serverless, K8s
├── 05-storage/             # Block, Object, File
├── 06-database/            # Managed DBs
├── 07-security/            # Secrets, KMS, Compliance
├── 08-observability/       # Logs, Metrics, Traces
├── 09-cicd/                # IaC, Pipelines, GitOps
├── 10-lnd-specific/        # LND deep-dive
├── 11-reference/           # Limits, Pricing, CLI
├── 12-tutorials/           # Step-by-step
templates/                  # Document templates
assets/
  ├── screenshots/          # Cloud-organized
  └── diagrams/             # Source diagrams
scripts/                    # Validation scripts
.github/workflows/          # CI/CD
```

---

## FAQ

**Q: How do I add a new cloud provider?**
A: Add to `cloud:` frontmatter values, create `assets/screenshots/<new>/`, update templates with new tabbed code sections.

**Q: How to handle versioned docs (LND v0.18 vs v0.19)?**
A: Use `mike` plugin for versioning. See `mkdocs.yml` `extra.version.provider: mike`.

**Q: Can I use raw HTML?**
A: Avoid. Use Markdown + extensions. If needed, use `md_in_html` extension sparingly.

**Q: Where do shared Terraform modules live?**
A: Separate repo: `github.com/ajettesla/lnd-terraform-modules`. Reference in docs via `[§11.5]`.

---

## Contact

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Security: See `SECURITY.md`
