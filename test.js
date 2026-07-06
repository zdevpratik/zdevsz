
    /* ══════════════════════════════════════
       UNIQUE CANVAS BACKGROUND (PARTICLE NETWORK)
       ══════════════════════════════════════ */
    const canvas = document.getElementById('hero-canvas');
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    let numParticles = 120;
    let connectionDistance = 160;
    
    // Mouse tracking for interactivity
    let mouse = { x: -1000, y: -1000, radius: 180 };

    function initCanvas() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      
      // Balance chaos and coverage on mobile screens
      let speedMult = 2.0;
      if (width < 768) {
        numParticles = 90;
        connectionDistance = 125;
        speedMult = 1.0; // A little faster
      } else {
        numParticles = 140;
        connectionDistance = 160;
      }

      particles = [];
      for (let i = 0; i < numParticles; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * speedMult,
          vy: (Math.random() - 0.5) * speedMult,
          size: Math.random() * 2 + 0.5,
          color: Math.random() > 0.8 ? '#3df59a' : '#d4d2d2' // Mix of logo color and ash/bone
        });
      }
    }

    function drawNetwork() {
      ctx.clearRect(0, 0, width, height);
      
      // Update and draw particles
      for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        
        // Bounce off edges
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;
        
        // Interactive mouse repulsion
        let dx = p.x - mouse.x;
        let dy = p.y - mouse.y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < mouse.radius) {
          let force = (mouse.radius - distance) / mouse.radius;
          p.x += (dx / distance) * force * 5;
          p.y += (dy / distance) * force * 5;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
        
        // Draw connections
        for (let j = i + 1; j < particles.length; j++) {
          let p2 = particles[j];
          let dx2 = p.x - p2.x;
          let dy2 = p.y - p2.y;
          let dist2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
          
          if (dist2 < connectionDistance) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            let opacity = 1 - (dist2 / connectionDistance);
            ctx.strokeStyle = p.color === '#3df59a' || p2.color === '#3df59a' 
              ? `rgba(61, 245, 154, ${opacity * 0.85})` 
              : `rgba(212, 210, 210, ${opacity * 0.45})`;
            ctx.lineWidth = 1.5;
            ctx.stroke();
          }
        }
      }
      
      requestAnimationFrame(drawNetwork);
    }

    initCanvas();
    drawNetwork();
    
    window.addEventListener('resize', initCanvas);
    document.addEventListener('mousemove', (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });
    document.addEventListener('mouseleave', () => {
      mouse.x = -1000;
      mouse.y = -1000;
    });


    /* ══════════════════════════════════════
       CURSOR
       ══════════════════════════════════════ */
    const cursor = document.getElementById('cursor');
    let mx = -100, my = -100, cx = -100, cy = -100;

    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });

    (function animateCursor() {
      cx += (mx - cx) * 0.18;
      cy += (my - cy) * 0.18;
      cursor.style.left = cx + 'px';
      cursor.style.top  = cy + 'px';
      requestAnimationFrame(animateCursor);
    })();

    document.querySelectorAll('a, button').forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('hovered'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('hovered'));
    });




    document.querySelectorAll('.nav-links a').forEach(link => {
      const original = link.getAttribute('data-original');

      /* Smooth scroll using modern scrollIntoView */
      const target = link.getAttribute('data-scroll');
      if (target) {
        link.addEventListener('click', e => {
          e.preventDefault();
          if (target === 'top') {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          } else {
            const el = document.getElementById(target);
            if (el) {
              el.scrollIntoView({ behavior: 'smooth' });
            }
          }
        });
      }
    });

    /* Handle cross-page anchor links (e.g. from services.html) */
    window.addEventListener('load', () => {
      setTimeout(() => {
        if (window.location.hash === '#manifesto') {
          const el = document.getElementById('manifesto');
          if (el) {
            const range = el.offsetHeight - window.innerHeight;
            window.scrollTo({ top: el.offsetTop + range * 0.12, behavior: 'smooth' });
          }
        }
      }, 50);
    });


    /* ══════════════════════════════════════
       CHARACTER SPLIT
       Wrap every letter in .hl-caps / .hl-serif into its own
       .hl-char span so the ball tracker can highlight individual
       characters — exactly like the SVZ reference.
       Must run before entrance animations so the spans exist.
       ══════════════════════════════════════ */
    document.querySelectorAll('.hl-caps, .hl-serif').forEach(el => {
      /* Preserve the parent class (hl-caps / hl-serif) for font styling;
         replace its text content with a series of single-char spans. */
      el.innerHTML = [...el.textContent].map(ch =>
        `<span class="hl-char">${ch === ' ' ? ' ' : ch}</span>`
      ).join('');
    });


    /* ══════════════════════════════════════
       ENTRANCE ANIMATIONS
       Staggered fade-up on page load
       ══════════════════════════════════════ */
    [
      { id: 'heroLabel',  delay: 50 },
      { id: 'row1',       delay: 150 },
      { id: 'row2',       delay: 250 },
      { id: 'row3',       delay: 350 },
      { id: 'heroEnter',  delay: 450 },
    ].forEach(({ id, delay }) => {
      const el = document.getElementById(id);
      if (el) setTimeout(() => el.classList.add('visible'), delay);
    });


    /* ══════════════════════════════════════
       NAV — subtle dark fill on scroll
       ══════════════════════════════════════ */
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY > 40;
      navbar.style.background    = scrolled ? 'rgba(8,8,8,0.85)' : 'transparent';
      navbar.style.backdropFilter= scrolled ? 'blur(12px)' : 'none';
      navbar.style.borderBottom  = scrolled ? '1px solid rgba(255,255,255,0.06)' : 'none';
    }, { passive: true });

    /* ══════════════════════════════════════
       3D SCROLL SNAP ANIMATIONS
       ══════════════════════════════════════ */
    (function () {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
          } else {
            // Re-hide when scrolled away so it animates again
            entry.target.classList.remove('is-visible'); 
          }
        });
      }, { threshold: 0.3 });

      const weSection = document.getElementById('we-are');
      const manifesto = document.getElementById('manifesto');
      const closing = document.getElementById('closing');
      
      if (weSection) observer.observe(weSection);
      if (manifesto) observer.observe(manifesto);
      if (closing) observer.observe(closing);
    })();

    /* ══════════════════════════════════════
       MOBILE MENU TOGGLE
       ══════════════════════════════════════ */
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.getElementById('navLinks');
    if (mobileMenuToggle && navLinks) {
      mobileMenuToggle.addEventListener('click', () => {
        mobileMenuToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
      });
      navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          mobileMenuToggle.classList.remove('active');
          navLinks.classList.remove('active');
        });
      });
    }



    