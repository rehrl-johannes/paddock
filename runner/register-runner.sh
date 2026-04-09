#!/bin/sh
set -e

REG_TOKEN=$(curl -s -X POST -H "Authorization: token ${GITHUB_PAT}" https://api.github.com/repos/${REPO_NAME}/actions/runners/registration-token | jq -r .token)

# Configure the runner
/actions-runner/config.sh \
  --url "https://github.com/${REPO_NAME}" \
  --token "${REG_TOKEN}" \
  --name "${RUNNER_NAME}" \
  --work _work \
  --unattended \
  --replace

# Run the runner
exec /actions-runner/run.sh