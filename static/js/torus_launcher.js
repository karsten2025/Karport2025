// ============================================================
// 🌀 TORUS LAUNCHER: Die rollende "Symbiotic Value Engine"
// Hochwertige Roll-Animation mit perfekter Rotation & Glow
// ============================================================

(function() {
  'use strict';
  
  // Warte auf DOM-Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTorusLauncher);
  } else {
    initTorusLauncher();
  }
  
  function initTorusLauncher() {
    const torusLauncher = document.getElementById("torus-launcher");
    const chatTrigger = document.getElementById("kz-chat-trigger");
    const chatWindow = document.getElementById("kz-chat-window");

    if (!torusLauncher || !chatWindow) {
      console.warn("⚠️ Torus Launcher: Erforderliche Elemente nicht gefunden");
      return;
    }
    
    console.log("🌀 Torus Launcher initialized!");

    // ============================================================
    // 1. ROLL-ANIMATION: Von links nach rechts mit Ease-Out
    // ============================================================
    
    function startRollingAnimation() {
      console.log("🚀 Starting Torus Roll Animation (LEFT → RIGHT)...");
      
      // Viewport-Breite
      const viewportWidth = window.innerWidth;
      
      // Start-Position: LINKS außerhalb des Bildschirms (wie im CSS)
      const startX = -(viewportWidth + 200);
      
      // End-Position: 0 (normale Position = bottom: 30px, right: 30px)
      const endX = 0;
      
      // Roll-Distanz
      const distance = Math.abs(endX - startX);
      
      // Torus-Radius (halbe Breite = 35px)
      const radius = 35;
      
      // Berechne Rotationen: Eine volle Rolle = Umfang (2πr)
      const circumference = 2 * Math.PI * radius;
      const fullRotations = distance / circumference;
      
      // WICHTIG: Runde auf volle 360°-Vielfache für perfekte Endposition
      const roundedRotations = Math.round(fullRotations);
      const totalRotationDegrees = roundedRotations * 360;
      
      console.log(`📊 Distance: ${distance.toFixed(0)}px`);
      console.log(`🔄 Rotations: ${fullRotations.toFixed(2)} → rounded to ${roundedRotations}`);
      console.log(`🎯 Total Rotation: ${totalRotationDegrees}°`);
      
      // Animation-Dauer (2.8 Sekunden für smooth Roll)
      const duration = 2800; // ms
      
      // CSS hat bereits Start-Position gesetzt, wir starten direkt
      torusLauncher.classList.add("rolling");
      
      // ============================================================
      // 2. ANIMATION MIT EASING: Cubic-Bezier für sanftes Bremsen
      // ============================================================
      
      const startTime = performance.now();
      
      function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const rawProgress = Math.min(elapsed / duration, 1);
        
        // Easing: cubic-bezier(0.22, 1, 0.36, 1) = Smooth Ease-Out
        // Die letzten 20% werden extrem sanft abgebremst
        const t = rawProgress;
        const easeProgress = 1 - Math.pow(1 - t, 3.5); // Sanftes Gleiten
        
        // Berechne aktuelle Position (von links nach rechts)
        const currentX = startX + (endX - startX) * easeProgress;
        
        // Berechne aktuelle Rotation (synchron zur Bewegung)
        const currentRotation = totalRotationDegrees * easeProgress;
        
        // Wende Transformation an
        torusLauncher.style.transform = 
          `translateX(${currentX}px) rotate(${currentRotation}deg)`;
        
        // Weiter animieren oder stoppen
        if (rawProgress < 1) {
          requestAnimationFrame(animate);
        } else {
          // ============================================================
          // 3. ANIMATION BEENDET: Finales Gleiten & Glow aktivieren
          // ============================================================
          console.log("✅ Torus arrived at position!");
          
          torusLauncher.classList.remove("rolling");
          torusLauncher.classList.add("arrived");
          
          // Finale Position: Perfekt bei 0° (Text waagerecht oben)
          torusLauncher.style.transform = "translateX(0) rotate(0deg)";
        }
      }
      
      requestAnimationFrame(animate);
    }
    
    // ============================================================
    // 4. CLICK-HANDLER: Öffnet/Schließt Chat-Fenster
    // ============================================================
    
    torusLauncher.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      console.log("🌀 Torus clicked - toggling chat!");
      
      // Toggle Chat-Window
      chatWindow.classList.toggle("kz-active");
      
      // Fokussiere Input-Feld beim Öffnen
      if (chatWindow.classList.contains("kz-active")) {
        const chatInput = document.getElementById("kz-chat-input");
        if (chatInput) {
          setTimeout(() => chatInput.focus(), 350);
        }
      }
      
      // Visuelles Feedback: Kurzer Scale-Down
      torusLauncher.style.transition = "transform 0.15s ease";
      torusLauncher.style.transform = 
        "translateX(0) rotate(0deg) scale(0.92)";
      
      setTimeout(() => {
        torusLauncher.style.transition = 
          "transform 0.3s cubic-bezier(0.22, 1, 0.36, 1)";
        torusLauncher.style.transform = 
          "translateX(0) rotate(0deg) scale(1)";
      }, 150);
    });
    
    // ============================================================
    // 5. START: Animation nach Page-Load-Delay
    // ============================================================
    
    setTimeout(() => {
      startRollingAnimation();
    }, 1000); // 1 Sekunde Verzögerung für smooth Page-Load
    
    // ============================================================
    // 6. RESPONSIVE: Re-Position bei Window-Resize
    // ============================================================
    
    let resizeTimeout;
    window.addEventListener("resize", function() {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        // Bei Resize: Torus bleibt an Zielposition
        if (torusLauncher.classList.contains("arrived")) {
          torusLauncher.style.transform = "translateX(0) rotate(0deg)";
        }
      }, 250);
    });
    
    console.log("✨ Torus Launcher ready - waiting for animation start...");
  }
})();
