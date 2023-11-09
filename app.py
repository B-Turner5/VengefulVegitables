from flask import Flask, render_template, request
import os
from PIL import Image
from torch import autocast
from diffusers import StableDiffusionPipeline
import io, base64
from io import BytesIO
import requests


###### ensure "pip install --upgrade diffusers[torch]" is called after installing requirements.txt

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16000000

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

@app.route('/process_drawing', methods=['POST'])
def process_image_input():

    clear_cache()

    data = request.get_json()

    userDrawingBase64 = data.get('imagebase64')

    userPrompt = data.get('prompt')

    userDrawingBase64 = userDrawingBase64[22:]

    userDrawing = Image.open(io.BytesIO(base64.decodebytes(bytes(userDrawingBase64, "utf-8"))))
    userDrawingjpg = Image.new("RGB", userDrawing.size, (255,255,255))
    userDrawingjpg.paste(userDrawing,userDrawing)
    userDrawingjpg.save('static/generated/drawing.jpg')

    with open('static/generated/drawing.jpg', 'rb') as file:
        sketch_file_object = file.read()

    r = requests.post('https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image',
    files = {
        'sketch_file': ('static\generated\drawing.jpg', sketch_file_object, 'image/jpeg'),
        },
    data = { 'prompt': userPrompt},
    headers = { 'x-api-key': '9da43ca4ce11dbf1b1cdab36ecf968c36896bbb5a46f5b1a4d62e8039737176c023f251323833cd6d1580eea6ba22b4c'}
    )
    if (r.ok):
        with open('static/generated/sketchtoai.jpg', 'wb') as f:
            f.write(r.content)
            image = Image.open('static/generated/sketchtoai.jpg')
            image.show()  
    else:
        r.raise_for_status()

    return "static/generated/sketchtoai.jpg"
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)