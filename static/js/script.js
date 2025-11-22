document.addEventListener("DOMContentLoaded", function () {
  // --- NEU: LOGIK FÜR HAMBURGER MENÜ ---
  const menuToggle = document.getElementById("mobile-menu-toggle");
  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      // Fügt die Klasse .nav-open zum <body> hinzu oder entfernt sie.
      document.body.classList.toggle("nav-open");
    });
  }

  // --- KORRIGIERTER TOOLTIP-ANSATZ: Ein einziger, globaler Tooltip ---
  function createGlobalTooltip() {
    if (document.getElementById("global-tooltip"))
      return document.getElementById("global-tooltip");

    const tooltip = document.createElement("div");
    tooltip.id = "global-tooltip";
    Object.assign(tooltip.style, {
      position: "fixed",
      backgroundColor: "#ff7e5f",
      color: "white",
      padding: "5px 10px",
      borderRadius: "5px",
      fontSize: "14px",
      fontWeight: "bold",
      pointerEvents: "none",
      zIndex: "9999",
      display: "none",
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
    // RESPONSIVE: Nach dem Klick das Menü schließen
    document.body.classList.remove("nav-open");

    const currentLangParam = window.location.search;
    const url = `/load/${sectionName}${currentLangParam}`;

    previewContent.innerHTML = "<p>Lade Inhalt...</p>";
    fetch(url)
      .then((response) => {
        if (!response.ok)
          throw new Error(`HTTP error! status: ${response.status}`);
        return response.text();
      })
      .then((html) => {
        previewContent.innerHTML = html;
      })
      .catch((e) => {
        console.error("Fehler beim Laden des HTML-Inhalts:", e);
        previewContent.innerHTML = `<p style="color: red;">Fehler: Der Inhalt konnte nicht geladen werden.</p>`;
      });
  }

  // --- LINKE NAVIGATION ---
  if (navLeft) {
    navLeft.addEventListener("click", function (event) {
      const button = event.target.closest("button[data-section]");
      if (button) {
        loadHtmlContent(button.dataset.section);
      }
    });
    // RESPONSIVE: Tooltip für die linke Navigation wurde entfernt
  }

  // --- TEIL 3: RECHTE NAVIGATION ---
  if (navRight) {
    let fetchTimeout;

    // EINZIGER 'mouseover' LISTENER FÜR DIE RECHTE NAVIGATION
    navRight.addEventListener("mouseover", function (event) {
      const link = event.target.closest(".file-list-item a");
      if (link && link.href.includes("/static/certificates")) {
        const filePath = link.href;
        const fileExtension = filePath.split(".").pop().toLowerCase();
        if (["jpg", "jpeg", "png", "gif"].includes(fileExtension)) {
          previewContent.innerHTML = `<img src="${filePath}" style="max-width: 100%; height: auto; border-radius: 8px;">`;
        } else if (fileExtension === "pdf") {
          previewContent.innerHTML = `<iframe src="${filePath}" style="width: 100%; height: 60vh; border: none;"></iframe>`;
        }

        // RESPONSIVE: Tooltip-Text geändert
        globalTooltip.textContent = "double touch";
        globalTooltip.style.display = "block";
        return;
      }

      const container = event.target.closest(".accordion-container");
      if (container) {
        const fileList = container.querySelector(".file-list");
        if (fileList.children.length > 0) return;

        const category = container.dataset.category;
        const currentLangParam = window.location.search;
        clearTimeout(fetchTimeout);
        fetchTimeout = setTimeout(() => {
          fetch(`/certificates/${category}${currentLangParam}`)
            .then((response) => response.json())
            .then((files) => {
              fileList.innerHTML = "";
              if (files.length === 0) {
                fileList.innerHTML =
                  '<li class="file-list-item"><a>Keine Einträge</a></li>';
              } else {
                files.forEach((file) => {
                  const listItem = document.createElement("li");
                  listItem.className = "file-list-item";
                  const fileLink = document.createElement("a");
                  fileLink.href = `/static/certificates/${category}/${file}`;
                  fileLink.textContent = file
                    .split(".")
                    .slice(0, -1)
                    .join(".")
                    .replace(/_/g, " ");
                  fileLink.target = "_blank";
                  listItem.appendChild(fileLink);
                  fileList.appendChild(listItem);
                });
              }
            });
        }, 10);
      }
    });

    // EINZIGER 'mouseout' LISTENER
    navRight.addEventListener("mouseout", function (event) {
      const link = event.target.closest(".file-list-item a");
      if (link) {
        globalTooltip.style.display = "none";
      }

      if (!navRight.contains(event.relatedTarget)) {
        previewContent.innerHTML = initialContent;
        globalTooltip.style.display = "none";
      }
    });
  }

  // EIN globaler Listener für die Mausbewegung
  document.addEventListener("mousemove", function (event) {
    if (globalTooltip.style.display === "block") {
      globalTooltip.style.left = `${event.clientX + 15}px`;
      globalTooltip.style.top = `${event.clientY}px`;
    }
  });
});

