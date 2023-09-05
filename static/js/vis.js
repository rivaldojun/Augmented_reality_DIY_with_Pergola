const planeEl = document.querySelector('#my-plane');
    let rotationZ = 180;
    const mod=document.querySelector('#mod')
    const rotate = document.querySelector('#rotate');
let isRotating = false; 
let rotationInterval;

function rotatePlane() {
  rotationZ += 1;
  mod.setAttribute('rotation', {x: 180, y: rotationZ, z:180});
}

rotate.addEventListener('click', function() {
  if(isRotating){
    isRotating = false;
    clearInterval(rotationInterval); // arrête le setInterval
  } else {
    isRotating = true;
    rotationInterval = setInterval(rotatePlane, 20); // stocke l'identifiant renvoyé par setInterval
  }
});
let isnight=false;
const night=document.querySelector('#night')


  night.addEventListener('click', function() {
  if(isnight){
    var sky = document.querySelector("#sky");
    var light = document.querySelector("#light");
   
    

    sky.setAttribute("material", "src: static/day.jpg");
    light.setAttribute("intensity","1")
    isnight=false;
  } else {
    var sky = document.querySelector("#sky");
     var light = document.querySelector("#light");
     light.setAttribute("intensity","0.5")
    isnight = true;
    sky.setAttribute("material", "src: static/sky.jpg");
  }
});
const homeButton = document.getElementById('home');
homeButton.addEventListener('click', function() {
  window.location.href = '/accueil';
});

const Home = document.querySelector('#Home');
    const zoomInBtn = document.querySelector('#zoom-in-btn');
    const zoomOutBtn = document.querySelector('#zoom-out-btn');
    const cameraEl = document.querySelector('a-camera');
    const Bas = document.querySelector('#Bas');
    const Haut = document.querySelector('#Haut');


    
    zoomInBtn.addEventListener('click', function() {
      cameraEl.setAttribute('position', {x: cameraEl.object3D.position.x, y: cameraEl.object3D.position.y, z: cameraEl.object3D.position.z - 1});
    });

    zoomOutBtn.addEventListener('click', function() {
      cameraEl.setAttribute('position', {x: cameraEl.object3D.position.x, y: cameraEl.object3D.position.y, z: cameraEl.object3D.position.z + 1});
    });

    Bas.addEventListener('click', function() {
      cameraEl.setAttribute('position', {x: cameraEl.object3D.position.x, y: cameraEl.object3D.position.y-1, z: cameraEl.object3D.position.z });
    });

    Haut.addEventListener('click', function() {
      cameraEl.setAttribute('position', {x: cameraEl.object3D.position.x, y: cameraEl.object3D.position.y+1, z: cameraEl.object3D.position.z});
    });