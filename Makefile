# Makefile for LND Cloud Platform Guide
# Professional documentation build & validation

.PHONY: setup dev build lint test deploy deploy-preview check-refs check-figures check-listings check-frontmatter clean

# Python & MkDocs
PYTHON := python3
PIP := pip3
MKDOCS := mkdocs

# Directories
DOCS_DIR := docs
TEMPLATES_DIR := templates
SCRIPTS_DIR := scripts
ASSETS_DIR := assets

# Setup
setup:
	@echo "Installing Python dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-mermaid2-plugin mkdocs-macros-plugin pymdown-extensions
	$(PIP) install markdownlint-cli vale codespell markdown-link-check
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "Setup complete!"

# Development server
dev:
	$(MKDOCS) serve --dev-addr=0.0.0.0:8000 --dirtyreload

# Production build
build:
	$(MKDOCS) build --strict --clean --verbose

# Linting
lint: check-frontmatter check-listings check-refs check-figures
	@echo "Running markdownlint..."
	markdownlint $(DOCS_DIR) --config .markdownlint.json
	@echo "Running vale..."
	vale $(DOCS_DIR)
	@echo "Running codespell..."
	codespell $(DOCS_DIR) --skip=".git,assets"
	@echo "Running linkcheck..."
	markdown-link-check -c .linkcheck.json $(DOCS_DIR)/**/*.md
	@echo "All lint checks passed!"

# Test alias
test: lint

# Deploy to GitHub Pages
deploy:
	$(MKDOCS) gh-deploy --force --clean

# Deploy preview (Netlify/Cloudflare - requires config)
deploy-preview:
	@echo "Configure NETLIFY_AUTH_TOKEN and NETLIFY_SITE_ID for Netlify"
	@echo "Or configure CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID for Cloudflare Pages"
	@echo "See .github/workflows/deploy-preview.yml"

# Validation: Cross-references
check-refs:
	@echo "Validating cross-references..."
	@$(PYTHON) $(SCRIPTS_DIR)/check_refs.py $(DOCS_DIR)

# Validation: Mermaid diagrams
check-figures:
	@echo "Checking Mermaid diagrams..."
	@$(PYTHON) $(SCRIPTS_DIR)/check_figures.py $(DOCS_DIR)

# Validation: Code listings
check-listings:
	@echo "Checking code block language tags..."
	@$(PYTHON) $(SCRIPTS_DIR)/check_listings.py $(DOCS_DIR)

# Validation: Frontmatter
check-frontmatter:
	@echo "Validating frontmatter..."
	@$(PYTHON) $(SCRIPTS_DIR)/check_frontmatter.py $(DOCS_DIR)

# Clean build artifacts
clean:
	rm -rf site/
	rm -rf .mkdocs_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# New document from template
new-guide:
	@read -p "Section (e.g., 04-compute): " section; \
	read -p "Topic (e.g., aws-ec2-gp3): " topic; \
	read -p "Title: " title; \
	cp $(TEMPLATES_DIR)/guide-template.md $(DOCS_DIR)/$$section/$$topic.md; \
	sed -i "s/\[Guide Title: Cloud Provider + Service + LND Context\]/$$title/" $(DOCS_DIR)/$$section/$$topic.md; \
	sed -i "s/YYYY-MM-DD/$$(date +%Y-%m-%d)/" $(DOCS_DIR)/$$section/$$topic.md; \
	echo "Created $(DOCS_DIR)/$$section/$$topic.md"

new-tutorial:
	@read -p "Cloud (aws/gcp/azure): " cloud; \
	read -p "Compute (vm/eks/gke/aks/lambda/cloudrun/containerapps): " compute; \
	read -p "Title: " title; \
	cp $(TEMPLATES_DIR)/tutorial-template.md $(DOCS_DIR)/12-tutorials/$$cloud-$$compute-lnd.md; \
	sed -i "s/\[Tutorial: Deploy LND on Cloud Provider + Compute Type\]/$$title/" $(DOCS_DIR)/12-tutorials/$$cloud-$$compute-lnd.md; \
	sed -i "s/YYYY-MM-DD/$$(date +%Y-%m-%d)/" $(DOCS_DIR)/12-tutorials/$$cloud-$$compute-lnd.md; \
	echo "Created $(DOCS_DIR)/12-tutorials/$$cloud-$$compute-lnd.md"

new-reference:
	@read -p "Cloud (aws/gcp/azure/all): " cloud; \
	read -p "Service Category (e.g., compute-limits): " service; \
	read -p "Title: " title; \
	cp $(TEMPLATES_DIR)/reference-template.md $(DOCS_DIR)/11-reference/$$cloud-$$service.md; \
	sed -i "s/\[Reference: Cloud Provider + Service Category\]/$$title/" $(DOCS_DIR)/11-reference/$$cloud-$$service.md; \
	sed -i "s/YYYY-MM-DD/$$(date +%Y-%m-%d)/" $(DOCS_DIR)/11-reference/$$cloud-$$service.md; \
	echo "Created $(DOCS_DIR)/11-reference/$$cloud-$$service.md"
