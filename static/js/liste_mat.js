const cells = document.querySelectorAll('td');
  const images = [
    'static\te.png',
    'static\bois.jpg',
    'static\tr.png'
  ];

  cells.forEach((cell, index) => {
    const tooltip = document.createElement('div');
    tooltip.classList.add('tooltip');
  

    cell.addEventListener('mouseover', () => {
      const cellRect = cell.getBoundingClientRect();
      tooltip.style.top = `${cellRect.top - tooltip.offsetHeight}px`;
      tooltip.style.left = `${cellRect.left + cellRect.width / 2}px`;
      tooltip.style.display = 'block';
    });
    
    cell.addEventListener('mouseout', () => {
      tooltip.style.display = 'none';
    });

    document.body.appendChild(tooltip);
  });



  
    