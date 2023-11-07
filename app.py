from flask import Flask, render_template, jsonify, request, send_file
import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import random
#from rembg import remove # decided that it doesn't want to install. do pip install rembg later
from torch import autocast
from diffusers import StableDiffusionPipeline


###### ensure "pip install --upgrade diffusers[torch]" is called after installing requirements.txt

app = Flask(__name__)

os.environ["STABILITY_KEY"] = "sk-iWZM3tgSXtWq08nOkeBIEPx1mbh3W5AIaHqqHwIpZMnH2eXz"
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0"
)

@app.route("/")
def hello_world():

    return render_template('index.html')

@app.route('/process_prompt', methods=['POST'])
def process_input():

    clear_cache()

    data = request.get_json()
    userPrompt = data.get('prompt')


    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    pipe.to("cuda")
    image = pipe(userPrompt).images[0]
    
    output_path = f"static/generated/{userPrompt}.png"
    image.save(output_path)
    return output_path
    
def clear_cache():
    try:
        files = os.listdir("./static/generated")
        for file in files:
            file_path = os.path.join("./static/generated", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Cache cleared.")
    except OSError:
        print("Error occured when purging cache.")

def remove_background(i_path):
    img_input = Image.open(i_path)
    img_output = remove(img_input)
    img_output.save(i_path)


def artifact_shit(userPrompt):
    image = stability_api.generate(
    prompt=userPrompt,
    seed=random.randint(1,100000), # If a seed is provided, the resulting generated image will be deterministic.
                     # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                     # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
    steps=30, # Amount of inference steps performed on image generation. Defaults to 30. 
    cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
                   # Defaults to 7.0 if not specified.
    width=1024, # Generation width, defaults to 512 if not included.
    height=1024, # Generation height, defaults to 512 if not included.
    samples=1, # Number of images to generate, defaults to 1 if not included.
    sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
)
    for resp in image:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save("./static/generated/" + str(artifact.seed)+ ".png") # Save our generated images with their seed number as the filename.
    filename = "static/generated/" + str(artifact.seed) + ".png"
    remove_background(filename)
    return filename


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, ssl_context="adhoc")



