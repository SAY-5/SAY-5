// Renders README.md roughly the way GitHub does (dark and light), for a visual check.
import fs from 'node:fs';
const md = fs.readFileSync('README.md', 'utf8');
const html = md
  .replace(/^## (.*)$/gm, '<h2>$1</h2>')
  .replace(/^(?!<)(.+)$/gm, (l) => (l.trim() && !l.startsWith('<') ? `<p>${l}</p>` : l))
  .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
  .replace(/src="assets\//g, 'src="../assets/');
for (const [theme, bg, fg] of [['dark', '#0d1117', '#e6edf3'], ['light', '#ffffff', '#1f2328']]) {
  fs.writeFileSync(`scripts/preview-${theme}.html`, `<!doctype html><html><head><meta charset="utf-8"><style>
  body{margin:0;background:${bg};color:${fg};font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
  .wrap{max-width:896px;margin:24px auto;padding:32px;border:1px solid ${theme==='dark'?'#30363d':'#d0d7de'};border-radius:8px}
  h2{font-size:1.5em;border-bottom:1px solid ${theme==='dark'?'#30363d':'#d8dee4'};padding-bottom:.3em;margin-top:24px}
  a{color:${theme==='dark'?'#4493f8':'#0969da'};text-decoration:none} img{max-width:100%;vertical-align:middle} sub{opacity:.7}
  </style></head><body><div class="wrap">${html}</div></body></html>`);
}
console.log('previews written');
