import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import openai

cache_path = "./cached_models/"
model_id = "runwayml/stable-diffusion-v1-5"


def generate_image(**inputs):
    topic = inputs["topic"]

    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative director for a world famous art studio. You are looking to amaze your visitors with realistic and mind blowing pieces."},
            {"role": "user", "content": "Write a image description that is only physical nouns, adjectives, and prepositions for the concept of Ancient Venice-like city found on Earth-like planet"},
            {"role": "assistant", "content": "establishing shot of canal surrounded by verdant blue modern curved rustic Greek tiled buildings, dawn, water, canoes, refraction"},
            {"role": "user", "content": "Write a image description that is only physical nouns, adjectives, and prepositions for the concept of multidimensional space whales invading our universe"},
            {"role": "assistant", "content": "Majestic, gigantic, beautiful space whales shimmering in wide array of colors in starry space background"},
            {"role": "user", "content": f"Write a image description that is only physical nouns, adjectives, and prepositions for the concept of '{topic}'"},
            #         {"role": "assistant", "content": "Tiny fluffy kittens running up and down, exchanging fast cards on top of an inverted black and yellow pyramid in Upside-down world."},
            #         {"role": "user", "content": "There shouldn't be verbs or movement or actions like 'running' or 'exchanging' or vague concepts like 'Upside down world'. Regenerate please"}
        ],
        temperature=0.9
    )

    raw_prompt = response.choices[0].message.content

    print("Got raw prompt: " + raw_prompt)

    expanded_prompt = raw_prompt + \
        ", stunning, highly detailed, 8k, ornate, intricate, cinematic, dehazed, atmospheric, (oil painting:0.75), (splash art:0.75),(teal:0.2),(orange:0.2), (by Jeremy Mann:0.5), (by John Constable:0.1),(by El Greco:0.5),(acrylic paint:0.75)"
    negative_prompt = "bad:-1, ugly:-1.6, overexposed:-1, (low contrast):-1, (cut off):-1, tiling:-1, (watermark blurry):-1.5, deformed:-1, (weird colors):-1, (mutated color):-1, (muted color):-1, fused:-1, (less detail):-1, lowres:-1, (out of frame):-1, (worst quality):-1, (low quality):-1, (normal quality):-1, (displaced object):-1, (close up):-1, cartoon:-1, 3d:-1, (disfigured):-1, (deformed):-1, (poorly drawn):-1, (extra limbs):-1, blurry:-1, boring:-1, sketch:-1, lackluster:-1, signature:-1, letters:-1, (low res):-1, horrific:-1 , mutated:-1 , artifacts:-1, (bad art):-1 , gross:-1 , b&w:-1 , cropped:-1"
    prompt = expanded_prompt + " " + negative_prompt

    torch.backends.cuda.matmul.allow_tf32 = True

    scheduler = DPMSolverMultistepScheduler.from_pretrained(
        model_id,
        use_auth_token=os.environ["HUGGINGFACE_API_KEY"],
        subfolder="scheduler",
        # cache_dir=cache_path,
        solver_order=2,
        prediction_type="epsilon",
        thresholding=False,
        algorithm_type="dpmsolver++",
        solver_type="midpoint",
        denoise_final=True,
    )

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        revision="fp16",
        torch_dtype=torch.float16,
        # cache_dir=cache_path,
        scheduler=scheduler,
        # Add your own auth token from Huggingface
        use_auth_token=os.environ["HUGGINGFACE_API_KEY"],
    ).to("cuda")

    with torch.inference_mode():
        with torch.autocast("cuda"):
            image = pipe(prompt=prompt, num_inference_steps=100, height=400, width=512,
                         guidance_scale=7.5).images[0]

    print(f"Saved Image: {image}")
    image.save("output.png")


if __name__ == "__main__":
    prompt = "a renaissance style photo of elon musk"
    generate_image(prompt=prompt)
