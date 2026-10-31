# Example fixture image, not the user's complete deployment toolbox.
# Pin the resulting image ID/digest in an experiment manifest.
FROM node:22.23.4-bookworm-slim AS node
FROM ubuntu:24.04

ARG PI_VERSION=1.3.0
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates bash coreutils findutils grep ripgrep fd-find jq tar sqlite3 python3 libstdc++6 libatomic1 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=node /usr/local/ /usr/local/
RUN npm install --global --no-audit --no-fund --save-exact \
    @earendil-works/pi-coding-agent@${PI_VERSION} \
    && npm cache clean --force \
    && mkdir -p /workspace /skills /home/worker \
    && chmod 1777 /workspace /home/worker
ENV HOME=/home/worker \
    PI_CODING_AGENT_DIR=/home/worker/.pi/agent \
    PI_OFFLINE=1 \
    PI_SKIP_VERSION_CHECK=1
USER 10001:10001
WORKDIR /workspace
CMD ["pi", "--version"]
