import * as THREE from './three.module.js';
import {GLTFLoader} from './GLTFLoader.js';
import {OrbitControls} from './OrbitControls.js';
import {ARButton} from './ARButton.js';
// import {XRGestures} from '../../Three_debug/jsm/webxr/XRGestures.js';
//import MobileDetect from './node_modules/mobile-detect/mobile-detect.js';
//import QRCode from './qrcode.js';

let reticle;
let controller;
let hitTestSource;
let hitTestSourceRequested;
let modele;
let modele1;
let gestures;
let qrCodeDisplayed = false;

var monElement = document.querySelector('#hei');
var valeur = monElement.dataset.value;
valeur=parseInt(valeur)

var monmodel = document.querySelector('#model');
var model = monmodel.dataset.value;


//var container;
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

// container = document.createElement( 'div' );
const container =  document.getElementById('container');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);

const camera = new THREE.PerspectiveCamera(75,window.innerWidth / window.innerHeight, 0.01, 100);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha : true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.xr.enabled = true;
//container.appendChild(renderer.domElement);
if (container) {
    container.appendChild(renderer.domElement);
  } else {
    console.error('Container not found');
  }

const controls = new OrbitControls(camera, renderer.domElement);
controls.minDistance = 0;
controls.maxDistance = 40;

const arScene = new THREE.Scene();

const loader = new GLTFLoader();
loader.load(model, function(gltf){
    modele = gltf.scene.children[0]
    modele.position.set(-7.5,0,1);
    
   
    if(isMobile){
if(valeur==4)
{
    // plane.position.set(0,0, -15);
}
if(valeur==6)
{
    // plane.position.set(0,-6, -15);
}
if(valeur==5)
{
    // plane.position.set(0,1, -15);
}

            modele.position.set(-7.5,0,1);
    }
    scene.add(gltf.scene);
    modele1 = modele.clone();
    modele1.scale.set(0.4,13,0.4);
    //modele1.scale.set(1,1,1);
    //modele1.position.divide(modele1.scale);
    arScene.add(modele1);
    
}, undefined, function ( error ) {

	console.error( error );

});

hitTestSourceRequested = false;
hitTestSource = null;

//const md = new MobileDetect(window.navigator.userAgent);
//const isMobile = !!md.mobile();
let button1;
let button;
const h1 = document.querySelector('h1');
const h3 = document.querySelector('h3');

if(isMobile){
    button = ARButton.createButton(renderer, {requiredFeatures: ["hit-test"], optionalfeatures:['dom-overlay'],
        domOverlay:{root: document.body}  
    });

    button.addEventListener('click', function(){
        if(modele1 === undefined) return;
        modele1.visible = false;
    })
    document.body.appendChild(button);
}else{
    
    button1 = document.createElement('button');
    button1.innerHTML = 'START AR';
    button1.style.display = 'block';
    button1.style.height="60px"
    button1.style.width="200px"
    button1.style.backgroundColor="white"
    button1.style.textAlign="center"
    button1.style.fontSize="20px"
    button1.style.cursor="pointer"
    button1.style.fontWeight="bolder"
    button1.style.borderRadius="5px"
    button1.style.position = 'absolute';
    button1.style.bottom = '20px';  // Placer en bas avec une marge de 20px
    button1.style.left = 'calc(50% - 50px )';
    button1.style.transform = 'translateX(-50%)';
    document.body.appendChild(button1);
    //button1.visible = true;
    // button.visible = false;
    button1.addEventListener('click', function(){

        if (!qrCodeDisplayed && button1.innerHTML === 'START AR' ) {
            h1.style.display = 'block';
            h3.style.display = 'block';
            document.getElementById("qrcode").innerHTML = "";
            let qrCode = new QRCode("qrcode", {
                text: "https://fbeb-196-200-144-2.ngrok-free.app",
                width: 256,
                height: 256,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            });
            qrCode.makeCode("https://fbeb-196-200-144-2.ngrok-free.app");
            qrCodeDisplayed = true;
            document.getElementById("container").style.display = "none";
            document.querySelector("header").style.display = "flex";
            button1.innerHTML = 'RETOUR'
            button1.style.display = 'block';
            button1.style.height="60px"
            button1.style.width="200px"
            button1.style.backgroundColor="white"
            button1.style.textAlign="center"
            button1.style.fontSize="20px"
            button1.style.cursor="pointer"
            button1.style.fontWeight="bolder"
            button1.style.borderRadius="5px"
            button1.style.position = 'absolute';
            button1.style.left = 'calc(50% - 50px + 50px)';
            button1.style.bottom = '20px';  // Placer en bas avec une marge de 20px
            // button1.style.left = 'calc(50% - 50px )';
            // button1.style.transform = 'translateX(-50%)';
        }
        else if(button1.innerHTML === 'RETOUR'){
            modele1.visible = true;
            document.getElementById("container").style.display = "block";
            document.querySelector("header").style.display = "none";
            qrCodeDisplayed = false;
            button1.innerHTML = 'START AR';
            button1.style.display = 'block';
            button1.style.height="60px"
            button1.style.width="200px"
            button1.style.backgroundColor="white"
            button1.style.textAlign="center"
            button1.style.fontSize="20px"
            button1.style.cursor="pointer"
            button1.style.fontWeight="bolder"
            button1.style.borderRadius="5px"
            button1.style.position = 'absolute';
            button1.style.left = 'calc(50% - 50px + 50px)';
            button1.style.bottom = '20px';  // Placer en bas avec une marge de 20px
            // button1.style.left = 'calc(50% - 50px )';
            // button1.style.transform = 'translateX(-50%)';
        }
        

    })
    
}

