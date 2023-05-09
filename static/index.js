// Récupère toutes les cartes avec la classe .carte-zoom
const cartes = document.querySelectorAll('.carte-zoom');

// Crée un élément de superposition pour l'image agrandie
const overlay = document.createElement('div');
overlay.classList.add('carte-overlay');

// Crée un élément d'image pour afficher l'image agrandie
const image = document.createElement('img');
image.classList.add('carte-zoomed-image');
overlay.appendChild(image);

// Ajoute un gestionnaire d'événements click pour chaque carte avec la classe .carte-zoom
cartes.forEach(carte => {
  carte.addEventListener('click', () => {
    // Récupère l'URL de l'image agrandie depuis l'attribut data-zoom
    const url = carte.dataset.zoom;

    // Met à jour l'URL de l'image affichée dans l'élément d'image
    image.src = url;

    // Ajoute l'élément de superposition à la page
    document.body.appendChild(overlay);

    // Désactive le défilement de la page
    document.body.style.overflow = 'hidden';
  });
});

// Ajoute un gestionnaire d'événements click pour l'élément de superposition
overlay.addEventListener('click', () => {
  // Supprime l'élément de superposition de la page
  document.body.removeChild(overlay);

  // Réactive le défilement de la page
  document.body.style.overflow = '';
});