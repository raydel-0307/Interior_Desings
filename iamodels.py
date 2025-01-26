from diffusers import DiffusionPipeline
import time
from metrics import get_time
import pickle
import os

def TrainModel(dir_path,model_name):

	init_time = time.perf_counter()

	pipe = DiffusionPipeline.from_pretrained(model_name)

	with open(f"{dir_path}/model.pkl", 'wb') as f:
		pickle.dump(pipe, f)

	print(f"Modelo exportado en '{dir_path}/'")

	get_time(init_time)


def MainModel(dir_path,prompt,image_path,output_path,settings):

	init_time = time.perf_counter()

	model_path = f"{dir_path}/model.pkl"

	if not os.path.exists(model_path):
		print("!OPS, para usar esta función debe descargar el modelo !")
		return

	with open(model_path, 'rb') as f:
		pipe = pickle.load(f)

	if "bedroom" in prompt and "bed " not in prompt:
		prompt += ", with a queen size bed against the wall"
	elif "children room" in prompt or "children's room" in prompt:
		if "bed " not in prompt:
			prompt += ", with a twin bed against the wall"

	pos_prompt = prompt + f", {settings['additional_quality_suffix']}"

	image = pipe(
		prompt=pos_prompt,
		image=image_path,
		negative_prompt=settings["negative_prompt"],
		num_inference_steps=settings["num_inference_steps"],
		guidance_scale=settings["guidance_scale"],
		prompt_strength=settings["prompt_strength"],
		seed=settings["seed"]
	).images[0]

	image.save(output_path)

	print(f"Imagen exportada '{output_path}'")

	get_time(init_time)