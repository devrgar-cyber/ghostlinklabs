# syntax=docker/dockerfile:1.6
FROM python:3.11-slim

# Create non-root user
ARG USER=ghostlink
ARG UID=10001
RUN useradd -m -u $UID -s /usr/sbin/nologin $USER

# System deps (curl for healthcheck)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy application
COPY gl_controller_metrics.py gl_peer.py gl_openai_bridge.py /app/
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Runtime user
USER $USER

# Expose internal ports (you can use host networking or map these)
EXPOSE 7420/tcp 7422/tcp 9108/tcp

# Healthcheck: /metrics should be reachable once controller is up
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=5 \
  CMD curl -fsS http://127.0.0.1:9108/metrics >/dev/null || exit 1

# Environment flags
ENV RUN_CONTROLLER=1 \
    RUN_PEER=0 \
    RUN_BRIDGE=0 \
    HOST=127.0.0.1 \
    GL_MODEL=gpt-4.1-mini

ENTRYPOINT ["/app/entrypoint.sh"]
