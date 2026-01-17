# Observability Setup Guide

**Date:** 2026-01-10  
**Purpose:** Complete guide for setting up Langfuse and OpenTelemetry observability in YBIS

---

## Overview

YBIS supports two observability backends:

1. **Langfuse** - LLM tracing, cost tracking, and analytics
2. **OpenTelemetry** - Distributed tracing for microservices

Both are now **enabled by default** in `configs/profiles/default.yaml`, but require configuration to work.

---

## 1. Langfuse Setup

### What is Langfuse?

Langfuse is an open-source LLM observability platform that provides:
- **LLM call tracing** - Track every LLM API call
- **Cost tracking** - Monitor token usage and costs
- **Latency monitoring** - Track response times
- **Analytics** - Success rates, error analysis
- **Dashboard** - Visual interface for all metrics

### Setup Steps

#### Step 1: Get Langfuse API Keys

**Option A: Use Langfuse Cloud (Recommended for beginners)**

1. Go to [https://cloud.langfuse.com](https://cloud.langfuse.com)
2. Sign up for a free account
3. Create a new project
4. Go to Settings → API Keys
5. Copy your **Public Key** and **Secret Key**

**Option B: Self-Hosted Langfuse**

1. Deploy Langfuse server (Docker, Kubernetes, etc.)
2. Get API keys from your self-hosted instance
3. Note the host URL (default: `https://cloud.langfuse.com`)

#### Step 2: Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:LANGFUSE_PUBLIC_KEY="your-public-key-here"
$env:LANGFUSE_SECRET_KEY="your-secret-key-here"
$env:LANGFUSE_HOST="https://cloud.langfuse.com"  # Optional, default is cloud
```

**Windows (Command Prompt):**
```cmd
set LANGFUSE_PUBLIC_KEY=your-public-key-here
set LANGFUSE_SECRET_KEY=your-secret-key-here
set LANGFUSE_HOST=https://cloud.langfuse.com
```

**Linux/Mac:**
```bash
export LANGFUSE_PUBLIC_KEY="your-public-key-here"
export LANGFUSE_SECRET_KEY="your-secret-key-here"
export LANGFUSE_HOST="https://cloud.langfuse.com"  # Optional
```

**Permanent Setup (`.env` file):**

Create a `.env` file in project root:
```env
LANGFUSE_PUBLIC_KEY=your-public-key-here
LANGFUSE_SECRET_KEY=your-secret-key-here
LANGFUSE_HOST=https://cloud.langfuse.com
```

Then load it:
```bash
# Linux/Mac
source .env

# Windows PowerShell
Get-Content .env | ForEach-Object { $line = $_; if ($line -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') } }
```

#### Step 3: Verify Setup

Run a test workflow:
```bash
python scripts/ybis_run.py T-<task_id> --workflow self_develop
```

Check Langfuse dashboard:
1. Go to [https://cloud.langfuse.com](https://cloud.langfuse.com)
2. Navigate to your project
3. You should see traces appearing in real-time

### What Gets Logged to Langfuse?

- **Workflow traces** - Start/end of workflows
- **LLM calls** - Every LLM API call with:
  - Model name
  - Input prompts
  - Output responses
  - Token usage (prompt, completion, total)
  - Cost (if available)
  - Latency
- **Node execution** - Node start/success/error
- **Errors** - Exception details and stack traces

### Langfuse Dashboard Features

- **Traces** - View all workflow executions
- **Generations** - View all LLM calls
- **Analytics** - Cost, latency, success rate
- **Scores** - Custom scoring and evaluation
- **Datasets** - Test datasets and evaluation

---

## 2. OpenTelemetry Setup

### What is OpenTelemetry?

OpenTelemetry is an open-source observability framework that provides:
- **Distributed tracing** - Track requests across services
- **Span correlation** - Link related operations
- **Multiple exporters** - Jaeger, Zipkin, OTLP, etc.
- **Standard protocol** - Works with many backends

### Setup Steps

#### Step 1: Choose an Exporter

OpenTelemetry supports multiple exporters:

1. **Console Exporter** (Default) - Prints traces to console (for development)
2. **OTLP Exporter** - OpenTelemetry Protocol (works with many backends)
3. **Jaeger Exporter** - Jaeger tracing backend
4. **Zipkin Exporter** - Zipkin tracing backend

#### Step 2: Set Environment Variables

**For Console Exporter (Development):**
```bash
export OTEL_SERVICE_NAME="ybis"
export OTEL_EXPORTER="console"
```

**For OTLP Exporter (Production):**
```bash
export OTEL_SERVICE_NAME="ybis"
export OTEL_EXPORTER="otlp"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"  # OTLP gRPC endpoint
```

**For Jaeger Exporter:**
```bash
export OTEL_SERVICE_NAME="ybis"
export OTEL_EXPORTER="jaeger"
export JAEGER_ENDPOINT="http://localhost:14268/api/traces"  # Jaeger HTTP endpoint
```

#### Step 3: Install OpenTelemetry Collector (Optional but Recommended)

The OpenTelemetry Collector is a separate service that:
- Receives traces from YBIS
- Processes and exports them to backends
- Provides buffering and retry logic

**Quick Start with Docker:**

```bash
# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC receiver
      - "4318:4318"   # OTLP HTTP receiver
      - "8888:8888"   # Prometheus metrics
    environment:
      - JAEGER_ENDPOINT=http://jaeger:14250  # If using Jaeger

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # Jaeger UI
      - "14268:14268"  # Jaeger HTTP endpoint
      - "14250:14250"  # Jaeger gRPC endpoint
EOF

# Create otel-collector-config.yaml
cat > otel-collector-config.yaml << EOF
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  logging:
    loglevel: info

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger, logging]
EOF

# Start services
docker-compose up -d
```

#### Step 4: Verify Setup

**Check Collector Status:**
```bash
# Check if collector is running
curl http://localhost:8888/metrics

# Check Jaeger UI (if using Jaeger)
open http://localhost:16686
```

**Run a Test Workflow:**
```bash
python scripts/ybis_run.py T-<task_id> --workflow self_develop
```

**View Traces:**
- **Jaeger UI:** http://localhost:16686
- **Console:** Check terminal output (if using console exporter)

### What Gets Logged to OpenTelemetry?

- **Spans** - Each workflow node execution
- **Trace context** - Correlation between related operations
- **Attributes** - Metadata (task_id, run_id, node_name, etc.)
- **Events** - Important events (start, end, errors)
- **Links** - Relationships between traces

### OpenTelemetry Backends

You can export to multiple backends:

1. **Jaeger** - Popular tracing backend
2. **Zipkin** - Another popular tracing backend
3. **OTLP** - Works with many backends (Datadog, New Relic, etc.)
4. **Console** - For development/debugging

---

## 3. Combined Setup (Both Langfuse + OpenTelemetry)

You can use both simultaneously:

```bash
# Langfuse
export LANGFUSE_PUBLIC_KEY="your-public-key"
export LANGFUSE_SECRET_KEY="your-secret-key"

# OpenTelemetry
export OTEL_SERVICE_NAME="ybis"
export OTEL_EXPORTER="otlp"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
```

**Benefits:**
- **Langfuse** - Best for LLM-specific observability (costs, tokens, prompts)
- **OpenTelemetry** - Best for distributed tracing and system-wide observability

---

## 4. Verification

### Check if Adapters are Active

**Python Script:**
```python
from src.ybis.services.observability import get_observability_service

obs = get_observability_service()
print(f"Observability adapters: {len(obs._adapters)}")

for adapter in obs._adapters:
    print(f"  - {adapter.__class__.__name__}: {adapter.is_available()}")
```

**Expected Output:**
```
Observability adapters: 2
  - LangfuseObservabilityAdapter: True
  - OpenTelemetryObservabilityAdapter: True
```

### Check Journal Logs

All events are also logged to journal files:
```bash
# View recent events
cat workspaces/*/runs/*/journal/events.jsonl | jq 'select(.event_type == "LLM_CALL")' | tail -5
```

### Check Langfuse Dashboard

1. Go to https://cloud.langfuse.com
2. Navigate to your project
3. Check "Traces" tab - should see workflow executions
4. Check "Generations" tab - should see LLM calls

### Check OpenTelemetry Traces

**If using Jaeger:**
1. Go to http://localhost:16686
2. Select service: "ybis"
3. Click "Find Traces"
4. Should see traces with spans

**If using Console:**
- Check terminal output for trace logs

---

## 5. Troubleshooting

### Langfuse Not Working

**Problem:** No traces in Langfuse dashboard

**Solutions:**
1. Check environment variables:
   ```bash
   echo $LANGFUSE_PUBLIC_KEY
   echo $LANGFUSE_SECRET_KEY
   ```
2. Check adapter availability:
   ```python
   from src.ybis.adapters.observability_langfuse import LangfuseObservabilityAdapter
   adapter = LangfuseObservabilityAdapter()
   print(adapter.is_available())  # Should be True
   ```
3. Check Langfuse logs:
   - Look for errors in journal logs
   - Check Langfuse dashboard for API errors

### OpenTelemetry Not Working

**Problem:** No traces in backend

**Solutions:**
1. Check environment variables:
   ```bash
   echo $OTEL_EXPORTER
   echo $OTEL_EXPORTER_OTLP_ENDPOINT
   ```
2. Check collector status:
   ```bash
   docker ps | grep otel-collector
   curl http://localhost:8888/metrics
   ```
3. Check adapter availability:
   ```python
   from src.ybis.adapters.observability_opentelemetry import OpenTelemetryObservabilityAdapter
   adapter = OpenTelemetryObservabilityAdapter()
   print(adapter.is_available())  # Should be True
   ```

### Both Adapters Disabled

**Problem:** `len(obs._adapters) == 0`

**Solutions:**
1. Check profile configuration:
   ```yaml
   # configs/profiles/default.yaml
   adapters:
     langfuse_observability:
       enabled: true  # Should be true
     opentelemetry_observability:
       enabled: true  # Should be true
   ```
2. Check adapter registration:
   ```python
   from src.ybis.adapters.registry import get_registry
   registry = get_registry()
   adapters = registry.list_adapters()
   print([a['name'] for a in adapters if 'observability' in a['name']])
   ```

---

## 6. Best Practices

### Development

- Use **Console Exporter** for OpenTelemetry (easy debugging)
- Use **Langfuse Cloud** (free tier is sufficient)
- Enable both adapters for comprehensive observability

### Production

- Use **OTLP Exporter** with OpenTelemetry Collector
- Use **Self-Hosted Langfuse** (if privacy is concern)
- Set up **alerts** based on metrics
- **Monitor costs** via Langfuse dashboard

### Performance

- OpenTelemetry uses **batch processing** (minimal overhead)
- Langfuse uses **async calls** (non-blocking)
- Both adapters have **graceful degradation** (fail silently if unavailable)

---

## 7. Summary

### Quick Start Checklist

- [ ] Set `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`
- [ ] Set `OTEL_SERVICE_NAME` and `OTEL_EXPORTER`
- [ ] (Optional) Set up OpenTelemetry Collector
- [ ] Verify adapters are active
- [ ] Run a test workflow
- [ ] Check Langfuse dashboard
- [ ] Check OpenTelemetry traces

### Configuration Files

- **Profile:** `configs/profiles/default.yaml` (adapters enabled)
- **Environment:** `.env` file or system environment variables
- **Collector:** `otel-collector-config.yaml` (if using collector)

---

## 8. Resources

- **Langfuse Docs:** https://langfuse.com/docs
- **OpenTelemetry Docs:** https://opentelemetry.io/docs/
- **Jaeger Docs:** https://www.jaegertracing.io/docs/
- **OTLP Protocol:** https://opentelemetry.io/docs/specs/otlp/

---

**Observability artık tam olarak aktif!** 🎉

