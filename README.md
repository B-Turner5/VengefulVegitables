# VengefulVegetables
As part of the 2023 BU Code Jam, our team, the "Vengeful Vegetables" have designed an application that allows you to search ClickASnap or generate AI images which you can then view in AR and purchase as a TeeMill shirt.

### Guide
Draw and image or write a propmt, either find an image from ClickASnap or generate a custom AI image.

### Python Installation
`python3 -m venv .env`
`.env/Scripts/activate`
`python -m pip install -r ./requirements.txt`
`python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu118`
`python -m pip install --upgrade diffusers[torch]`

In case you get cuda errors and torch breaks.
`python -m pip install torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/nightly/cu118`

### Limitations and Further Development

### References
https://www.w3schools.com/
https://teemill.com/api-docs/create-custom-product/guides/javascript/



