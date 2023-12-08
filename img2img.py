import torch
from diffusers import AutoencoderTiny, AutoPipelineForImage2Image
from diffusers.utils import load_image
import math

#
# constants
#
CACHE_DIR = "/mnt/data/ML_models/huggingface"

#
# backend
#
torch.set_grad_enabled(False)
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

#
# setup
#
vae = AutoencoderTiny.from_pretrained(
    'madebyollin/taesd',
    torch_dtype=torch.float16,
    cache__dir=CACHE_DIR,
)
pipeline = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/sd-turbo",
    vae=vae,
    torch_dtype=torch.float16,
    variant="fp16",
    cache_dir=CACHE_DIR,
)
pipeline.set_progress_bar_config(disable=True)

#
# compilation
#
from sfast.compilers.stable_diffusion_pipeline_compiler import (
    compile, CompilationConfig
)
config = CompilationConfig.Default()
config.enable_xformers = True
config.enable_triton = True
config.enable_cuda_graph = True
config.enable_jit = False # You can set this to True, but you'll have to disable generator.manual_seed
config.enable_jit_freeze = True
config.trace_scheduler = True
config.enable_cnn_optimization = True
config.preserve_parameters = False
config.prefer_lowp_gemm = True
pipeline = compile(pipeline, config)

# # move to gpu
pipeline.to("cuda")
generator = torch.Generator(device="cuda")

def process_frame(frame, prompt="a man with glasses", strength=0.5, steps=2, seed=8934953498):
    generator.manual_seed(seed)

    return pipeline(
        prompt=prompt,
        image=frame,
        num_inference_steps=math.ceil(1/strength),
        strength=strength,
        guidance_scale=0.0,
        output_type="np",
        generator=generator
    ).images[0]
