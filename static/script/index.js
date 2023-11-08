/**
 * Canvas code taken from teemill API example page. https://codepen.io/Teemill/pen/ExLerwZ
 */

const canvas = document.getElementById('drawingCanvas');
// const canvasContainer = document.getElementById('drawingContainer'); //Wont work due to scope of the script, however if the script is not inside the div, it will cease to function.... help?????

const context = canvas.getContext('2d');

const color = '#000000';

// canvasContainer.id = "false";

canvas.width = 512;
canvas.height = 512;

var drawingMode = false;
var lastEvent = null;
var lastSize = 0;
var maxSize = 15;
var minSize = 2;

function drawCircle(x, y, radius, color) {
  context.fillStyle = color;
  context.beginPath();
  const canvasRect = canvas.getBoundingClientRect();
  const canvasScale = canvas.width / canvasRect.width;
  context.save();
  context.scale(canvasScale, canvasScale);
  context.arc(
    x - canvasRect.x,
    y - canvasRect.y,
    radius, 0,
    Math.PI * 2,
  );
  context.fill();
  context.closePath();
  context.restore();
}

function onMouseDown(e) {
//   canvasContainer.id = "true";
  if (e.touches) {
    e = e.touches[0];
  }

  lastEvent = e;
  drawingMode = true;
}

function onMouseUp() {
  drawingMode = false;
}

function onMouseMove(e) {
  if (!drawingMode) {
    return;
  }
  if (e.touches) {
    e.preventDefault();
    e = e.touches[0];
  }
  let size = 1;
  
  // calculate the distance between the points and scale the size of the new circle based on that distance
  const deltaX = e.pageX - lastEvent.pageX;
  const deltaY = e.pageY - lastEvent.pageY;
  const distanceToLastMousePosition = Math.sqrt(
    (deltaX ** 2) +
    (deltaY ** 2)
  );

  size = Math.max(minSize, Math.min(maxSize, distanceToLastMousePosition / 3));
  
  if (drawingMode) {
    drawCircle(e.pageX, e.pageY, size, color);
  }
  
  if (lastSize) {
    const deltaSize = size - lastSize;
    
    for (let i = 0; i < distanceToLastMousePosition; i += 1) {
      const shift = (i / distanceToLastMousePosition);
      // draw circles between our new mouse position and our previous one, to smooth the line out
      drawCircle(
        e.pageX - (deltaX * shift),
        e.pageY - (deltaY * shift),
        size - (deltaSize * shift),
        color
      );
    }
  }

  lastEvent = e;
  lastSize = size;
}

canvas.addEventListener('mousedown', onMouseDown);
canvas.addEventListener('touchstart', onMouseDown);

canvas.addEventListener('mousemove', onMouseMove);
canvas.addEventListener('touchmove', onMouseMove);

window.addEventListener('mouseup', onMouseUp);
window.addEventListener('touchend', onMouseUp);


    