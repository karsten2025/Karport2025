// ---------------------------------------------------------
// HAUPTBLOCK: wird nach DOMContentLoaded ausgeführt
// ---------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
  // --- HAMBURGER MENÜ ---
  const menuToggle = document.getElementById("mobile-menu-toggle");
  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
    });
  }

  // --- GLOBALER TOOLTIP ---
  function createGlobalTooltip() {
    const existing = document.getElementById("global-tooltip");
    if (existing) return existing;

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

  // --- SLIDESHOW ---
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

  // --- PREVIEW / NAVIGATION ---
  const previewContent = document.getElementById("preview-content");
  const navLeft = document.querySelector(".nav-left");
  const navRight = document.querySelector(".nav-right");
  const initialContent = previewContent ? previewContent.innerHTML : "";

  // Aktuelle Sprache bestimmen (aus data-lang oder ?lang=de|en)
  function getCurrentLang() {
    const bodyAttr = document.body.getAttribute("data-lang");
    if (bodyAttr === "de" || bodyAttr === "en") return bodyAttr;

    const params = new URLSearchParams(window.location.search);
    const fromParam = params.get("lang");
    if (fromParam === "de" || fromParam === "en") return fromParam;

    return "de";
  }
  const CURRENT_LANG = getCurrentLang();

  // Inhalte aus Flask-Partials nachladen
  function loadHtmlContent(sectionName) {
    document.body.classList.remove("nav-open");
    const currentLangParam = window.location.search;
    const url = "/load/" + sectionName + currentLangParam;

    if (previewContent) {
      previewContent.innerHTML = "<p>Lade Inhalt...</p>";
    }

    fetch(url)
      .then(function (response) {
        if (!response.ok) {
          throw new Error("HTTP error! status: " + response.status);
        }
        return response.text();
      })
      .then(function (html) {
        if (previewContent) {
          previewContent.innerHTML = html;
        }
      })
      .catch(function (e) {
        console.error("Fehler beim Laden des HTML-Inhalts:", e);
        if (previewContent) {
          previewContent.innerHTML =
            '<p style="color: red;">Fehler: Der Inhalt konnte nicht geladen werden.</p>';
        }
      });
  }

  // Linke Navigation
  if (navLeft) {
    navLeft.addEventListener("click", function (event) {
      const button = event.target.closest("button[data-section]");
      if (button) {
        loadHtmlContent(button.dataset.section);
      }
    });
  }

  // Rechte Navigation (Accordion + Previews)
  if (navRight) {
    let fetchTimeout;

    navRight.addEventListener("mouseover", function (event) {
      const link = event.target.closest(".file-list-item a");
      if (link && link.href.indexOf("/static/certificates") !== -1) {
        const filePath = link.href;
        const fileExtension = filePath.split(".").pop().toLowerCase();

        if (previewContent) {
          if (["jpg", "jpeg", "png", "gif"].indexOf(fileExtension) !== -1) {
            previewContent.innerHTML =
              '<img src="' +
              filePath +
              '" style="max-width: 100%; height: auto; border-radius: 8px;">';
          } else if (fileExtension === "pdf") {
            previewContent.innerHTML =
              '<iframe src="' +
              filePath +
              '" style="width: 100%; height: 60vh; border: none;"></iframe>';
          }
        }

        globalTooltip.textContent = "double touch";
        globalTooltip.style.display = "block";
        return;
      }

      const container = event.target.closest(".accordion-container");
      if (container) {
        const fileList = container.querySelector(".file-list");
        if (fileList.children.length > 0) return;

        const category = container.getAttribute("data-category");
        const currentLangParam = window.location.search;

        clearTimeout(fetchTimeout);
        fetchTimeout = setTimeout(function () {
          fetch("/certificates/" + category + currentLangParam)
            .then(function (response) {
              return response.json();
            })
            .then(function (files) {
              fileList.innerHTML = "";
              if (!files || files.length === 0) {
                fileList.innerHTML =
                  '<li class="file-list-item"><a>Keine Einträge</a></li>';
              } else {
                files.forEach(function (file) {
                  const listItem = document.createElement("li");
                  listItem.className = "file-list-item";
                  const fileLink = document.createElement("a");
                  fileLink.href =
                    "/static/certificates/" + category + "/" + file;
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

    navRight.addEventListener("mouseout", function (event) {
      const link = event.target.closest(".file-list-item a");
      if (link) {
        globalTooltip.style.display = "none";
      }

      if (!navRight.contains(event.relatedTarget)) {
        if (previewContent) {
          previewContent.innerHTML = initialContent;
        }
        globalTooltip.style.display = "none";
      }
    });
  }

  // Tooltip-Position mit Maus mitführen
  document.addEventListener("mousemove", function (event) {
    if (globalTooltip.style.display === "block") {
      globalTooltip.style.left = event.clientX + 15 + "px";
      globalTooltip.style.top = event.clientY + "px";
    }
  });

  // -----------------------------------------------------
  // BALLOON-LOGIK: mehrere konfigurierbare Ballons
  // -----------------------------------------------------

  const BALLOON_CONFIGS = [
    {
      id: "cpmai",
      xPercent: 48,
      riseDurationSeconds: 18,
      scaleStart: 0.55,
      scaleEnd: 3.2,
      theme: "cpmai", // verwendet das Standard-Gradient-Theme
      delayMs: 0,
      // kein auto-close: Dialog bleibt, bis "Schließen" geklickt wird
      text: {
        de: {
          title: "CPMAI in der Praxis",
          body: "Wenn wir KI- oder Automationsprojekte mit CPMAI strukturieren, landen weniger Ideen auf dem Proof-of-Concept-Friedhof – und mehr Lösungen erzeugen echte Wertschöpfung im Betrieb.",
        },
        en: {
          title: "CPMAI in Practice",
          body: "When we structure AI and automation projects with CPMAI, fewer ideas end up on the proof-of-concept graveyard – and more solutions go live and create real business value.",
        },
      },
    },
    {
      id: "explore",
      xPercent: 36,
      riseDurationSeconds: 20,
      scaleStart: 0.5,
      scaleEnd: 3.4,
      theme: "secondary", // nutzt das alternative Theme aus CSS
      delayMs: 3500,
      // Beispiel: Dialog nach 15s automatisch schließen (optional)
      // dismissAfterMs: 15000,
      text: {
        de: {
          title: "Was ist Ihr nächster Schritt?",
          body: "Zukünftig können wir auch über das Client-Portal Ihr Anliegen gemäß Ihren Bedürfnissen skizzieren – von der Diagnose bis zur Umsetzung. So wird aus vagen Ideen ein adaptiver Fahrplan.",
        },
        en: {
          title: "What’s your next step?",
          body: "In future, we can also use the client portal to sketch your request around your specific needs – from diagnosis through to implementation. This way, vague ideas turn into an adaptive roadmap.",
        },
      },
    },
    {
      id: "next-step-right",
      xPercent: 60, // rechts von der Mitte
      riseDurationSeconds: 19,
      scaleStart: 0.5,
      scaleEnd: 3.2,
      theme: "gray",
      delayMs: 7000,
      // optional: Dialog nach X ms automatisch schließen
      // dismissAfterMs: 12000,
      text: {
        de: {
          title: "Ein PMO, das den Laden zusammenhält",
          body: "Integration von strategischer Vision, taktischer Umsetzung und operativer Exzellenz: Das PMI-OPM-Modell und die PMI-PMOCP-Zertifizierung – ein duales Framework für den Erfolg von PMOs, das messbare Ergebnisse liefert, die organisatorische Agilität stärkt und den langfristigen Wert von Produkten, Portfolios, Programmen und Projekten maximiert.",
        },
        en: {
          title: "A PMO That Holds Things Together",
          body: "Integrating Strategic Vision, Tactical Execution, and Operational Excellence: The PMI OPM Model and PMI-PMOCP Certification—A Dual Framework for PMO Success that drives measurable results, enhances organizational agility, and maximizes the long-term value of products, portfolios, programs, and projects.",
        },
      },
    },
  ];

  function spawnBalloon(config, lang) {
    const layer = document.getElementById("balloon-layer");
    if (!layer) return;

    // --- Ballon-Button ---
    const balloon = document.createElement("button");
    balloon.type = "button";
    balloon.className = "balloon";
    balloon.setAttribute("data-balloon-id", config.id);

    const riseSeconds =
      typeof config.riseDurationSeconds === "number"
        ? config.riseDurationSeconds
        : 18;
    balloon.style.setProperty(
      "--balloon-rise-duration",
      riseSeconds.toString() + "s"
    );

    if (typeof config.xPercent === "number") {
      balloon.style.setProperty("--balloon-x", config.xPercent + "%");
    }
    if (typeof config.scaleStart === "number") {
      balloon.style.setProperty(
        "--balloon-scale-start",
        config.scaleStart.toString()
      );
    }
    if (typeof config.scaleEnd === "number") {
      balloon.style.setProperty(
        "--balloon-scale-end",
        config.scaleEnd.toString()
      );
    }
    if (config.theme) {
      balloon.classList.add("balloon--theme-" + config.theme);
    }

    const inner = document.createElement("span");
    inner.className = "balloon__inner";
    const string = document.createElement("span");
    string.className = "balloon__string";

    balloon.appendChild(inner);
    balloon.appendChild(string);
    layer.appendChild(balloon);

    // --- Dialog zum Ballon ---
    const dialog = document.createElement("div");
    dialog.className = "balloon-message";
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-hidden", "true");

    const content = document.createElement("div");
    content.className = "balloon-message__content";

    let textByLang = null;
    if (config.text) {
      if (lang === "de" && config.text.de) textByLang = config.text.de;
      else if (lang === "en" && config.text.en) textByLang = config.text.en;
      else if (config.text.de) textByLang = config.text.de;
      else if (config.text.en) textByLang = config.text.en;
    }
    if (!textByLang) {
      textByLang = { title: "", body: "" };
    }

    const title = textByLang.title || "";
    const body = textByLang.body || "";

    content.innerHTML =
      "<h2>" +
      title +
      "</h2>" +
      "<p>" +
      body +
      "</p>" +
      '<button type="button" class="balloon-message__close">' +
      (lang === "de" ? "Schließen" : "Close") +
      "</button>";

    dialog.appendChild(content);
    layer.appendChild(dialog);

    // --- Zustand & Hilfsfunktionen ---
    let clicked = false;
    let popped = false;
    let dialogRemoved = false;
    let autoCloseTimer = null;

    function showMessage() {
      dialog.classList.add("is-visible");
      dialog.setAttribute("aria-hidden", "false");
    }

    function hideMessage() {
      dialog.classList.remove("is-visible");
      dialog.setAttribute("aria-hidden", "true");
    }

    function removeBalloon() {
      balloon.classList.add("balloon--hidden");
      setTimeout(function () {
        balloon.remove();
      }, 400);
    }

    function removeDialog() {
      if (dialogRemoved) return;
      dialogRemoved = true;
      if (autoCloseTimer !== null) {
        clearTimeout(autoCloseTimer);
      }
      hideMessage();
      setTimeout(function () {
        dialog.remove();
      }, 250);
    }

    function popBalloon(withMessage) {
      if (popped) return;
      popped = true;
      balloon.classList.add("balloon--popped");

      if (withMessage) {
        // Klick: Dialog anzeigen, Ballon/Faden weg
        showMessage();
        setTimeout(removeBalloon, 350);

        if (typeof config.dismissAfterMs === "number") {
          autoCloseTimer = window.setTimeout(function () {
            removeDialog();
          }, config.dismissAfterMs);
        }
      } else {
        // Kein Klick: leises Platzen ohne Dialog
        setTimeout(function () {
          removeBalloon();
          dialog.remove();
        }, 350);
      }
    }

    // --- Event-Handler ---

    // Klick auf Ballon -> Dialog öffnen
    balloon.addEventListener("click", function (ev) {
      ev.stopPropagation();
      clicked = true;
      popBalloon(true);
    });

    // Ende der Aufstiegsanimation -> ggf. leises Platzen
    balloon.addEventListener("animationend", function () {
      if (!clicked) {
        popBalloon(false);
      }
    });

    // "Schließen"-Button im Dialog
    const closeBtn = content.querySelector(".balloon-message__close");
    if (closeBtn) {
      closeBtn.addEventListener("click", function () {
        removeDialog();
      });
    }

    // Klick auf den halbtransparenten Hintergrund
    dialog.addEventListener("click", function (ev) {
      if (ev.target === dialog) {
        removeDialog();
      }
    });
  }

  function initBalloons() {
    const layer = document.getElementById("balloon-layer");
    if (!layer || !BALLOON_CONFIGS || BALLOON_CONFIGS.length === 0) return;

    BALLOON_CONFIGS.forEach(function (config, index) {
      const delay =
        typeof config.delayMs === "number" ? config.delayMs : index * 2500;
      window.setTimeout(function () {
        spawnBalloon(config, CURRENT_LANG);
      }, delay);
    });
  }

  // Ballons initial starten
  initBalloons();
});

// ---------------------------------------------------------
// CTA unter Profilbild + NEWS-TICKER
// ---------------------------------------------------------
(function () {
  const preview = document.getElementById("preview-content");
  const cta = document.getElementById("ctaUnderProfile");
  if (!preview || !cta) return;

  function profileVisible() {
    return !!preview.querySelector(".profile-figure");
  }

  function updateCTA() {
    const show = profileVisible();
    cta.classList.toggle("is-hidden", !show);
  }

  // 1) Beim ersten Laden
  updateCTA();

  // 2) Auf DOM-Wechsel im Preview reagieren
  const mo = new MutationObserver(updateCTA);
  mo.observe(preview, { childList: true, subtree: true });

  // 3) Klicks in den Navs triggern ebenfalls ein Update
  const navLeft = document.querySelector(".nav-left");
  const navRight = document.querySelector(".nav-right");
  [navLeft, navRight].forEach(function (el) {
    if (!el) return;
    el.addEventListener("click", function () {
      setTimeout(updateCTA, 50);
    });
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

    const firstWidth = firstItem.getBoundingClientRect().width;

    const styles = getComputedStyle(track);
    const gapValue =
      styles.getPropertyValue("gap") || styles.getPropertyValue("column-gap");
    const gap = parseFloat(gapValue) || 48;

    const distance = firstWidth + gap;
    track.style.setProperty("--ticker-distance", distance + "px");

    const pxPerSecond = 80;
    const duration = distance / pxPerSecond;
    track.style.animationDuration = duration + "s";
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNewsTicker();
    window.addEventListener("resize", function () {
      initNewsTicker();
    });
  });
})();
