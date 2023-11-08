from flask import Flask, render_template, jsonify, request, send_file
import os
import io
import warnings
from PIL import Image
import random
from torch import autocast
from diffusers import StableDiffusionPipeline
from super_image import DrlnModel, ImageLoader
import requests


###### ensure "pip install --upgrade diffusers[torch]" is called after installing requirements.txt

app = Flask(__name__)

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
    image.save(output_path, 'png')
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

def upscale_image(image, output_path):
    model = DrlnModel.from_pretrained('eugenesiow/drln-bam', scale=2)
    inputs = ImageLoader.load_image(image)
    preds = model(inputs)
    ImageLoader.save_image(preds, output_path)

@app.route('/process_drawing', methods=['POST'])
def process_image_input():
    data = request.get_json()
    userPrompt = data.get('prompt')
    userDrawingBase64 = data.get('imagebase64')

    uesrDrawing = image.save('static/generated/drawing', 'png')

    clear_cache()

    r = requests.post('https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image',
    files = {
        'sketch_file': ('owl-sketch.jpg', sketch_file_object, 'image/jpeg'),
        },
    data = { 'prompt': 'an owl on a branch, cinematic' },
    headers = { 'x-api-key': 'YOUR_API_KEY'}
    )
    if (r.ok):
        image = io.BytesIO(r.binary)
        image.save(str)
    else:
        r.raise_for_status()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, ssl_context="adhoc")