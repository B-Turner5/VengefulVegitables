document.getElementById('open-camera-button').addEventListener('click', function () {
  fetch('/update_shirt_texture', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    // body: JSON.stringify({"prompt": prompt})
  })
  .then(response => 
  {
    document.getElementById("camera-overlay").style.display = "flex";
    window.scrollTo(0, 0);
    document.getElementsByTagName("body")[0].style.overflowY = "hidden";
    
    var frame = document.getElementById("iframe");
    var cont = frame.innerHTML;
    frame.innerHTML = cont; 
    
    //document.getElementById('TSHIRT_model');
    //TSHIRT_model.setAttribute(obj-model, "obj: url(/static/assets/tshirt/tshirt.obj); mtl: url(/static/assets/tshirt/tshirt.mtl)");
})

document.getElementById('close-camera-button').addEventListener('click', function () {
  document.getElementById("camera-overlay").style.display = "none";
  document.getElementsByTagName("body")[0].style.overflowY = "scroll";
})

let ctx = canvas.getContext("2d");

document.getElementById('clear-image-button').addEventListener('click', function () {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawingMade = false;

  document.getElementById('gen-button-container').style.display = "flex";
  document.getElementById('extra-button-container').style.display = "none";
  document.getElementById('output-image').style.display = "none";
  document.getElementById('loader').style.display = "none";
})



document.getElementById('purchase-item-button').addEventListener('click', function () {
  const apiKey = 'OdCOVs1LdtwCLoeC5VE22JHETdNSyq75aY2ahGdt'; 
  var img = document.getElementById('output-image');

  // Create a canvas element
  var myCanvas = document.createElement('canvas');
  var myContext = myCanvas.getContext('2d');

  // Set canvas dimensions to match the image
  myCanvas.width = img.naturalWidth;
  myCanvas.height = img.naturalHeight;

  // Draw the image onto the canvas
  myContext.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);

  // Get the base64 data from the canvas
  var base64String = myCanvas.toDataURL('image/png'); // You can change the format as needed

  // Display or use the base64 string
  console.log('Base64 String:', base64String);


    const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          image_url: base64String,
          item_code: "RNA1",
          name: "Limited Edition Vengeful Vegetables Tee ",
          colours: "White",
          description: "For those people who absolutely detest meat and want to watch the world burn.",
          price: 20.00,
        }),
      };
      
      // Open a new tab, ready to receive the product URL
      var newTab = window.open('/generating');
    
      // Send the API request, and redirect the new tab to the URL that is returned
      fetch('https://teemill.com/omnis/v3/product/create', options)
        .then(response => response.json())
        .then(response => newTab.location.href = response.url)
        .catch(err => console.error(err));
})})