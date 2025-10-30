# SpecQuant – Speculative Decoding with Multi-Parent Quantization for Adaptive LLM Inference

> **⚠️ NOTICE: This repository has moved!**  
> This project is now actively maintained at: **[https://github.com/HyperKuvid-Labs/SpecQuant](https://github.com/HyperKuvid-Labs/SpecQuant)**  
> Please visit the new repository for the latest updates, issues, and contributions.

This repository contains the source code for **SpecQuant (A Speculative Decoding with Multi-Parent Quantization for Adaptive LLM Inference)**, a system designed to make Large Language Models (LLMs) run faster on personal computers without sacrificing the quality of the answers. It intelligently adjusts to the complexity of your questions and the hardware you have.

## Overview

Running large language models locally on consumer hardware is challenging due to limited memory and processing power. SpecQuant addresses this by using a technique called **adaptive speculative decoding**.

The core idea is to use different versions of the same model, quantized to different precision levels (like FP16, Q8, Q4). When you enter a prompt, the system first analyzes its complexity.

- For **simple prompts**, it uses a highly compressed (quantized) and faster "draft" model to generate a draft response, which is then verified by a more precise "target" model.
- For **more complex prompts**, it uses a less compressed draft model or no draft model at all to ensure high-quality output.

This approach, called **SpecQuant – Speculative Decoding with Multi-Parent Quantization for Adaptive LLM Inference**, speeds up inference significantly because the draft and target models are closely related (being versions of the same base model), leading to high acceptance rates of the drafted tokens.

## How It Works

The system follows a three-step process for each prompt:

### 1. Prompt Complexity Classification

When a prompt is provided, it is first analyzed to determine its complexity. This is done by the `ClassifyPrompt` class in `complexity.py`, which evaluates three aspects:

- **Length Complexity**: The number of words in the prompt.
- **Syntactic Complexity**: The grammatical structure, like the use of conjunctions or subordinate clauses.
- **Semantic Complexity**: The number of named entities (like people, places, organizations) in the prompt.

Based on a weighted score of these three metrics, the prompt is classified as **low**, **medium**, or **high** complexity.

### 2. Adaptive Model Selection

Based on the determined complexity, the system selects the appropriate models for speculative decoding:

- **Low Complexity**: Uses a high-precision model (FP16) as the target and a highly quantized model (Q4) as the draft.
- **Medium Complexity**: Uses the same high-precision target model (FP16) but a medium-quantized model (Q8) as the draft.
- **High Complexity**: Uses only the high-precision model (FP16) without a draft model to ensure the highest accuracy for complex questions.

The system is also designed to be hardware-aware. The `detect_device()` function in `utils.py` checks if a CUDA-enabled GPU is available to run the models on the most performant hardware.

### 3. Speculative Decoding

With the target and draft models selected, the system performs speculative decoding using the `lmstudio` library. The draft model generates a sequence of tokens (a draft response) which are then efficiently verified by the target model in parallel. This allows the system to process multiple tokens at once, leading to a significant speedup in generating the final response.

## Features

- **Adaptive Inference**: Automatically adjusts model precision based on prompt complexity.
- **Speculative Decoding**: Speeds up LLM inference without quality loss.
- **Hardware-Aware**: Detects and utilizes available GPU for better performance.
- **No Retraining Required**: Uses post-training quantization, so no need for expensive model retraining.
- **Easy to Use**: A simple command-line interface to run the model with a given prompt.

## System Requirements

- Python 3.12+
- A CUDA-enabled GPU is recommended for best performance, but it can also run on a CPU.
- Dependencies listed in `pyproject.toml`.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/HARISH20205/SpecQuant.git
    cd SpecQuant
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.

    ```bash
    # Using uv (recommended)
    uv pip install -e .

    # Or using pip
    pip install -e .
    ```

    _(Note: This will install the project in editable mode based on `pyproject.toml`)_

3.  **Setup LM Studio:**
    Follow the instructions at [LM Studio](https://lmstudio.ai)

    Add the models you want to use (e.g., Qwen2.5-FP16, Qwen2.5-Q8, Qwen2.5-Q4) in LM Studio.

    Use the model names as specified in LM Studio when prompted in the code.

4.  **Download NLTK data:**
    The complexity classification requires some data from the NLTK library. Run the following in a Python interpreter:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    ```

## Usage

You can run the system using the `main.py` script. You can provide a prompt as a command-line argument.

```bash
python main.py --prompt "Your question here"
```

If no prompt is provided, it will run with a default example prompt.

**Example:**

```bash
python main.py --prompt "What is the capital of France?"
```

The script will output the complexity classification, the models being used, and the final response from the LLM.

## Project Structure

```
.
├── main.py             # Main script to run the adaptive speculative decoding
├── complexity.py       # Logic for classifying prompt complexity
├── utils.py            # Utility functions like device detection
├── test.py             # A script for benchmarking performance
├── pyproject.toml      # Project metadata and dependencies
├── README.md           # This file
```

## Results

| Run | **Normal** |              | **SpecQuant** |              |      **Improvement**      |
| :-: | :--------: | :----------: | :-----------: | :----------: | :-----------------------: |
|     |  Time (s)  | Accuracy (%) |   Time (s)    | Accuracy (%) | Speed-up (%) / Δ Accuracy |
|  1  |    4.07    |     72.5     |     3.01      |     72.3     |  **35.2% faster / -0.2**  |
|  2  |    6.42    |     75.0     |     4.50      |     74.9     |  **42.7% faster / -0.1**  |
|  3  |    8.83    |     70.0     |     6.43      |     69.9     |  **37.3% faster / -0.1**  |
