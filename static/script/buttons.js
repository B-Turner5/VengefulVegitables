const button = document.getElementById('gen-image-button');
const canvasContainer = document.getElementById('drawingContainer');

button.addEventListener('click', (e) => {
    e.preventDefault();
    if (canvasContainer.id == "false"){
        console.log("No Drawing Made.")
    }
    else{
        const base64_image = canvas.toDataURL();
    }
})
