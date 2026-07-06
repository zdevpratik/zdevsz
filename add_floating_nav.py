import glob
import re

css_code = r'''
    /* ────────────────────────────────────────
       FLOATING MOBILE NAV
       ──────────────────────────────────────── */
    @media (min-width: 901px) {
      .floating-nav-wrapper { display: none; }
    }
    @media (max-width: 900px) {
      .floating-nav-wrapper {
        position: fixed;
        bottom: 32px;
        right: 24px;
        z-index: 999999;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 16px;
      }
      .floating-nav-menu {
        background: rgba(15, 15, 15, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px 28px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        opacity: 0;
        pointer-events: none;
        transform: translateY(20px) scale(0.95);
        transition: all 0.4s var(--ease-expo);
        transform-origin: bottom right;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
      }
      .floating-nav-menu.active {
        opacity: 1;
        pointer-events: auto;
        transform: translateY(0) scale(1);
      }
      .floating-nav-menu a {
        color: var(--ash);
        font-family: var(--font);
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        transition: color 0.2s ease;
        text-align: right;
      }
      .floating-nav-menu a:hover,
      .floating-nav-menu a:active {
        color: #3df59a;
      }
      .floating-nav-btn {
        background: #3df59a;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 5px;
        cursor: pointer;
        box-shadow: 0 8px 32px rgba(61, 245, 154, 0.3);
        transition: transform 0.3s var(--ease-expo), background 0.3s;
        -webkit-tap-highlight-color: transparent;
      }
      .floating-nav-btn:active {
        transform: scale(0.92);
        background: #2ce088;
      }
      .floating-nav-btn .f-bar {
        width: 24px;
        height: 2px;
        background: #080808;
        border-radius: 2px;
        transition: all 0.3s ease;
      }
      .floating-nav-btn.active .f-bar:nth-child(1) { transform: translateY(7px) rotate(45deg); }
      .floating-nav-btn.active .f-bar:nth-child(2) { opacity: 0; }
      .floating-nav-btn.active .f-bar:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
    }
'''

html_code = r'''
  <!-- FLOATING MOBILE NAV -->
  <div class="floating-nav-wrapper">
    <div class="floating-nav-menu" id="floatingNavMenu">
      <a href="index.html" data-scroll="top">HOME</a>
      <a href="index.html#we-are" data-scroll="we-are">WHO ARE WE</a>
      <a href="services.html">SERVICES</a>
      <a href="pricing.html">PRICING</a>
      <a href="contact.html">CONTACT</a>
    </div>
    <button class="floating-nav-btn" id="floatingNavBtn" aria-label="Open Menu">
      <span class="f-bar"></span>
      <span class="f-bar"></span>
      <span class="f-bar"></span>
    </button>
  </div>
'''

js_code = r'''
    /* ══════════════════════════════════════
       FLOATING NAV LOGIC
       ══════════════════════════════════════ */
    const floatingBtn = document.getElementById('floatingNavBtn');
    const floatingMenu = document.getElementById('floatingNavMenu');
    if (floatingBtn && floatingMenu) {
      floatingBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        floatingBtn.classList.toggle('active');
        floatingMenu.classList.toggle('active');
      });
      
      document.addEventListener('click', (e) => {
        if (!floatingMenu.contains(e.target) && !floatingBtn.contains(e.target)) {
          floatingBtn.classList.remove('active');
          floatingMenu.classList.remove('active');
        }
      });

      floatingMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          floatingBtn.classList.remove('active');
          floatingMenu.classList.remove('active');
        });
      });
    }
'''

for f in glob.glob('*.html'):
    content = open(f, encoding='utf-8').read()
    
    # Inject CSS before closing </style>
    if 'FLOATING MOBILE NAV' not in content:
        content = content.replace('</style>', css_code + '\n  </style>')
        
        # Inject HTML before first <script>
        # find the first <script
        idx = content.find('<script')
        if idx != -1:
            content = content[:idx] + html_code + '\n  ' + content[idx:]
            
        # Inject JS before closing </body>
        idx2 = content.rfind('</body>')
        if idx2 != -1:
            content = content[:idx2] + js_code + '\n' + content[idx2:]
            
        with open(f, 'w', encoding='utf-8') as out:
            out.write(content)
        print(f"Added floating nav to {f}")
    else:
        print(f"Already added to {f}")
