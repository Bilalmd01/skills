# Model Catalog

Complete reference of available LLM models with specifications, capabilities, costs, and limitations.

## Model Reference Table

| Provider | Model ID | Alias | Input Cost ($/M) | Output Cost ($/M) | Context Window | Capabilities | Best Use Cases | Known Limitations |
|----------|----------|-------|------------------|-------------------|----------------|--------------|----------------|------------------|
| **Local Models** | | | **Free** | **Free** | | | | |
| Ollama | ollama/qwen2.5:1.5b | Qwen 2.5 1.5B | 0.00 | 0.00 | 32K | Text, basic reasoning | Testing, prototyping, simple tasks | Very limited reasoning, small context |
| Ollama | ollama/qwen2.5:32b | Qwen 2.5 32B | 0.00 | 0.00 | 32K | Text, code, reasoning | General purpose, local development | Requires local GPU, slower than cloud |
| Ollama | ollama/llama3.3 | Llama 3.3 70B | 0.00 | 0.00 | 128K | Text, code, reasoning | High-quality local work | Resource intensive, slower response |
| **z.ai Proxy** | | | **Low Cost** | **Low Cost** | | | | |
| z.ai | anthropic-proxy-4/glm-4.7 | GLM-4.7 (Proxy 4) | 0.50 | 1.50 | 131K | Text, code, reasoning, vision | General purpose, cost-effective | Proxy layer may add latency |
| z.ai | anthropic-proxy-6/glm-4.7 | GLM-4.7 (Proxy 6) | 0.50 | 1.50 | 131K | Text, code, reasoning, vision | General purpose, reliable | Same as above |
| z.ai | anthropic-proxy-6/glm-4.5-air | GLM-4.5-Air | 0.10 | 0.10 | 131K | Text, summarization, basic tasks | Monitoring, checks, summaries | Limited complex reasoning |
| **NVIDIA NIM** | | | **Medium Cost** | **Medium Cost** | | | | |
| NVIDIA | nvidia-nim/meta/llama-3.3-70b-instruct | Llama 3.3 70B NIM | 0.40 | 0.40 | 131K | Text, code, reasoning | General purpose, balanced cost/quality | Less creative than frontier models |
| NVIDIA | nvidia-nim/deepseek-ai/deepseek-v3.2 | DeepSeek V3.2 | 0.40 | 1.30 | 131K | Text, code, reasoning (excellent) | Code generation, complex logic | Higher output cost |
| NVIDIA | nvidia-nim/nvidia/llama-3.1-nemotron-ultra-253b-v1 | Nemotron Ultra 253B | 2.50 | 5.00 | 131K | Text, reasoning (excellent) | Complex reasoning, analysis | Very expensive |
| **Other Proxies** | | | **Variable Cost** | **Variable Cost** | | | | |
| DeepSeek | anthropic-proxy-5/deepseek-chat | DeepSeek Chat | 3.00 | 15.00 | 64K | Text, code, reasoning | ⚠️ AVOID — use `nvidia-nim/deepseek-ai/deepseek-v3.2` instead at $0.40/$1.30 | Massively overpriced via proxy |
| **Anthropic** | | | **Premium** | **Premium** | | | | |
| Anthropic | anthropic/claude-sonnet-4-5 | Claude Sonnet 4.5 | 3.00 | 15.00 | 200K | Text, code, reasoning, vision | High-quality general purpose | Expensive |
| Anthropic | anthropic/claude-opus-4-6 | Claude Opus 4.6 | 5.00 | 25.00 | 1M | Text, code, reasoning, vision (best) | Critical tasks, security, production | Most expensive |

## Detailed Specifications

### Local Models (Free)

**Ollama/qwen2.5:1.5b**
- **Capabilities**: Basic text processing, simple Q&A, format conversion
- **Best for**: Prototyping, testing pipelines, simple text transformations
- **Limitations**: Cannot handle complex logic, limited context, poor at code
- **When to use**: When cost is zero priority and task is trivial

