// Récupérer tous les éléments "a" dans la barre latérale
const sidebarLinks = document.querySelectorAll('.sidebar ul li');

// Parcourir chaque élément "a"
sidebarLinks.forEach(link => {
  // Ajouter un écouteur d'événements de clic à chaque élément "a"
  link.addEventListener('click', function(event) {
    // Empêcher le comportement par défaut de l'événement de clic
    
     event.preventDefault();
    


    // Supprimer la classe "selected" de tous les éléments "a" dans la barre latérale
    sidebarLinks.forEach(link => {
      link.classList.remove('selected');
    });

    // Ajouter la classe "selected" à l'élément "a" qui a été cliqué
    this.classList.add('selected');
  });
});

const ismobile=/Android|webOS|iphone/i.test(navigator.userAgent);

if(ismobile){

  var sidebar=document.getElementsByClassName("sidebar");
  sidebar.style.height="39px"

  
}