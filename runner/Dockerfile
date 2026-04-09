FROM ubuntu:latest

ARG ARCHITECTURE=ARM64

ARG GITHUB_PAT
ENV GITHUB_PAT=$GITHUB_PAT

ARG REPO_NAME
ENV REPO_NAME=$REPO_NAME

ARG RUNNER_NAME
ENV RUNNER_NAME=$RUNNER_NAME

RUN apt update -y && apt upgrade -y && apt install -y  \
    curl  \
    ca-certificates  \
    gnupg2  \
    tar  \
    jq \
    libicu-dev \
    libssl-dev \
    libkrb5-3 \
    zlib1g \
    libcurl4 \
    libunwind8 \
    libuuid1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /actions-runner

RUN curl -o actions-runner-linux-arm64-2.333.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.333.1/actions-runner-linux-arm64-2.333.1.tar.gz
RUN echo "69ac7e5692f877189e7dddf4a1bb16cbbd6425568cd69a0359895fac48b9ad3b  actions-runner-linux-arm64-2.333.1.tar.gz" | sha256sum -c
RUN tar xzf ./actions-runner-linux-arm64-2.333.1.tar.gz

RUN useradd -m runner

COPY register-runner.sh /home/runner/register-runner.sh
RUN chmod +x /home/runner/register-runner.sh

USER runner
WORKDIR /home/runner

CMD [ "./register-runner.sh" ]