# Community Patterns: Tool Use & Environment
> Source: awesome-agentic-patterns (https://github.com/nicoloboschi/awesome-agentic-patterns)

## Overview
Patterns for connecting agents to the external world — APIs, databases, code executors, file systems, browsers, and other services. Tool use is the primary way agents take actions with real-world consequences, making this category both the most impactful and the most dangerous.

**24 patterns in this category.** For full detail on key patterns, see:
- Pattern 05: Tool Use / Function Calling (`patterns/05-tool-use.md`)
- Pattern 10: MCP (`patterns/10-mcp.md`)
- Pattern 27: Agentic Search (`patterns/27-agentic-search.md`)
- Pattern 29: Sandboxed Tool Authorization (`patterns/29-sandboxed-authorization.md`)

---

## Patterns

### Agentic Search Over Tools
**Status**: established
**Problem**: Complex information needs cannot be satisfied by a single search query.
**Solution**: Multi-step search loop: decompose query, select tool, evaluate results, refine, aggregate. See Pattern 27 for full detail.
**Tags**: search, multi-step, tool-use, retrieval
**Reference**: See Pattern 27 (`patterns/27-agentic-search.md`)

### Tool Selection Router
**Status**: established
**Problem**: Agent has many tools available; choosing the wrong tool wastes time and may cause errors.
**Solution**: Train or prompt a classifier to select the optimal tool for each sub-task before invocation. Selection considers: task type, data format, required permissions, latency, and cost.
**Tags**: routing, tool-selection, classification, efficiency
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Result Normalization
**Status**: established
**Problem**: Different tools return data in different formats (JSON, XML, Markdown, binary); agents must handle all formats.
**Solution**: Wrap each tool with a normalizer that converts output to a standard schema before returning to the agent. Agent always receives normalized output, regardless of source format.
**Tags**: normalization, tools, schema, consistency
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Code Execution Sandbox
**Status**: established
**Problem**: Agent-generated code may have bugs, infinite loops, or malicious behavior if executed directly.
**Solution**: Execute all agent-generated code in an isolated sandbox (container, subprocess with resource limits, WebAssembly). Enforce CPU time limit, memory limit, and no network access by default.
**Tags**: code-execution, sandbox, safety, isolation
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Browser Automation Agent
**Status**: established
**Problem**: Many tasks require interacting with web interfaces that have no API.
**Solution**: Give the agent a browser automation tool (Playwright, Selenium); agent navigates pages, clicks elements, fills forms, and extracts content. Combine with vision models for complex UI interpretation.
**Tags**: browser, automation, web, UI
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### File System Tool
**Status**: established
**Problem**: Agent needs to read, write, and organize files as part of its task execution.
**Solution**: Expose a scoped file system tool with read/write/list operations constrained to a designated working directory. Enforce path traversal prevention; log all file operations.
**Tags**: file-system, tool, scoping, safety
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### API Composition
**Status**: established
**Problem**: Agent needs to combine outputs from multiple APIs that were not designed to work together.
**Solution**: Implement an API composition layer: agent specifies a composition plan (call A, transform output, pass to B); the layer executes the composition, handles authentication per API, and returns a unified result.
**Tags**: API, composition, integration, multi-source
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Versioning
**Status**: established
**Problem**: Tool APIs change over time; agents trained on one version break when tools are upgraded.
**Solution**: Version all tool schemas; include the version in the tool definition; route agent calls to the appropriate version; support multiple versions concurrently during migration windows.
**Tags**: versioning, tools, compatibility, migration
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Parameterized Tool Templates
**Status**: established
**Problem**: Tool arguments contain complex nested structures that agents frequently mis-format.
**Solution**: Define tool argument templates with explicit examples; validate agent-provided arguments against the template schema before execution; return structured validation errors on mismatch.
**Tags**: tools, templates, validation, schema
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Database Query Tool
**Status**: established
**Problem**: Agent needs to query databases but writing raw SQL is error-prone and risks injection.
**Solution**: Expose a structured query tool: agent provides query parameters (table, filters, columns, limit); tool constructs a parameterized query; result is returned as structured rows. No raw SQL in agent context.
**Tags**: database, query, SQL, safety
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Webhook and Notification Tool
**Status**: established
**Problem**: Agent needs to trigger actions in external systems asynchronously.
**Solution**: Provide a webhook dispatch tool: agent provides (endpoint, payload, auth_ref); tool validates the endpoint against an allowlist, injects credentials, and dispatches; returns delivery confirmation.
**Tags**: webhook, async, notification, integration
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Health Check
**Status**: established
**Problem**: External tools become unavailable (API downtime, rate limits); agent continues trying and wastes budget.
**Solution**: Before task execution, probe all required tools with lightweight health checks; report unavailable tools to the user before starting; during execution, apply circuit breakers to detect tool degradation.
**Tags**: health-check, circuit-breaker, reliability, tools
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Structured Data Extraction Tool
**Status**: established
**Problem**: Unstructured documents (PDFs, HTML, emails) must be parsed into structured data before the agent can reason over them.
**Solution**: Expose a document extraction tool: agent provides (document, extraction_schema); tool uses specialized parsing (PDFParser, HTML cleaner, table extractor) to return structured data conforming to the schema.
**Tags**: extraction, documents, structured, parsing
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Call Batching
**Status**: established
**Problem**: Agents make many small tool calls that could be batched, causing unnecessary latency and API overhead.
**Solution**: Implement a batching layer: accumulate tool calls of the same type within a short time window; send as a single batch request; return individual results. Transparent to the agent.
**Tags**: batching, latency, efficiency, tools
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Capability Discovery
**Status**: emerging
**Problem**: Agents have access to many tools but do not know which tools are available at runtime (tools change, get added/removed).
**Solution**: Expose a meta-tool: `list_available_tools()` returns current tool catalog with descriptions, schemas, and usage examples. Agent queries this at task start to understand current capabilities.
**Tags**: discovery, meta-tool, dynamic, capability
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Read-Only Tool Mode
**Status**: established
**Problem**: During exploration and information gathering phases, the agent should not be able to take actions.
**Solution**: Implement a read-only mode flag: when active, all non-read tool calls are rejected with a structured error. Agent can gather information safely; write operations require explicit mode switch.
**Tags**: read-only, safety, exploration, permissions
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Long-Running Tool Handler
**Status**: established
**Problem**: Some tools (code compilation, data processing jobs) take minutes to complete; synchronous waiting blocks the agent.
**Solution**: For tools that may take > N seconds, return a job handle immediately; agent can continue with other work; poll for completion or register a callback. Implement async tool interface.
**Tags**: async, long-running, polling, tools
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Output Size Limiting
**Status**: established
**Problem**: Some tools return very large responses (full file contents, large API results) that fill the context window.
**Solution**: Apply output size limits per tool: truncate, paginate, or summarize responses that exceed a threshold. Include pagination tokens so the agent can request more if needed.
**Tags**: context, output-size, pagination, tools
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Idempotent Tool Operations
**Status**: established
**Problem**: Agent retries failed tool calls but the tool is not idempotent, causing duplicate side effects.
**Solution**: Implement idempotency keys: agent provides a unique operation ID with each tool call; tool checks if the ID has been processed; returns cached result for duplicate requests without re-executing.
**Tags**: idempotency, retry, side-effects, reliability
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Observability
**Status**: established
**Problem**: Tool calls are black boxes; failures are hard to debug without execution telemetry.
**Solution**: Wrap all tool calls with telemetry: log (tool_name, args_hash, latency_ms, result_status, result_size); emit traces linking tool calls to their parent agent spans.
**Tags**: observability, tools, telemetry, debugging
**Reference**: See Pattern 30 LLM Observability (`patterns/30-llm-observability.md`)

### Fallback Tool Chain
**Status**: established
**Problem**: Primary tool fails; agent gives up rather than trying an alternative.
**Solution**: Define a fallback chain per tool capability: primary → secondary → tertiary → manual fallback. On primary failure, automatically try the next option; log which fallback was used.
**Tags**: fallback, resilience, reliability, tools
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Tool Schema Versioning
**Status**: established
**Problem**: Tool schema changes break agents that were trained on the old schema.
**Solution**: Include schema version in every tool definition; validate agent-provided arguments against the version's schema; provide clear migration guides when schemas change; run parallel validation during migration.
**Tags**: schema, versioning, compatibility, tools
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Environment State Snapshot
**Status**: established
**Problem**: Agent actions on the environment (file writes, database changes) are hard to undo if the task fails.
**Solution**: Before starting a task, snapshot the relevant environment state; on task failure, restore from snapshot; on success, commit the snapshot as the new baseline.
**Tags**: snapshot, rollback, state, environment
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment

### Multi-Modal Tool Integration
**Status**: emerging
**Problem**: Tasks require combining text, image, audio, and structured data processing in a single pipeline.
**Solution**: Expose specialized tools per modality (image_analyze, audio_transcribe, chart_extract); agent orchestrates calls across modalities; output is always normalized to text/structured data before re-entering the agent context.
**Tags**: multi-modal, image, audio, tools
**Reference**: Source: awesome-agentic-patterns — Tool Use & Environment
