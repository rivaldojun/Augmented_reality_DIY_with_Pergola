const colorOptions = document.querySelectorAll('.color-option');
const heightOptions = document.querySelectorAll('.height-option');
const sizeOptions = document.querySelectorAll('.size-option');
const typeOptions = document.querySelectorAll('.type-option');

const selectedOptioncol = Array.from(colorOptions).find(option => option.classList.contains('selected'));

const selectedOptionhei = Array.from(heightOptions).find(option => option.classList.contains('selected'));

const selectedOptionsiz = Array.from(sizeOptions).find(option => option.classList.contains('selected'));
const selectedOptiontyp = Array.from(typeOptions).find(option => option.classList.contains('selected'));

color= selectedOptioncol.getAttribute('value');
height= selectedOptionhei.getAttribute('value');
size= selectedOptionsiz.getAttribute('value');
type= selectedOptiontyp.getAttribute('value');

colorOptions.forEach(option => {
  
  // color= option.getAttribute('value')
  option.addEventListener('click', () => {
    
    colorOptions.forEach(option => {
      option.classList.remove('selected');
    });
    option.classList.add('selected');
   color= option.getAttribute('value')
    // alert(color)
  });
  
});

heightOptions.forEach(option => {
  // height= option.getAttribute('value')
  option.addEventListener('click', () => {
    heightOptions.forEach(option => {
      option.classList.remove('selected');
    });
    option.classList.add('selected');
    height= option.getAttribute('value')
    // alert(height)
    
  });
  
});

sizeOptions.forEach(option => {
  option.addEventListener('click', () => {
    sizeOptions.forEach(option => {
      option.classList.remove('selected');
    });
    option.classList.add('selected');
  });
});

typeOptions.forEach(option => {
  // type= option.getAttribute('value')
  option.addEventListener('click', () => {
    typeOptions.forEach(option => {
      option.classList.remove('selected');
    });
    option.classList.add('selected');
    type= option.getAttribute('value')
    // alert(type)
  });
});


function handleSubmit(event) {
  event.preventDefault();
  const selectedValues = selectedSquares.map(square => square.dataset.square);
  
  const matrice = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
  for (let i = 0; i < selectedValues.length; i++) {
    const position = selectedValues[i];
    
    const row = Math.floor((parseInt(position)-1) / 4);
    const col = (parseInt(position) - 1) % 4;
    matrice[row][col] = 1;
  }
  const data = {
    'matrix':matrice,
    'type':type,
    'color': color,
    'height': height
  };

  // Envoi de la matrice à Flask via une requête AJAX
  fetch('/accueil', {
    
    method: 'POST',redirect:'follow',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {response.json(),window.location.href='/result'})
  .then(data => {
    console.log(data);
    
  })
  .catch(error => {
    console.error(error);
  });
};

const form = document.getElementById('select-square-form');
form.addEventListener('submit', handleSubmit);
