document.addEventListener("DOMContentLoaded", function () {

  // --- NEU: LOGIK FÜR HAMBURGER MENÜ ---
  const menuToggle = document.getElementById('mobile-menu-toggle');
  if (menuToggle) {
    menuToggle.addEventListener('click', function() {
      // Fügt die Klasse .nav-open zum <body> hinzu oder entfernt sie.
      // Das CSS kümmert sich um den Rest.
      document.body.classList.toggle('nav-open');
    });
  }

  // --- KORRIGIERTER TOOLTIP-ANSATZ: Ein einziger, globaler Tooltip ---
  function createGlobalTooltip() {
    // Erstellt das Tooltip-Element, falls es noch nicht existiert
    if (document.getElementById('global-tooltip')) return;
    
    const tooltip = document.createElement('div');
    tooltip.id = 'global-tooltip';
    // Styling wird direkt hier gesetzt, keine CSS-Datei nötig
    Object.assign(tooltip.style, {
      position: 'fixed', // Bleibt an der gleichen Stelle, auch beim Scrollen
      backgroundColor: '#ff7e5f',
      color: 'white',
      padding: '5px 10px',
      borderRadius: '5px',
      fontSize: '14px',
      fontWeight: 'bold',
      pointerEvents: 'none', // Verhindert, dass der Tooltip die Maus blockiert
      zIndex: '9999', // Immer im Vordergrund
      display: 'none' // Standardmäßig unsichtbar
    });
    document.body.appendChild(tooltip);
    return tooltip;
  }

  const globalTooltip = createGlobalTooltip();

  // --- TEIL 1: SLIDESHOW ---
  const slides = document.querySelectorAll(".slide");
  let currentSlide = 0;
  function showNextSlide() {
    if (slides.length === 0) return;
    slides[currentSlide].classList.remove("active");
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add("active");
  }
  if (slides.length > 1) {
    setInterval(showNextSlide, 3000);
  }

  // --- TEIL 2: ALLGEMEINE VARIABLEN UND FUNKTIONEN ---
  const previewContent = document.getElementById("preview-content");
  const navLeft = document.querySelector(".nav-left");
  const navRight = document.querySelector(".nav-right");
  const initialContent = previewContent.innerHTML;

  // Ladefunktion für die LINKE Navigation
  function loadHtmlContent(sectionName) {
    const currentLangParam = window.location.search; 
    const url = `/load/${sectionName}${currentLangParam}`;

    previewContent.innerHTML = '<p>Lade Inhalt...</p>';
    fetch(url)
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.text();
      })
      .then(html => { 
        previewContent.innerHTML = html; 
      })
      .catch(e => {
        console.error("Fehler beim Laden des HTML-Inhalts:", e);
        previewContent.innerHTML = `<p style="color: red;">Fehler: Der Inhalt konnte nicht geladen werden.</p>`;
      });
  }

  // --- LINKE NAVIGATION ---
  if (navLeft) {
    navLeft.addEventListener("click", function (event) {
      const button = event.target.closest('button[data-section]');
      if (button) { loadHtmlContent(button.dataset.section); }
    });
    navLeft.addEventListener('mouseover', function(event) {
      if (event.target.closest('button[data-section]')) {
        globalTooltip.textContent = 'click';
        globalTooltip.style.display = 'block';
      }
    });
    navLeft.addEventListener('mouseout', function(event) {
      if (event.target.closest('button[data-section]')) {
        globalTooltip.style.display = 'none';
      }
    });
  }

  // --- TEIL 3: RECHTE NAVIGATION ---
  if (navRight) {
    let fetchTimeout;

    // EINZIGER 'mouseover' LISTENER FÜR DIE RECHTE NAVIGATION
    navRight.addEventListener('mouseover', function(event) {
      const link = event.target.closest('.file-list-item a');
      if (link && link.href.includes('/static/certificates')) {
        const filePath = link.href;
        const fileExtension = filePath.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension)) {
          previewContent.innerHTML = `<img src="${filePath}" style="max-width: 100%; height: auto; border-radius: 8px;">`;
        } else if (fileExtension === 'pdf') {
          previewContent.innerHTML = `<iframe src="${filePath}" style="width: 100%; height: 60vh; border: none;"></iframe>`;
        }
        globalTooltip.textContent = 'click';
        globalTooltip.style.display = 'block';
        return;
      }
      
      const container = event.target.closest('.accordion-container');
      if (container) {
        const fileList = container.querySelector('.file-list');
        if (fileList.children.length > 0) return;
        
        const category = container.dataset.category;
        const currentLangParam = window.location.search;
        clearTimeout(fetchTimeout);
        fetchTimeout = setTimeout(() => {
          fetch(`/certificates/${category}${currentLangParam}`)
            .then(response => response.json())
            .then(files => {
              fileList.innerHTML = ''; 
              if (files.length === 0) {
                fileList.innerHTML = '<li class="file-list-item"><a>Keine Einträge</a></li>';
              } else {
                files.forEach(file => {
                  const listItem = document.createElement('li');
                  listItem.className = 'file-list-item';
                  const fileLink = document.createElement('a');
                  fileLink.href = `/static/certificates/${category}/${file}`;
                  fileLink.textContent = file.split('.').slice(0, -1).join('.').replace(/_/g, ' ');
                  fileLink.target = "_blank";
                  listItem.appendChild(fileLink);
                  fileList.appendChild(listItem);
                });
              }
            });
        }, 10);
      }
    });

    // EINZIGER 'mouseout' LISTENER FÜR DIE RECHTE NAVIGATION
    navRight.addEventListener('mouseout', function(event) {
      const link = event.target.closest('.file-list-item a');
      if (link) {
        globalTooltip.style.display = 'none';
      }
      
      if (!navRight.contains(event.relatedTarget)) {
        previewContent.innerHTML = initialContent;
        globalTooltip.style.display = 'none';
      }
    });
  }

  // --- Globaler Listener für die Mausbewegung ---
  document.addEventListener('mousemove', function(event) {
      if (globalTooltip.style.display === 'block') {
        globalTooltip.style.left = `${event.clientX + 15}px`;
        globalTooltip.style.top = `${event.clientY}px`;
      }
  });

});