const textureLoader = new THREE.TextureLoader();
const texture = textureLoader.load('static/image/grass.png');
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;
texture.repeat.set(120, 120); // répéter la texture 10 fois horizontalement et verticalement
const planeMaterial = new THREE.MeshStandardMaterial({ 
    map: texture, 
    color: 0xffffff, 
    roughness: 1,
    metalness: 0 
  });

const planeGeometry = new THREE.PlaneGeometry(500, 500);
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2; // pour tourner le plan de 90 degrés autour de l'axe x
scene.add(plane);
if(valeur==4)
{
    plane.position.set(0,-4, -15);
}
if(valeur==6)
{
    plane.position.set(0,-6, -15);
}
if(valeur==5)
{
    plane.position.set(0,-5, -15);
}



const directionalLight = new THREE.DirectionalLight( 0xffffff, 1 );
directionalLight.position.set( 0, 1, 1 ); // Positionne la lumière directionnelle
scene.add( directionalLight );
arScene.add( directionalLight.clone() );

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);
arScene.add(ambientLight.clone());

camera.position.set(-10,12,10);
camera.lookAt(0, -5, -5);


function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener('resize', onWindowResize, false);

function addreticle(){
    const geometry = new THREE.RingBufferGeometry(0.15, 0.2, 32).rotateX(
        -Math.PI / 2
    );
    const mat = new THREE.MeshBasicMaterial();
    reticle = new THREE.Mesh(geometry,mat);

    reticle.matrixAutoUpdate = false;
    reticle.visible = false;
    arScene.add(reticle);
}

addreticle();

function onSelect(){
    if(modele === undefined) return;

    if(reticle.visible){
        modele1.position.setFromMatrixPosition(reticle.matrix);
        //modele1.quaternion.setFromRotationMatrix(reticle.matrix);
        //modele1.rotateY(Math.PI / 2);
        modele1.rotation.set(0, Math.PI/2, 0);
        modele1.visible = true;
    }
}




controller = renderer.xr.getController(0);
controller.addEventListener('select', onSelect);
arScene.add(controller);

function requestHitTestSource(){

    const session = renderer.xr.getSession();

    session.requestReferenceSpace( 'viewer' ).then(function(referenceSpace){
        session.requestHitTestSource({space: referenceSpace}).then(function(source){
            hitTestSource = source;
        })
    });
    session.addEventListener('end', function(){
        hitTestSourceRequested = false;
        hitTestSource = null;
        referenceSpace = null;
    });
    hitTestSourceRequested = true;
}

function getHitTestResults(frame){

    const hitTestresults = frame.getHitTestResults(hitTestSource);
    if(hitTestresults.length){
        const referenceSpace = renderer.xr.getReferenceSpace();
        const hit = hitTestresults[0];
        const pose = hit.getPose(referenceSpace);
        
        reticle.visible = true;
        reticle.matrix.fromArray(pose.transform.matrix);
    }else{
        reticle.visible = false;
    }
}



function animate(){
    //requestAnimationFrame( animate );
    renderer.setAnimationLoop( render );
    controls.update();
}

function render(timestamp, frame){
    //renderer.render(scene,camera);
    if (renderer.xr.isPresenting && isMobile){
        //modele.visible = false;
        if(frame){
            if (hitTestSourceRequested === false)
            requestHitTestSource();
            if (hitTestSource)  getHitTestResults(frame);
        }
        renderer.render(arScene, camera);
    } else {
        renderer.render(scene, camera);
    }
}

animate();