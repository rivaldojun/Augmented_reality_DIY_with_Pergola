let selectedSquares =[];
// let matrice = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
function toggleSquare(square) {
  const index = selectedSquares.indexOf(square);
  if (index === -1) {
    // Le carré n'est pas encore sélectionné, on l'ajoute à la liste
    selectedSquares.push(square);
    square.classList.remove('plus');
    square.classList.add('minus');
    square.classList.add('clicked');
    // localStorage.setItem('selectedSquares', JSON.stringify(selectedSquares)); // Enregistrer les carrés sélectionnés dans le localStorage

  } else {
    // Le carré est déjà sélectionné, on le supprime de la liste
    selectedSquares.splice(index, 1);
    square.classList.remove('minus');
    square.classList.add('plus');
    square.classList.remove('clicked');
    // localStorage.setItem('selectedSquares', JSON.stringify(selectedSquares)); // Enregistrer les carrés sélectionnés dans le localStorage

  }
}

function handleSquareClick(event) {
  const square = event.target;
  toggleSquare(square);
}


// function handleSubmit(event) {
//   event.preventDefault();
// const selectedValues = selectedSquares.map(square => square.dataset.square);
  
//   const matrice = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
//   for (let i = 0; i < selectedValues.length; i++) {
//     const position = selectedValues[i];
    
//     const row = Math.floor((parseInt(position)-1) / 4);
//    // calcul de la ligne
//     const col = (parseInt(position) - 1) % 4; // calcul de la colonne
     

// }

  
  
// }


const squares = document.querySelectorAll('.square');
squares.forEach(square => square.addEventListener('click', handleSquareClick));

var materiaux = document.getElementById("materiaux");
var visualiser = document.getElementById("visualiser");


window.addEventListener('load', function() {
  var materiaux = document.getElementById("materiaux");
  var visualiser = document.getElementById("visualiser");
  var mat = localStorage.getItem('mat');
  var vis = localStorage.getItem('vis');
  if (mat === 'visible') {
    materiaux.style.display = 'block';
  } else {
    materiaux.style.display = 'none';
  }

  if (vis === 'visible') {
    visualiser.style.display = 'block';
  } else {
    visualiser.style.display = 'none';
  }
  var button=document.getElementById("button");


  function checkAdjacent(pergolas) {
    
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 4; j++) {
        if (pergolas[i][j] === 1) {
          let adjacent = false;
  
          for (let row = Math.max(0, i - 1); row <= Math.min(2, i + 1); row++) {
            for (let col = Math.max(0, j - 1); col <= Math.min(3, j + 1); col++) {
              if (row !== i || col !== j) {
                if (pergolas[row][col] === 1) {
                  adjacent = true;
                  break;
                }
              }
            }
            if (adjacent) {
              break;
            }
          }
  
          if (!adjacent) {
            return false;
          }
        }
      }
    }
  
    return true;
  }
  
var al=document.getElementsByClassName("alert");
function update(){
  let sum = 0;
  const selectedValues = selectedSquares.map(square => square.dataset.square);
  
  const matrice = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
  for (let i = 0; i < selectedValues.length; i++) {
    const position = selectedValues[i];
    
    const row = Math.floor((parseInt(position)-1) / 4);
   // calcul de la ligne
    const col = (parseInt(position) - 1) % 4; // calcul de la colonne
    matrice[row][col] = 1;
    sum=sum+matrice[row][col]
}
let adj=false;
adj=checkAdjacent(matrice)


if ((sum === 0)||((sum>1)&&(adj===false))) {
  // désactive le bouton submit si la somme est nulle
  button.disabled = true;
  al[0].style.display="block"
}
else{
  button.disabled = false;
  al[0].style.display="none"
}
}


update();

squares.forEach(square => square.addEventListener('click', update));



  
  // Ajouter un écouteur d'événements au formulaire
  var form = document.getElementById('select-square-form');
  
  form.addEventListener('submit', function(event) {
    
    // Code pour valider le formulaire et afficher le lien "visualiser"
    
    // Stocker la valeur "visible" dans le stockage local
    localStorage.setItem('mat', 'visible');
    localStorage.setItem('vis', 'visible');

    materiaux.style.display = 'block';
    visualiser.style.display = 'block';
  });

  var logout = document.getElementById('logout');
  logout.addEventListener('click', function(event) {
    
    // Code pour valider le formulaire et afficher le lien "visualiser"
    
    // Stocker la valeur "visible" dans le stockage local
    localStorage.setItem('mat', 'invisible');
    localStorage.setItem('vis', 'invisible');
    materiaux.style.display = 'none';
    visualiser.style.display = 'none';
  });
});

