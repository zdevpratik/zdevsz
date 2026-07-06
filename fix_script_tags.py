import glob
import re

for f in glob.glob('*.html'):
    content = open(f, encoding='utf-8').read()
    
    # We injected:
    #     /* ══════════════════════════════════════
    #        FLOATING NAV LOGIC
    
    # Let's wrap it in <script> tags if it's currently outside
    
    js_text = r'''
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

    if js_text in content and '<script>' + js_text not in content and '<script type="text/javascript">' + js_text not in content:
        # It's currently plain text
        content = content.replace(js_text, '\n<script>\n' + js_text + '\n</script>\n')
        with open(f, 'w', encoding='utf-8') as out:
            out.write(content)
        print(f"Fixed {f}")
