import glob
import re

css_old = r'''      .floating-nav-wrapper {
        position: fixed;
        top: 24px;
        right: 20px;
        z-index: 999999;
        display: flex;
        flex-direction: column-reverse;
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
        transform: translateY(-20px) scale(0.95);
        transition: all 0.4s var(--ease-expo);
        transform-origin: top right;
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
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
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
        width: 20px;
        height: 2px;
        background: #080808;
        border-radius: 2px;
        transition: all 0.3s ease;
      }
      .floating-nav-btn.active .f-bar:nth-child(1) { transform: translateY(6px) rotate(45deg); }
      .floating-nav-btn.active .f-bar:nth-child(2) { opacity: 0; }
      .floating-nav-btn.active .f-bar:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }'''

css_new = r'''      .floating-nav-wrapper {
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
        width: 44px;
        height: 44px;
        border-radius: 50%;
        border: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
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
        width: 18px;
        height: 2px;
        background: #080808;
        border-radius: 2px;
        transition: all 0.3s ease;
      }
      .floating-nav-btn.active .f-bar:nth-child(1) { transform: translateY(6px) rotate(45deg); }
      .floating-nav-btn.active .f-bar:nth-child(2) { opacity: 0; }
      .floating-nav-btn.active .f-bar:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }'''

for f in glob.glob('*.html'):
    content = open(f, encoding='utf-8').read()
    if css_old in content:
        content = content.replace(css_old, css_new)
        with open(f, 'w', encoding='utf-8') as out:
            out.write(content)
        print(f"Updated {f}")
    else:
        print(f"Could not find exact match in {f}")
