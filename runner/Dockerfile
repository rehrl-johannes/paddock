FROM ubuntu:latest

ARG ARCHITECTURE=arm64
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
    libcurl4t64 \
    libunwind8 \
    libuuid1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /actions-runner

RUN if [ "$ARCHITECTURE" = "x64" ]; then \
        curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.334.0/actions-runner-linux-x64-2.334.0.tar.gz && \
        echo "048024cd2c848eb6f14d5646d56c13a4def2ae7ee3ad12122bee960c56f3d271  actions-runner.tar.gz" | sha256sum -c; \
    elif [ "$ARCHITECTURE" = "arm64" ]; then \
        curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.334.0/actions-runner-linux-arm64-2.334.0.tar.gz && \
        echo "f44255bd3e80160eb25f71bc83d06ea025f6908748807a584687b3184759f7e4  actions-runner.tar.gz" | sha256sum -c; \
    elif [ "$ARCHITECTURE" = "arm" ]; then \
        curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.334.0/actions-runner-linux-arm-2.334.0.tar.gz && \
        echo "84a25196caf971d0c634e32864731e773e1668235f799666fc0ec40ac666a0ab  actions-runner.tar.gz" | sha256sum -c; \
    fi

RUN tar xzf ./actions-runner.tar.gz

RUN useradd -m runner
COPY register-runner.sh /home/runner/register-runner.sh
RUN chmod +x /home/runner/register-runner.sh

USER runner
WORKDIR /home/runner

CMD [ "./register-runner.sh" ]