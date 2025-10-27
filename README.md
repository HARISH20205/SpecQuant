| Framework | Model           | Size (B Params) | Tokens/sec CPU | Tokens/sec GPU | Latency Metrics                     |
|-----------|-----------------|-----------------|----------------|----------------|-------------------------------------|
| SGLang    | LLaMA 1B        | 1               | ~15-20         | ~25-30         | TTFT ~50 ms, ITL ~10 ms             |
| SGLang    | LLaMA 3B        | 3               | ~7-10          | ~18-22         | TTFT ~80 ms, ITL ~12 ms             |
| SGLang    | LLaMA 7B        | 7               | ~2-3           | ~10-12         | TTFT >100 ms, ITL ~15-20 ms         |
| vLLM      | LLaMA 1B        | 1               | ~12-15         | ~20-25         | TTFT ~40-60 ms, ITL ~8-10 ms        |
| vLLM      | LLaMA 3B        | 3               | ~6-8           | ~16-20         | TTFT ~70-90 ms, ITL ~10-13 ms       |
| vLLM      | LLaMA 7B (Q8)   | 7               | ~1.5-2         | ~9-11          | TTFT ~120 ms, ITL ~18 ms            |
| Ollama    | LLaMA 1B        | 1               | ~14-18         | ~22-26         | TTFT ~55-70 ms, ITL ~9-11 ms        |
| Ollama    | LLaMA 3B        | 3               | ~5-7           | ~14-18         | TTFT ~85 ms, ITL ~14 ms             |
| Ollama    | LLaMA 7B (Quant)| 7               | ~1.5           | ~8-9           | TTFT >100 ms, ITL ~20 ms            |
| frugalsot | all             | 1               | ~20-25         | -`30-32        | TTFT ~40 ms, ITL  ~10ms             |

gpt-oss:20b