// ---- CTA unter dem Profilbild automatisch ein-/ausblenden ---------------
(function () {
  const preview = document.getElementById("preview-content");
  const cta = document.getElementById("ctaUnderProfile");
  if (!preview || !cta) return;

  function profileVisible() {
    // Profile-Startzustand: figure.profile-figure existiert (und ist sichtbar)
    return !!preview.querySelector(".profile-figure");
  }

  function updateCTA() {
    // CTA nur zeigen, wenn NUR das Profilbild im Preview steht
    // (sprich: sobald Content via Navigation/Akkordeon geladen wird -> ausblenden)
    const show = profileVisible();
    cta.classList.toggle("is-hidden", !show);
  }

  // 1) Beim ersten Laden
  updateCTA();

  // 2) Auf DOM-Wechsel im Preview reagieren (Navigation lädt andere Inhalte hinein)
  const mo = new MutationObserver(updateCTA);
  mo.observe(preview, { childList: true, subtree: true });

  // 3) Sicherstellen, dass ein Klick links/rechts (der Content lädt) das Update triggert
  const navLeft = document.querySelector(".nav-left");
  const navRight = document.querySelector(".nav-right");
  [navLeft, navRight].forEach((el) => {
    if (!el) return;
    el.addEventListener("click", () => setTimeout(updateCTA, 50));
  });
  // -----------------------------------------------------
  // NEWS-TICKER: Distanz & Dauer dynamisch setzen
  // -----------------------------------------------------
  function initNewsTicker() {
    const ticker = document.querySelector(".news-ticker");
    if (!ticker) return;

    const viewport = ticker.querySelector(".news-ticker__viewport");
    const track = ticker.querySelector(".news-ticker__track");
    if (!viewport || !track) return;

    const firstItem = track.querySelector(".news-ticker__item");
    if (!firstItem) return;

    // Breiten messen
    const firstWidth = firstItem.getBoundingClientRect().width;
    const viewportWidth = viewport.getBoundingClientRect().width;

    // gap aus CSS-Variable lesen (Fallback: 48px)
    const styles = getComputedStyle(track);
    const gapValue =
      styles.getPropertyValue("gap") || styles.getPropertyValue("column-gap");
    const gap = parseFloat(gapValue) || 48;

    // Distanz = Textbreite + Gap
    // -> Wenn der erste Text komplett raus ist, sitzt der zweite an seiner Stelle.
    const distance = firstWidth + gap;

    track.style.setProperty("--ticker-distance", distance + "px");

    // Optional: Dauer zusätzlich an Distanz koppeln (lesbare Geschwindigkeit)
    // Wenn du NUR die CSS-Variable --ticker-speed nutzen willst,
    // kommentiere die nächsten 3 Zeilen einfach aus.
    const pxPerSecond = 80; // je größer, desto schneller
    const duration = distance / pxPerSecond;
    track.style.animationDuration = duration + "s";
  }

  document.addEventListener("DOMContentLoaded", () => {
    initNewsTicker();
    window.addEventListener("resize", () => {
      // bei Resize neu berechnen
      initNewsTicker();
    });
  });
})();
