import lmstudio as lms
import time

prompt = "what are the benefits of speculative decoding in large language models? Explain with examples. "
main_model_key_1 = "qwen2.5-1.5b-instruct@fp16"
main_model_key_2 = "qwen2.5-1.5b-instruct@q8_0"
draft_model_key = "qwen2.5-1.5b-instruct@q4_k_m"

def run_basic(model_key, prompt):
    model = lms.llm(model_key)
    start = time.time()
    result = model.respond(prompt)
    end = time.time()
    duration = end - start
    stats = getattr(result, "stats", None)
    return {
        "mode": "normal",
        "accepted": getattr(stats, "accepted_draft_tokens_count", None),
        "predicted": getattr(stats, "predicted_tokens_count", None),
        "elapsed_time": duration
    }
def run_spec(model_key, prompt, draft_key):
    model = lms.llm(model_key)
    start = time.time()
    result = model.respond(prompt, config={"draftModel": draft_key})
    end = time.time()
    duration = end - start
    stats = getattr(result, "stats", None)
    return {
        "mode": "speculative",
        "accepted": getattr(stats, "accepted_draft_tokens_count", None),
        "predicted": getattr(stats, "predicted_tokens_count", None),
        "elapsed_time": duration
    }

results = []
results.append(run_basic(main_model_key_1, prompt))
results.append(run_spec(main_model_key_2, prompt, draft_model_key))

headers = ["Metric", "Normal", "Speculative"]
metrics = ["Accepted Tokens", "Predicted Tokens", "Elapsed Time (s)"]

normal_data = results[0]
spec_data = results[1]

col_widths = [20, 15, 15]
print(f"| {headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}} | {headers[2]:<{col_widths[2]}} |")
print(f"|{'-'*(col_widths[0]+2)}|{'-'*(col_widths[1]+2)}|{'-'*(col_widths[2]+2)}|")
print(f"| {'Accepted Tokens':<{col_widths[0]}} | {str(normal_data['accepted']):<{col_widths[1]}} | {str(spec_data['accepted']):<{col_widths[2]}} |")
print(f"| {'Predicted Tokens':<{col_widths[0]}} | {str(normal_data['predicted']):<{col_widths[1]}} | {str(spec_data['predicted']):<{col_widths[2]}} |")
print(f"| {'Elapsed Time (s)':<{col_widths[0]}} | {normal_data['elapsed_time']:<{col_widths[1]}.2f} | {spec_data['elapsed_time']:<{col_widths[2]}.2f} |")
