## Stable Diffusion benchmarks

model: https://huggingface.co/runwayml/stable-diffusion-v1-5

batch size = 1, image size 512x512, fp16

| GPU                    | PT2.0,fp16,xformers   | PT,fp16 | DeepSpeed,fp16   | Oneflow,fp16     |
| :---                   | :---                  | :---    | :---             | :---             |
| A100-sxm4-40gb         | 1.96 s (4.54gb VRAM)  | 2.8 s   | 1.28 s (4.97 gb) | 0.98 s (5.62 gb) |
| V100, 16gb             | 2.96 s                |         |                  |                  |
| T4, 16gb               | 7.83 s                |         |                  |                  |


## How to run
VM setup https://gist.github.com/alexeigor/b4c21b5e1fe62d670c433d4ac8c9fd83
```
docker build . -t test_engine
docker run -it -v ${PWD}:${PWD} -w ${PWD} --gpus all test_engine
```

## Optimizations
1. xFormers
2. Channels last https://huggingface.co/docs/diffusers/main/en/optimization/fp16#using-channels-last-memory-format
3. 


## References:
1. https://github.com/microsoft/DeepSpeed-MII/tree/main/examples/benchmark/txt2img
2. https://github.com/Oneflow-Inc/oneflow
3. https://github.com/facebookincubator/AITemplate
4. https://arxiv.org/abs/2304.11267
5. https://github.com/dbolya/tomesd
6. https://huggingface.co/docs/diffusers/main/en/optimization/fp16
7. https://github.com/hidet-org/hidet
