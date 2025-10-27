"""
/main.py
-------------------------
Adaptive speculative decoding system using LM Studio

Automatically selects optimal model precision (FP16, Q8, Q4)
based on prompt complexity and performs speculative decoding
for faster inference without compromising quality.

"""
from __future__ import annotations
import argparse
import logging
import lmstudio as lms


from complexity import ClassifyPrompt, ComplexityLevels
from utils import detect_device

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("main")



MODELS = {
    "Q16": "qwen2.5-1.5b-instruct@fp16",
    "Q8":  "qwen2.5-1.5b-instruct@q8_0",
    "Q4":  "qwen2.5-1.5b-instruct@q4_k_m",
}

def speculative_decode(prompt: str) -> str:
    """
    Perform speculative decoding 

    The complexity classifier decides which model precision to load
    and whether to use a draft model for speculative decoding.
    """
    try:
        complexity = ClassifyPrompt.get_complexity(prompt)
        logger.info(f"Prompt complexity classified as: {complexity}")

        if complexity == ComplexityLevels.low:
            model_key = MODELS["Q16"]
            draft_key = MODELS["Q4"]
        elif complexity == ComplexityLevels.mid:
            model_key = MODELS["Q16"]
            draft_key = MODELS["Q8"]
        else:
            model_key = MODELS["Q16"]
            draft_key = None

        logger.info(f"Loading target model: {model_key}")
        model = lms.llm(model_key)

        if draft_key:
            logger.info(f"Using draft model: {draft_key}")
            result = model.respond(prompt, config={"draftModel": draft_key})
        else:
            result = model.respond(prompt)

        return str(result)

    except Exception as e:
        logger.exception(f"Error during speculative decoding: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Adaptive speculative decoding using LM Studio.")
    parser.add_argument(
        "--prompt",
        type=str,
        required=False,
        default="Explain the theorem of CAP in distributed systems for GPUs, highlighting trade-offs and failure cases.",
        help="Prompt text for the model",
    )
    args = parser.parse_args()

    device = detect_device()
    logger.info(f"Running on device: {device}")

    output = speculative_decode(args.prompt)
    print("\n" + "=" * 80)
    print(output)
    print("=" * 80)
