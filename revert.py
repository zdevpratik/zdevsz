import glob
import re
import os

css_old = r'''.mobile-menu-toggle {
        display: flex !important; flex-direction: column; gap: 4px;
        background: none; border: none; cursor: pointer; padding: 4px;
        position: relative; z-index: 200;
      }
      .mobile-menu-toggle .bar {
        width: 20px; height: 2px; background: var(--bone); transition: 0.3s;
      }
      .mobile-menu-toggle.active .bar:nth-child(1) { transform: translateY(6px) rotate(45deg); }
      .mobile-menu-toggle.active .bar:nth-child(2) { opacity: 0; }
      .mobile-menu-toggle.active .bar:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }
      .nav-links { display: none !important; }
      .mobile-menu-overlay {
        display: none; flex-direction: column; width: 100%;
        position: fixed; top: 64px; left: 0; right: 0; bottom: 0;
        background: rgba(8,8,8,0.98); padding: 40px 20px;
        align-items: center; text-align: center; justify-content: flex-start; gap: 32px;
        z-index: 9999999; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
      }
      .mobile-menu-overlay.active { display: flex !important; }
      .mobile-menu-overlay a {
        font-family: var(--font); font-weight: 400; font-size: 24px !important;
        letter-spacing: .08em; text-transform: uppercase; color: var(--ash);
        text-decoration: none; transition: color .2s ease;
      }
      .mobile-menu-overlay a:hover { color: var(--bone); }'''

css_new = r'''.mobile-menu-toggle {
        display: flex; flex-direction: column; gap: 4px;
        background: none; border: none; cursor: pointer; padding: 4px;
        position: relative; z-index: 200;
      }
      .mobile-menu-toggle .bar {
        width: 20px; height: 2px; background: var(--bone); transition: 0.3s;
      }
      .mobile-menu-toggle.active .bar:nth-child(1) { transform: translateY(6px) rotate(45deg); }
      .mobile-menu-toggle.active .bar:nth-child(2) { opacity: 0; }
      .mobile-menu-toggle.active .bar:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }
      .nav-links {
        display: none; flex-direction: column; width: 100%; margin-top: 16px; gap: 12px;
        background: var(--void); padding: 16px; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px;
        align-items: flex-start; text-align: left;
      }
      .nav-links.active { display: flex; }
      .nav-links a { font-size: 14px; }'''

js_old = r'''const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.getElementById('navLinks');
    if (mobileMenuToggle && navLinks) {
      const overlay = document.createElement('div');
      overlay.className = 'mobile-menu-overlay';
      overlay.innerHTML = navLinks.innerHTML;
      document.body.appendChild(overlay);
      
      mobileMenuToggle.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        mobileMenuToggle.classList.toggle('active');
        overlay.classList.toggle('active');
      });
      overlay.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          mobileMenuToggle.classList.remove('active');
          overlay.classList.remove('active');
        });
      });
    }'''

js_new = r'''const mobileMenuToggle = document.getElementById('mobileMenuToggle');
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
    }'''

for f in glob.glob('*.html'):
    content = open(f, encoding='utf-8').read()
    
    # 1. Replace the CSS block
    content = content.replace(css_old, css_new)
    
    # 2. Replace the JS block
    content = content.replace(js_old, js_new)
    
    # 3. Remove .mobile-menu-overlay global CSS
    content = re.sub(r'\s*\.mobile-menu-overlay\s*\{\s*display:\s*none;\s*\}', '', content)
    
    # 4. Remove .mobile-menu-toggle { display: none; } if duplicated at end of file (from buggy task 1078)
    content = content.replace('.mobile-menu-toggle { display: flex !important; } </style>', '</style>')
    
    # 5. Fix index.html specific global listener
    content = content.replace("const overlay = document.querySelector('.mobile-menu-overlay');\n          if (overlay) overlay.classList.remove('active');", "const nl = document.getElementById('navLinks');\n          if (nl) nl.classList.remove('active');")
    
    with open(f, 'w', encoding='utf-8') as out:
        out.write(content)
        
    print(f"Updated {f}")
