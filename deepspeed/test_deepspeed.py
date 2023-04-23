import deepspeed
import torch
import os

from diffusers import DiffusionPipeline

from time import perf_counter
import numpy as np


def measure_latency(pipe, prompt):
    latencies = []
    # warm up
    # pipe.set_progress_bar_config(disable=True)
    for _ in range(2):
        _ =  pipe(prompt)
    # Timed run
    for _ in range(10):
        start_time = perf_counter()
        with torch.inference_mode():
            _ = pipe(prompt)
        latency = perf_counter() - start_time
        latencies.append(latency)
    # Compute run statistics
    time_avg_s = np.mean(latencies)
    time_std_s = np.std(latencies)
    time_p95_s = np.percentile(latencies,95)
    return f"P95 latency (seconds) - {time_p95_s:.2f}; Average latency (seconds) - {time_avg_s:.2f} +\- {time_std_s:.2f};", time_p95_s

def main():
    prompt = "a dog on a rocket"

    model = "runwayml/stable-diffusion-v1-5"

    pipe_ds = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.half).to("cuda")

    # NOTE: DeepSpeed inference supports local CUDA graphs for replaced SD modules.
    #       Local CUDA graphs for replaced SD modules will only be enabled when `mp_size==1`
    pipe_ds = deepspeed.init_inference(
        pipe_ds,
        mp_size=1,
        dtype=torch.half,
        replace_with_kernel_inject=True,
        enable_cuda_graph=True,
    )

    deepspeed_image = pipe_ds(prompt, guidance_scale=7.5).images[0]
    deepspeed_image.save(f"deepspeed.png")

    prompt = "a photo of an astronaut riding a horse on mars"

    vanilla_results = measure_latency(pipe_ds, prompt)

    print(f"Deepspeed pipeline: {vanilla_results[0]}")

if __name__ == "__main__":
    main()