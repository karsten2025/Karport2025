// Header Hologram: Profilbild → Torus (Option B: Delayed Init)
(function() {
  'use strict';
  
  function initHologram() {
    const profileImg = document.getElementById('hologram-profile');
    const torusImg = document.getElementById('hologram-torus');
    
    if (!profileImg || !torusImg) return;
    
    function startSequence() {
      setTimeout(() => {
        profileImg.classList.add('fade-out');
        torusImg.classList.add('morph-in');
        
        setTimeout(() => {
          torusImg.classList.add('settled');
          setTimeout(() => profileImg.style.display = 'none', 1200);
        }, 2000);
      }, 1000);
    }
    
    startSequence();
  }
  
  // CRITICAL: Start erst nach window.onload (Page ist komplett fertig)
  if (document.readyState === 'complete') {
    setTimeout(() => initHologram(), 500);
  } else {
    window.addEventListener('load', function() {
      setTimeout(() => initHologram(), 500);
    });
  }
})();
