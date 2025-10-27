import torch

from complexity import ComplexityLevels


def detect_device():
    cuda_available = torch.cuda.is_available()
    if cuda_available:
        gpu_vram = torch.cuda.get_device_properties(0).total_memory // (1024 ** 2) # MB
        return "cuda", gpu_vram
    else:
        return "cpu", None
