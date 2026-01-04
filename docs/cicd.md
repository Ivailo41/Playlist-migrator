# Purpose and Scope
This document describes the CI/CD pipeline for this project. It automates testing and container creation of the backend application.

The primary goals of the pipeline are:
- Detect early build and integration issues
- Consistent and reproducable Docker Images
- Separation between development and release workflows

# High-Level Overview
**develop branch**
```
Code push -> Lint -> Security check -> Build Dev Docker image
          └─ Unit tests
```
**main branch** (Requires successfuly passed tests and image build, accepts PRs only from dev branch)
```
Code merge -> Code check -> Build Prod Docker image
```

# Workflow Structure
The CI/CD workflows are located in the following directory:
```
.github/
└─ workflows/
   ├─ server-ci-dev.yml
   └─ server-ci-prod.yml
```
# Branch-Based Pipeline Behavior

### Develop branch
The pipeline on the dev branch is triggered on every push or PR. Pull requests are required to have passed the lint, unit-tests and security-scan jobs before merge and direct pushes are allowed as the project is developed by a single developer and more complex rules would only cause confusion.

>In the future the project may make use of separate branches per feature and locking the direct pushes to the "develop" branch.

### Main branch
The pipeline on the main branch is triggered only on pull requests. Direct pushes to the branch are blocked and merging requires successful tests pass and image build.

# Image Build and Tagging Strategy
Different tags are used depending on the branch:

### Development builds:
- `server:develop`

### Production builds:
- `server:latest`

# Failure Handling and Observability
The pipeline is designed to fail fast:

- Test failures stop the pipeline immediately
- Docker build failures prevent image publication
- Deployment steps run only after successful builds

All pipeline logs and execution details are available in the GitHub Actions interface, providing full visibility into failures and execution history.

# Pipelines Workflow
There are 2 workflow files that describe the jobs after code push or PR to both branches.
 Both have restricted permisions that allows the actions to only read contents

### server-ci-develop.yml
Jobs:
- lint - Formats code and runs style checks using `Black` and `Flake8`
- unit-tests - Runs unit tests paralel with **lint**
- security-scan - Uses `Trivy` to run file system security check
- build-server-dev-image - Builds Docker dev image, runs security scan with `Trivy` and pushes it to the registry

### server-ci-prod.yml
Jobs:
- build-server-prod-image - Builds Docker production image, runs security scan with `Trivy` and pushes it to the registry