const ismobile=/Android|webOS|iphone/i.test(navigator.userAgent);

if(ismobile){

  var grids=document.getElementsByClassName("grid");

  for(var i=0; i<squares.length; i++){
    // squares[i].style.width="250px"
    squares[i].style.height="250px"
    squares[i].style.width="250px"
    squares[i].style.lineHeight="250px"
    
    

  }
  
  grids[0].style.position="absolute"
  grids[0].style.top="400px"
  grids[0].style.bottom="3200px"
  grids[0].style.left="800px"
  grids[0].style.gridTemplateColumns = "repeat(4, 250px)";
  grids[0].style.gridTemplateRows = "repeat(3, 250px)";

  var option=document.getElementsByClassName("options-container");
  option[0].style.position="relative"
  option[0].style.top="220px"
  option[0].style.left="1250px"
  option[0].style.width="350px"
  option[0].style.height="600px"
  option[0].style.borderRadius="0px"

  var button=document.getElementById("button");

  button.style.marginLeft="75px"
  button.style.marginTop="70px"
  button.style.scale="1.2"

var titre=document.getElementsByClassName("obj");
titre[0].style.marginLeft="700px"
titre[0].style.fontSize="50px"



// var co=document.getElementsByClassName("color-options");
// var ho=document.getElementsByClassName("height-options");
// var so=document.getElementsByClassName("size-options");
// var to=document.getElementsByClassName("type-options");
// ho[0].style.marginLeft="100px"
// ho[0].style.marginTop="80px"
// co[0].style.marginLeft="100px"
// co[0].style.marginTop="80px"
// to[0].style.marginLeft="150px"
// to[0].style.marginTop="80px"
// so[0].style.marginLeft="100px"
// so[0].style.marginTop="80px"

// var cos=document.getElementById("color");
// var hos=document.getElementById("height");
// var sos=document.getElementById("taille");
// var tos=document.getElementById("type");

// cos.style.height="300px"
// cos.style.paddingBottom="100px"
// hos.style.height="300px"
// hos.style.paddingBottom="100px"
// sos.style.height="300px"
// sos.style.paddingBottom="100px"
// tos.style.height="300px"
// tos.style.paddingBottom="100px"

// var black=document.getElementById("black");
// black.style.scale="3"
// black.style.marginRight="150px"

// var red=document.getElementById("red");
// red.style.scale="3"
// red.style.marginRight="150px"
// var blue=document.getElementById("blue");
// blue.style.scale="3"
// blue.style.marginRight="150px"
// var white=document.getElementById("white");
// white.style.scale="3"
// white.style.marginRight="150px"

// var m4=document.getElementById("4m");
// m4.style.scale="3"
// m4.style.marginRight="200px"
// var m5=document.getElementById("5m");
// m5.style.scale="3"
// m5.style.marginRight="200px"
// var m6=document.getElementById("6m");
// m6.style.scale="3"
// m6.style.marginRight="100px"

// var t1=document.getElementById("1");
// t1.style.scale="3"
// t1.style.marginRight="200px"
// var t2=document.getElementById("2");
// t2.style.scale="3"
// t2.style.marginRight="200px"
// var t3=document.getElementById("3");
// t3.style.scale="3"
// t3.style.marginRight="100px"

// var ouv=document.getElementById("ouv");
// ouv.style.scale="3"
// ouv.style.marginRight="200px"
// var ferm=document.getElementById("ferm");
// ferm.style.scale="3"
// ferm.style.marginRight="150px"


// var th1=document.getElementsByClassName("ent");
// th1[0].style.fontSize="60px"
// th1[0].style.paddingTop="70px"

// var c=document.getElementsByClassName("c");
// c[0].style.fontSize="60px"

// var h=document.getElementsByClassName("h");
// h[0].style.fontSize="60px"

// var ta=document.getElementsByClassName("ta");
// ta[0].style.fontSize="60px"

// var ty=document.getElementsByClassName("ty");
// ty[0].style.fontSize="60px"
var msg=document.getElementsByClassName("alert");
msg[0].style.left='80%'

}


