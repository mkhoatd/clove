# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Clove project.

## Workflows

### 1. Build and Publish to PyPI (`build-and-publish.yml`)
This workflow builds and publishes the Python package to PyPI and TestPyPI.
- Triggers on release creation or manual workflow dispatch
- Builds the frontend and Python wheel
- Publishes to PyPI on releases
- Can publish to TestPyPI for testing

### 2. Docker Build and Push (`docker-publish.yml`)
This workflow builds Docker images and pushes them to both Docker Hub and GitHub Container Registry (GHCR).

#### Features:
- Multi-platform builds (linux/amd64, linux/arm64)
- Pushes to both Docker Hub and GHCR
- Security scanning with Trivy
- Automatic tagging based on branches and semantic versions

#### Docker Hub Images:
- Repository: `mirrorange/clove`
- Requires secrets: `DOCKER_HUB_USERNAME` and `DOCKER_HUB_TOKEN`

#### GitHub Container Registry Images:
- Repository: `ghcr.io/{owner}/clove` (automatically uses repository owner)
- Uses built-in `GITHUB_TOKEN` for authentication
- No additional secrets required

#### Tags:
- `latest`: Always points to the latest main branch build
- `main`: Latest main branch build
- `vX.Y.Z`: Semantic version tags
- `vX.Y`: Major.minor version tags
- `vX`: Major version tags
- `pr-N`: Pull request builds (not pushed)

## Usage

### Pulling Images

#### From Docker Hub:
```bash
docker pull mirrorange/clove:latest
```

#### From GitHub Container Registry:
```bash
docker pull ghcr.io/{owner}/clove:latest
```

Replace `{owner}` with the actual GitHub repository owner name.

### Running the Container:
```bash
# Using Docker Hub image
docker run -d -p 5201:5201 -v ./data:/data mirrorange/clove:latest

# Using GHCR image
docker run -d -p 5201:5201 -v ./data:/data ghcr.io/{owner}/clove:latest
```

## Security

Both workflows include security scanning using Trivy, which:
- Scans built images for vulnerabilities
- Reports results to GitHub Security tab
- Helps maintain secure container images