**Ollama/qwen2.5:32b**
- **Capabilities**: Good general reasoning, decent code generation, summarization
- **Best for**: Local development, privacy-sensitive tasks, offline work
- **Limitations**: Slower than cloud, requires GPU memory, limited compared to frontier models
- **When to use**: When privacy/local processing is required

**Ollama/llama3.3**
- **Capabilities**: High-quality local model, good at code and reasoning
- **Best for**: Complex local work when cloud costs are prohibitive
- **Limitations**: Resource intensive (70B parameters), slower inference
- **When to use**: High-quality local work without cloud costs

### z.ai Proxy Models (Low Cost)

**GLM-4.7 Series**
- **Capabilities**: Strong general purpose, good code generation, vision support
- **Best for**: Everyday tasks, general coding, research, analysis
- **Limitations**: Proxy layer adds some latency, may default to Chinese in edge cases
- **Cost efficiency**: Excellent value for general purpose work

**GLM-4.5-Air**
- **Capabilities**: Optimized for summarization, monitoring, basic tasks
- **Best for**: Heartbeat checks, status monitoring, simple fetches
- **Limitations**: Not suitable for complex reasoning or creative work
- **Cost efficiency**: Cheapest cloud option ($0.10/$0.10 per M)

### NVIDIA NIM Models (Medium Cost)

**Llama 3.3 70B NIM**
- **Capabilities**: Well-rounded, good balance of capabilities
- **Best for**: General coding, documentation, medium-complexity tasks
- **Limitations**: Less creative/insightful than frontier models
- **Cost efficiency**: Good balance at $0.40/$0.40

**DeepSeek V3.2**
- **Capabilities**: Excellent at code, strong reasoning, mathematical ability
- **Best for**: Complex coding tasks, debugging, algorithm design
- **Limitations**: Higher output cost ($1.30/M), less creative writing
- **Cost efficiency**: Great for code-heavy work

**Nemotron Ultra 253B**
- **Capabilities**: Exceptional reasoning, analysis, complex problem-solving
- **Best for**: Critical analysis, strategic planning, complex logic
- **Limitations**: Very expensive ($2.50/$5.00), overkill for simple tasks
- **Cost efficiency**: Only for highest-stakes work

### Premium Models

**Claude Sonnet 4.5**
- **Capabilities**: High-quality general purpose, creative writing, analysis
- **Best for**: Important but non-critical tasks, creative work, analysis
- **Limitations**: Expensive ($3/$15), not the absolute best
- **When to use**: When quality matters but cost sensitivity exists

**Claude Opus 4.6**
- **Capabilities**: Frontier model, best overall quality, 1M context
- **Best for**: Security audits, production code, financial analysis, critical work
- **Limitations**: Most expensive option ($5/$25)
- **When to use**: When failure is not an option

## Cost Comparison Examples

**Scenario**: Processing 1000 tokens input + 500 tokens output:
- **GLM-4.5-Air**: $0.0001 + $0.0001 = $0.0002
- **Llama 3.3 70B**: $0.0004 + $0.0004 = $0.0008
- **DeepSeek V3.2**: $0.0004 + $0.0013 = $0.0017
- **Claude Opus**: $0.005 + $0.025 = $0.030

**Rule of thumb**: Opus is ~150x more expensive than GLM-4.5-Air for the same task.

## Selection Guidelines

1. **Start cheap**: Always try the cheapest suitable model first
2. **Escalate on failure**: Move up one tier if results are unsatisfactory
3. **Consider task volume**: High-volume tasks benefit more from cheaper models
4. **Factor in retry costs**: Expensive models may reduce retry needs
5. **Know your priorities**: Cost vs quality vs speed trade-offs

## Updates

This catalog should be updated periodically as:
- New models become available
- Pricing changes occur
- Capabilities evolve
- Performance benchmarks update

Check with the maintainer for the latest version.