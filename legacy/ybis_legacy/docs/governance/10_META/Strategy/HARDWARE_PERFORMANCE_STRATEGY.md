# ⚡ YBIS HARDWARE & PERFORMANCE STRATEGY

**Goal:** Maximize Local GPU (RTX 5090) utilization and reach peak TPS (Tokens Per Second) while maintaining Tier 4+ intelligence.

---

## 1. INTELLIGENT MODEL ROUTING (The Switchboard)
Don't use a sledgehammer to crack a nut.
- **Micro-Tasks (1.5B - 3B models):** Unit test generation, docstring fixes, syntax validation.
- **Logic-Tasks (7B - 14B models):** Implementation of small functions, log analysis.
- **Architect-Tasks (32B - 70B models):** System design, complex refactoring, multi-file reasoning.
- **Optimization:** Implement an async "Model Warm-up" system that pre-loads the next required model based on the task queue.

## 2. INFERENCE ENGINE OPTIMIZATIONS
Move beyond basic wrappers to high-performance engines.
- **vLLM Integration:** Use PagedAttention to handle massive context without VRAM fragmentation.
- **TensorRT-LLM:** Leverage NVIDIA-specific optimizations for the 5090.
- **Quantization Strategy:**
    - Use `EXL2` or `AWQ` for coding models (better logic retention).
    - Use `GGUF` only for low-priority background tasks.
- **Context Caching:** Enable "Flash Attention 2" and "Prompt Caching" to skip processing unchanged parts of the codebase.

## 3. GPU & VRAM MANAGEMENT (The Offloader)
- **VRAM Guard:** A monitor that dynamically adjusts context window size based on current VRAM headroom.
- **Multi-GPU Ready:** Design the Orchestrator to split layers across multiple GPUs if the factory expands.
- **Idle Offloading:** Automatically move models to System RAM (System RAM Offload) during long "Sentinel" verification runs to free up GPU for parallel visualization.

## 4. SOFTWARE-LEVEL ACCELERATION
- **Speculative Decoding:** Use a tiny "Draft Model" (e.g., Qwen-0.5B) to predict tokens, verified by the "Target Model" (32B). High TPS gain for code.
- **Batch Processing:** Group multiple verification or planning requests into a single GPU pass.
- **Async Streaming:** Sentinel should start analyzing the code *while* Aider is still streaming the output (Pipeline Parallelism).

## 5. REPOSITORY INDEXING (RAG Speed)
- **Vector Sharding:** Split the Vector DB into "Active Code", "Legacy Base", and "API Docs".
- **HNSW Indexing:** Use high-speed neighbor search for sub-millisecond context retrieval.

---
*Status: Strategy Defined - Ready for Implementation Phase*
