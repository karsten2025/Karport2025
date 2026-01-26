// Torus Launcher: Rollende "Symbiotic Value Engine"
(function() {
  'use strict';
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTorusLauncher);
  } else {
    initTorusLauncher();
  }
  
  function initTorusLauncher() {
    const torusLauncher = document.getElementById("torus-launcher");
    const chatWindow = document.getElementById("kz-chat-window");

    if (!torusLauncher || !chatWindow) return;

    function startRollingAnimation() {
      const viewportWidth = window.innerWidth;
      const startX = -(viewportWidth + 200);
      const endX = 0;
      const distance = Math.abs(endX - startX);
      const radius = 35;
      const circumference = 2 * Math.PI * radius;
      const fullRotations = distance / circumference;
      const roundedRotations = Math.round(fullRotations);
      const totalRotationDegrees = roundedRotations * 360;
      const duration = 2800;
      
      torusLauncher.classList.add("rolling");
      const startTime = performance.now();
      
      function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const rawProgress = Math.min(elapsed / duration, 1);
        const t = rawProgress;
        const easeProgress = 1 - Math.pow(1 - t, 3.5);
        const currentX = startX + (endX - startX) * easeProgress;
        const currentRotation = totalRotationDegrees * easeProgress;
        
        torusLauncher.style.transform = 
          `translateX(${currentX}px) rotate(${currentRotation}deg)`;
        
        if (rawProgress < 1) {
          requestAnimationFrame(animate);
        } else {
          torusLauncher.classList.remove("rolling");
          torusLauncher.classList.add("arrived");
          torusLauncher.style.transform = "translateX(0) rotate(0deg)";
        }
      }
      
      requestAnimationFrame(animate);
    }
    
    torusLauncher.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      chatWindow.classList.toggle("kz-active");
      
      if (chatWindow.classList.contains("kz-active")) {
        const chatInput = document.getElementById("kz-chat-input");
        if (chatInput) setTimeout(() => chatInput.focus(), 350);
      }
      
      torusLauncher.style.transition = "transform 0.15s ease";
      torusLauncher.style.transform = "translateX(0) rotate(0deg) scale(0.92)";
      
      setTimeout(() => {
        torusLauncher.style.transition = "transform 0.3s cubic-bezier(0.22, 1, 0.36, 1)";
        torusLauncher.style.transform = "translateX(0) rotate(0deg) scale(1)";
      }, 150);
    });
    
    setTimeout(() => startRollingAnimation(), 1000);
    
    let resizeTimeout;
    window.addEventListener("resize", function() {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        if (torusLauncher.classList.contains("arrived")) {
          torusLauncher.style.transform = "translateX(0) rotate(0deg)";
        }
      }, 250);
    });
  }
})();
