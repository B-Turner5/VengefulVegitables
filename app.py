from flask import Flask, render_template, request
import os
from PIL import Image
from torch import autocast
from diffusers import StableDiffusionPipeline
import io, base64
from io import BytesIO


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
    print(request.content_length)
    data = request.get_json() # So the issue with this, is that data is a dictionary, and contains ALL THE DATA needed. 
    #However, for some arbitrary reason, data["imagebase64"] does NOT CONTAIN all the data stored within the dictionary, returning a truncated version of it.

    userDrawingBase64 = data.get('imagebase64')

    # print(userDrawingBase64)

    def fix_base64_padding(base64_string):
        missing_padding = len(base64_string) % 4
        if missing_padding != 0:
            base64_string += '=' * (4 - missing_padding)
        return base64_string
    
    def convert_base64_to_image(base64_string, output_filename):
        # Fix base64 padding
        base64_string = fix_base64_padding(base64_string)

        # Convert the base64 string to bytes
        base64_bytes = base64.b64decode(base64_string)

        # Check if the data is a valid image
        image = Image.open(BytesIO(base64_bytes))
        print(image)
        image.verify()

        # Reset the BytesIO object for reading the image
        image.seek(0)

        # Save the image as a JPG file
        image.save(output_filename, "JPEG")

    userDrawingBase64 = userDrawingBase64[22:]
    print(userDrawingBase64)
    convert_base64_to_image(userDrawingBase64, "static/generated/drawing.jpg")


    clear_cache()

    # r = requests.post('https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image',
    # files = {
    #     'sketch_file': ('static/generated/drawing.jpg', sketch_file_object, 'image/jpeg'),
    #     },
    # data = { 'prompt': userPrompt},
    # headers = { 'x-api-key': '9da43ca4ce11dbf1b1cdab36ecf968c36896bbb5a46f5b1a4d62e8039737176c023f251323833cd6d1580eea6ba22b4c'}
    # )
    # if (r.ok):
    #     image = io.BytesIO(r.binary)
    #     image.save(str)
    # else:
    #     r.raise_for_status()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, ssl_context="adhoc")