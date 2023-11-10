from flask import Flask, render_template, request
import os
from PIL import Image
from torch import autocast, Generator
from diffusers import StableDiffusionPipeline
import io, base64
import requests
import random
import pygltflib
import pygltflib.utils
import re
import cv2
import numpy
from bing_image_downloader import downloader
import shutil
###### ensure "pip install --upgrade diffusers[torch]" is called after installing requirements.txt

global recent_image
recent_image = "generated/RamenPanda.png"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16000000

@app.route("/")
def hello_world():

    return render_template('index.html')

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    clear_cache()
    data = request.get_json()
    userPrompt = data.get('prompt')
    random_seed = random.randint(1, 4294967296)
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    generator = Generator("cuda").manual_seed(random_seed)
    pipe.to("cuda")
    image = pipe(userPrompt, generator=generator).images[0]
    
    output_path = f"static/generated/{userPrompt}_{random_seed}.png"
    global recent_image
    print(recent_image)
    recent_image = output_path
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

    # USE A REGEX EXPRESSION TO AVOID BAD FILENAMES
    userPrompt = re.sub(r"^![\w\-. ]+$", "", userPrompt)

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

@app.route('/update_shirt_texture', methods=['POST'])
def update_model():
    # gltf_model = pygltflib.GLTF2().load("static/assets/tshirt/tshirt.gltf")
    # gltf_image = pygltflib.Image()
    # gltf_image.uri = recent_image

    # gltf_model.images.append(gltf_image)
    # gltf_model.convert_images(pygltflib.ImageFormat.DATAURI)
    # gltf_model.images[0].uri
    # gltf_model.images[0].name

    # gltf_model.save("static/assets/tshirt/tshirt_UPDATED.gltf")

    shirt_texture = cv2.imread("static/assets/tshirt/shirt.png")
    replacing_img = cv2.imread(recent_image)

    offset_x = 400
    shirt_texture[256:768, (512-offset_x):(1024-offset_x)] = replacing_img[0:512,0:512] #0.256:0.676
    cv2.imwrite("static/assets/tshirt/shirt.png", shirt_texture)
    return "done"

@app.route('/generating')
def display_generating_page():
    return render_template('generating.html')

def center_crop(img, dim):
	"""Returns center cropped image
	Args:
	img: image to be center cropped
	dim: dimensions (width, height) to be cropped
	"""
	width, height = img.shape[1], img.shape[0]

	# process crop width and height for max available dimension
	crop_width = dim[0] if dim[0]<img.shape[1] else img.shape[1]
	crop_height = dim[1] if dim[1]<img.shape[0] else img.shape[0] 
	mid_x, mid_y = int(width/2), int(height/2)
	cw2, ch2 = int(crop_width/2), int(crop_height/2) 
	crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	return crop_img

def scale_image(img, factor=1):
	"""Returns resize image by scale factor.
	This helps to retain resolution ratio while resizing.
	Args:
	img: image to be scaled
	factor: scale factor to resize
	"""
	return cv2.resize(img,(int(img.shape[1]*factor), int(img.shape[0]*factor)))

#https://medium.com/curious-manava/center-crop-and-scaling-in-opencv-using-python-279c1bb77c74

@app.route("/image_search", methods=['POST'])
def search():

    for subdir, dirs, files in os.walk("static/searched"):
        for d in dirs:
            p = os.path.join("static/searched", d)
            shutil.rmtree(p)
            

    data = request.get_json()
    userPrompt = data.get('prompt')
    downloader.download(userPrompt, limit=1, output_dir='static/searched', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
    image_path = f"static/searched/{userPrompt}"

    for i in os.listdir(image_path):
        image_path = os.path.join(image_path, i)

    img = cv2.imread(image_path)

    if img is not None:

        #scale = img.shape[0] if img.shape[0] < img.shape[1] else img.shape[1]

        #out = center_crop(img, (512, 512))
        #out = scale_image(out, scale/512)

        out = img

        cv2.imwrite(image_path, out)

        global recent_image
        recent_image = image_path
    
        return image_path
    
    return 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, ssl_context="adhoc")