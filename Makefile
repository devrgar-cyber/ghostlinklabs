# Quick ops
.PHONY: env ctl peer bridge sanity

env:
\t@echo "HOST=$${HOST:-10.7.0.1} PORT=$${PORT:-7420} PROM=$${PROMETHEUS_BIND:-127.0.0.1:9108}"

ctl:
\tpython3 gl_controller_metrics_env.py

peer:
\tpython3 gl_peer.py

bridge:
\tOPENAI_API_KEY=$$OPENAI_API_KEY python3 gl_openai_bridge.py

sanity:
\tbash gl_sanity_check.sh
