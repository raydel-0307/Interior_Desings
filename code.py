#pip install diffusers accelerate safetensors transformers

import PIL
import requests
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler

model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
pipe.to("cuda")
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

url = "https://raw.githubusercontent.com/timothybrooks/instruct-pix2pix/main/imgs/example.jpg"
def download_image(url):
	image = PIL.Image.open(requests.get(url, stream=True).raw)
	image = PIL.ImageOps.exif_transpose(image)
	image = image.convert("RGB")
	return image

def local_image(file_path):
	image = PIL.Image.open(file_path)
	image = PIL.ImageOps.exif_transpose(image)
	image = image.convert("RGB")
	return image

image = local_image("children_room_3.jpg")

prompt = "Crea un mejor diseño para este cuarto. interior design, 4K, high resolution, elegant, tastefully decorated, functional"
images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images
images[0]