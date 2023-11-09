document.getElementById('open-camera-button').addEventListener('click', function () {
    document.getElementById("camera-overlay").style.display = "flex";
})

document.getElementById('close-camera-button').addEventListener('click', function () {
    document.getElementById("camera-overlay").style.display = "none";
})

document.getElementById('clear-image-button').addEventListener('click', function () {
    let canvas = document.getElementById("drawing-canvas");
    let ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawingMade = false;

    document.getElementById('gen-button-container').style.display = "flex";
    document.getElementById('extra-button-container').style.display = "none";
    document.getElementById('output-image').style.display = "none";
    document.getElementById('loader').style.display = "none";
})



// THIS FUNCTION DOES NOT SEEM TO RUN. I HAVE NO IDEA WHY
document.getElementById('purchase-item-button').addEventListener('click', function () {
    const apiKey = 'OdCOVs1LdtwCLoeC5VE22JHETdNSyq75aY2ahGdt'; 
    const img = document.getElementById("output-image");
    context.drawImage(img, canvas.width, canvas.height);
    const base64_image = canvas.toDataURL();
    console.log(base64_image)

    const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          image_url: base64_image,
          item_code: "RNA1",
          name: "Limited Edition Vengeful Vegetables Tee ",
          colours: "White",
          description: "For those people who absolutely detest meat and want to watch the world burn.",
          price: 20.00,
        }),
      };
      
      // Open a new tab, ready to receive the product URL
      var newTab = window.open('about:blank', '_blank');
      newTab.document.write("<div> <p> Generating Your Shirt </p> </div>");
    
      // Send the API request, and redirect the new tab to the URL that is returned
      fetch('https://teemill.com/omnis/v3/product/create', options)
        .then(response => response.json())
        .then(response => newTab.location.href = response.url)
        .catch(err => console.error(err));
})