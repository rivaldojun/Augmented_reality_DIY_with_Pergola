var table1 = document.getElementById("table");

// Création d'un tableau vide pour stocker les valeurs des colonnes
var values = [];

// Parcours de chaque ligne de la table (en ignorant la première ligne qui contient les en-têtes)
for (let i = 1; i < table1.rows.length; i++) {
  // Récupération des valeurs des deux colonnes
  const nom = table1.rows[i].cells[0].innerText;
  const nombre = parseInt(table1.rows[i].cells[1].innerText);
  
  // Stockage des valeurs dans un objet
  const rowValues = {
    nom: nom,
    nombre: nombre
  };
  
  // Ajout de l'objet au tableau de valeurs
  values.push(rowValues);

  fetch('/result', {
    
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(rowValues)
  })

}

