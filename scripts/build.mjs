// Builds the SVG assets and README for the profile from the portfolio's project
// data. Run with Node 22+ (type stripping is used to import projects.ts).
//
//   node scripts/build.mjs            # full build
//   GITHUB_TOKEN=... node scripts/build.mjs   # also refreshes GitHub numbers
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import opentype from 'opentype.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CACHE = path.join(ROOT, 'scripts', '.cache');
const ASSETS = path.join(ROOT, 'assets');
fs.mkdirSync(CACHE, { recursive: true });
fs.mkdirSync(path.join(ASSETS, 'cards'), { recursive: true });

const USER = 'SAY-5';
const SITE = 'https://sayportfolio.vercel.app';
const DEMOS = 'https://showcases-lime.vercel.app';
const PROJECTS_URL = 'https://raw.githubusercontent.com/SAY-5/Portfolio/main/src/data/projects.ts';

// Palette: the same tokens the portfolio uses.
const C = {
  bg: '#0b0c0a',
  bg2: '#0e100d',
  surface: '#121411',
  line: 'rgba(236,246,200,0.10)',
  lineSoft: 'rgba(236,246,200,0.06)',
  paper: '#eef1e4',
  dim: '#a9ae9d',
  faint: '#858b7b',
  lime: '#cdf53a',
  limeDeep: '#9fc41f',
  graphiteTop: '#1e211d',
  graphiteL: '#121412',
  graphiteR: '#0e100e',
  ink: '#10140a',
};

// ---------- fetch helpers ----------
async function fetchText(url) {
  const r = await fetch(url, { headers: { 'user-agent': 'Mozilla/5.0 profile-build' } });
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.text();
}
async function fetchBuffer(url) {
  const r = await fetch(url, { headers: { 'user-agent': 'Mozilla/5.0 profile-build' } });
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return Buffer.from(await r.arrayBuffer());
}
async function cached(name, loader) {
  const p = path.join(CACHE, name);
  if (fs.existsSync(p) && Date.now() - fs.statSync(p).mtimeMs < 6 * 3600 * 1000) return fs.readFileSync(p);
  const buf = await loader();
  fs.writeFileSync(p, buf);
  return buf;
}

// ---------- data ----------
async function loadProjects() {
  const src = await cached('projects.ts', async () => Buffer.from(await fetchText(PROJECTS_URL)));
  const tmp = path.join(CACHE, 'projects.ts');
  fs.writeFileSync(tmp, src);
  const mod = await import(`${tmp}?t=${Date.now()}`);
  return { projects: mod.projects, flagships: mod.flagshipProjects, categories: mod.categories };
}

async function githubNumbers() {
  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  const headers = { 'user-agent': 'profile-build', accept: 'application/vnd.github+json' };
  if (token) headers.authorization = `Bearer ${token}`;
  const cachePath = path.join(ASSETS, 'numbers.json');
  const prev = fs.existsSync(cachePath) ? JSON.parse(fs.readFileSync(cachePath, 'utf8')) : null;
  try {
    const user = await (await fetch(`https://api.github.com/users/${USER}`, { headers })).json();
    const merged = await (await fetch(`https://api.github.com/search/issues?q=is:pr+author:${USER}+is:merged&per_page=1`, { headers })).json();
    const reposMerged = await (await fetch(`https://api.github.com/search/issues?q=is:pr+author:${USER}+is:merged+-user:${USER}&per_page=1`, { headers })).json();
    if (typeof user.public_repos !== 'number' || typeof merged.total_count !== 'number') throw new Error('unexpected api shape');
    const numbers = {
      publicRepos: user.public_repos,
      followers: user.followers,
      mergedPRs: merged.total_count,
      mergedPRsElsewhere: reposMerged.total_count,
      updated: new Date().toISOString().slice(0, 10),
    };
    fs.writeFileSync(cachePath, JSON.stringify(numbers, null, 2) + '\n');
    return numbers;
  } catch (e) {
    if (prev) return prev;
    return { publicRepos: null, followers: null, mergedPRs: null, mergedPRsElsewhere: null, updated: null };
  }
}

// ---------- fonts (outlines, so the SVGs render the same everywhere) ----------
async function loadFonts() {
  const css = await fetchText('https://api.fontshare.com/v2/css?f[]=switzer@400,500,600&display=swap');
  const blocks = css.split('@font-face').slice(1);
  const pick = (weight) => {
    const b = blocks.find((x) => new RegExp(`font-weight:\\s*${weight}`).test(x));
    const m = b && b.match(/url\('?(\/\/[^')]+\.ttf)'?\)/);
    return m ? `https:${m[1]}` : null;
  };
  const urls = { s400: pick(400), s500: pick(500), s600: pick(600) };
  const monoCss = await fetchText('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
  const monoUrl = (monoCss.match(/url\((https:[^)]+\.ttf)\)/) || [])[1];
  const load = async (key, url) => {
    if (!url) return null;
    const buf = await cached(`${key}.ttf`, () => fetchBuffer(url));
    return opentype.parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
  };
  return { s400: await load('switzer-400', urls.s400), s500: await load('switzer-500', urls.s500), s600: await load('switzer-600', urls.s600), mono: await load('jbmono-400', monoUrl) };
}

// Text as a path. Falls back to <text> when a font is missing.
function textPath(font, text, x, y, size, fill, extra = {}) {
  const tracking = extra.tracking || 0; // em units
  if (!font) {
    return `<text x="${x}" y="${y}" font-family="Switzer, Helvetica Neue, Arial, sans-serif" font-size="${size}" fill="${fill}" ${extra.anchor ? `text-anchor="${extra.anchor}"` : ''}>${esc(text)}</text>`;
  }
  let d = '';
  let cx = x;
  const width = measure(font, text, size, tracking);
  if (extra.anchor === 'end') cx = x - width;
  if (extra.anchor === 'middle') cx = x - width / 2;
  const glyphs = font.stringToGlyphs(text);
  const scale = size / font.unitsPerEm;
  for (let i = 0; i < glyphs.length; i++) {
    const g = glyphs[i];
    d += g.getPath(cx, y, size).toPathData(2);
    let adv = g.advanceWidth * scale;
    if (i + 1 < glyphs.length) adv += font.getKerningValue(g, glyphs[i + 1]) * scale;
    cx += adv + tracking * size;
  }
  return `<path d="${d}" fill="${fill}"/>`;
}
function measure(font, text, size, tracking = 0) {
  if (!font) return text.length * size * 0.55;
  return font.getAdvanceWidth(text, size) + tracking * size * Math.max(0, text.length - 1);
}
function wrap(font, text, size, maxWidth, maxLines) {
  const words = text.split(/\s+/);
  const lines = [];
  let cur = '';
  for (const w of words) {
    const t = cur ? `${cur} ${w}` : w;
    if (measure(font, t, size) <= maxWidth || !cur) cur = t;
    else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  if (lines.length > maxLines) {
    const kept = lines.slice(0, maxLines);
    let last = kept[maxLines - 1];
    while (measure(font, `${last}...`, size) > maxWidth && last.includes(' ')) last = last.slice(0, last.lastIndexOf(' '));
    kept[maxLines - 1] = `${last}...`;
    return kept;
  }
  return lines;
}
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// ---------- the slab (same geometry as the site's poster) ----------
function slab(projects, opts) {
  const { x0, y0, unit, lit, animate } = opts;
  const COLS = 17;
  const order = [...projects];
  const cells = order.map((p, i) => ({ col: i % COLS, row: Math.floor(i / COLS), h: 0.3 + (Math.min(9, p.flagshipScore) / 9) * 1.0, lit: p.isFlagship, name: p.name }));
  const CELL = 1, GAP = 0.16, HALF = (CELL - GAP) / 2;
  const U = unit, V = unit * 0.92;
  const proj = (px, pz, h) => [x0 + (px - pz) * U, y0 + (px + pz) * (U / 2) - h * V];
  const ROWS = Math.ceil(cells.length / COLS);
  const ordered = [...cells].sort((a, b) => a.col + a.row - (b.col + b.row));
  let out = '';
  for (const c of ordered) {
    const x = (c.col - (COLS - 1) / 2) * CELL;
    const z = (c.row - (ROWS - 1) / 2) * CELL;
    const aT = proj(x - HALF, z - HALF, c.h), bT = proj(x + HALF, z - HALF, c.h), cT = proj(x + HALF, z + HALF, c.h), dT = proj(x - HALF, z + HALF, c.h);
    const bG = proj(x + HALF, z - HALF, 0), cG = proj(x + HALF, z + HALF, 0), dG = proj(x - HALF, z + HALF, 0);
    const P = (pts) => pts.map(([a, b]) => `${a.toFixed(1)},${b.toFixed(1)}`).join(' ');
    out += `<polygon points="${P([dT, cT, cG, dG])}" fill="${C.graphiteL}"/>`;
    out += `<polygon points="${P([cT, bT, bG, cG])}" fill="${C.graphiteR}"/>`;
    if (c.lit && lit) {
      const anim = animate ? `<animate attributeName="opacity" values="1;0.55;1" dur="${(4 + (c.col % 5) * 0.7).toFixed(1)}s" begin="${((c.row * 0.4) % 3).toFixed(1)}s" repeatCount="indefinite"/>` : '';
      out += `<polygon points="${P([aT, bT, cT, dT])}" fill="${C.lime}">${anim}</polygon>`;
    } else {
      out += `<polygon points="${P([aT, bT, cT, dT])}" fill="${C.graphiteTop}"/>`;
    }
  }
  return out;
}

// ---------- assets ----------
function banner(F, data, numbers) {
  const W = 1200, H = 440;
  const name = 'Sai Asish Y';
  const role = 'Software engineer. Distributed systems, low latency infrastructure, databases.';
  const count = data.projects.length;
  const glowId = 'g' + Math.floor(Math.random() * 1e6);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(name)}. ${esc(role)}">
<defs>
  <radialGradient id="pool" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="${C.lime}" stop-opacity="0.16"/><stop offset="0.6" stop-color="${C.lime}" stop-opacity="0.04"/><stop offset="1" stop-color="${C.lime}" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect width="${W}" height="${H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="${W}" height="${H}" fill="${C.bg}"/>
<ellipse cx="850" cy="316" rx="360" ry="150" fill="url(#pool)"/>
${slab(data.projects, { x0: 850, y0: 208, unit: 21, lit: true, animate: true })}
${textPath(F.mono, 'SAY-5', 56, 64, 12, C.lime, { tracking: 0.16 })}
<rect x="118" y="59" width="18" height="1" fill="${C.lime}" opacity="0.5"/>
${textPath(F.s600, name, 52, 176, 84, C.paper, { tracking: -0.045 })}
${textPath(F.s400, 'Software engineer.', 56, 218, 20, C.dim)}
${textPath(F.s400, 'Distributed systems, low latency infrastructure, databases.', 56, 246, 20, C.dim)}
${textPath(F.s600, String(count), 52, 388, 72, C.paper, { tracking: -0.05 })}
${textPath(F.s500, 'public repos,', 52 + measure(F.s600, String(count), 72, -0.05) + 16, 366, 15, C.dim)}
${textPath(F.s500, 'one block each', 52 + measure(F.s600, String(count), 72, -0.05) + 16, 386, 15, C.dim)}
${textPath(F.s500, 'sayportfolio.vercel.app', 1148, 402, 13, C.faint, { anchor: 'end' })}
<rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="22" fill="none" stroke="${C.line}"/>
</g>
</svg>`;
}

function card(F, p, index) {
  const W = 580, H = 168;
  const num = String(index).padStart(3, '0');
  const lines = wrap(F.s400, p.tagline, 15, W - 64, 2);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(p.title)}: ${esc(p.tagline)}">
<rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="16" fill="${C.surface}" stroke="${C.line}"/>
<rect x="1" y="1" width="${W - 2}" height="1" fill="rgba(236,246,200,0.05)"/>
${textPath(F.mono, num, 32, 40, 11, C.lime, { tracking: 0.08 })}
${textPath(F.s500, `${p.language}  /  ${p.category}`, W - 32, 40, 12, C.faint, { anchor: 'end' })}
${textPath(F.s600, p.title, 31, 82, 27, C.paper, { tracking: -0.025 })}
${lines.map((l, i) => textPath(F.s400, l, 32, 112 + i * 21, 15, C.dim)).join('\n')}
${textPath(F.s500, 'Write-up and demo', W - 32, H - 22, 12, C.faint, { anchor: 'end' })}
<path d="M${W - 26} ${H - 30}l6-6m-5 0h5v5" fill="none" stroke="${C.lime}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;
}

function stats(F, data, numbers) {
  const W = 1200, H = 300;
  const cats = data.categories.map((label) => ({ label, count: data.projects.filter((p) => p.category === label).length })).filter((c) => c.count > 0).sort((a, b) => b.count - a.count);
  const max = Math.max(...cats.map((c) => c.count));
  const metrics = [
    { v: data.projects.length, l: 'public repos' },
    { v: numbers.mergedPRsElsewhere ?? numbers.mergedPRs, l: "merged PRs, other projects" },
    { v: data.flagships.length, l: "selected, with live demos" },
  ];
  let out = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Numbers">
<rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="22" fill="${C.surface}" stroke="${C.line}"/>`;
  metrics.forEach((m, i) => {
    const x = 44 + i * 236;
    const val = m.v == null ? '–' : String(m.v);
    out += textPath(F.s600, val, x, 96, 64, C.paper, { tracking: -0.05 });
    out += textPath(F.s500, m.l, x + 2, 124, 13, C.faint);
  });
  // category rows on the right
  const rx = 900, top = 44, rowH = 26;
  cats.forEach((c, i) => {
    const y = top + i * rowH;
    out += textPath(F.s400, c.label, rx - 12, y + 12, 12.5, C.dim, { anchor: 'end' });
    const blocks = c.count;
    const trackW = 210;
    const bw = Math.max(2, (trackW * (c.count / max)) / blocks - 2);
    for (let b = 0; b < blocks; b++) {
      out += `<rect x="${(rx + b * (bw + 2)).toFixed(1)}" y="${y + 3}" width="${bw.toFixed(1)}" height="10" fill="${C.limeDeep}" opacity="0.85"/>`;
    }
    out += textPath(F.mono, String(c.count).padStart(2, '0'), rx + trackW + 14, y + 12, 11, C.faint);
  });
  if (numbers.updated) out += textPath(F.s500, `Updated ${numbers.updated}`, 44, H - 26, 12, C.faint);
  out += textPath(F.s500, 'github.com/SAY-5', W - 44, H - 26, 12, C.faint, { anchor: 'end' });
  out += '</svg>';
  return out;
}

// ---------- README ----------
function readme(data, numbers) {
  const cards = data.flagships.map((p) => {
    const i = data.projects.findIndex((q) => q.name === p.name) + 1;
    return `<a href="${SITE}/p/${p.name}"><img src="assets/cards/${p.name}.svg" alt="${esc(p.title)}: ${esc(p.tagline)}" width="49%"></a>`;
  });
  const merged = numbers.mergedPRsElsewhere ?? numbers.mergedPRs;
  return `<a href="${SITE}"><img src="assets/banner.svg" alt="Sai Asish Y. Software engineer. Distributed systems, low latency infrastructure, databases." width="100%"></a>

<p>
  <a href="${SITE}">Portfolio</a> &nbsp;&middot;&nbsp;
  <a href="${DEMOS}">Live demos</a> &nbsp;&middot;&nbsp;
  <a href="https://www.linkedin.com/in/saiasishy/">LinkedIn</a> &nbsp;&middot;&nbsp;
  <a href="mailto:saiasish.cnp@gmail.com">saiasish.cnp@gmail.com</a>
</p>

Software engineer working on distributed systems, low latency infrastructure, and databases. MS in Computer Science from Stony Brook University, B.Tech from VIT. Previously at Nokia and in two research labs, CUBIT and the Data Management and Biomedical Analytics Lab. Open to SDE and SWE roles.

## Selected work

Each card opens the write-up; every one of these has a demo that runs in the browser.

<p>
${cards.join('\n')}
</p>

<a href="${SITE}/work"><img src="assets/stats.svg" alt="Numbers: public repos, merged pull requests, selected projects, and the catalog by category" width="100%"></a>

## Open source

${merged != null ? `${merged} merged pull requests in projects outside this account` : 'Merged pull requests in projects outside this account'} across the JavaScript, Python, Go, and Rust ecosystems. Until May 2026 the approach was volume; since May 5, 2026 it is one issue at a time: reproduce it, fix it, test it, and land a single clean change. Apologies to the maintainers who dealt with duplicate or half-tested PRs before that.

## Contributions

<img src="https://raw.githubusercontent.com/SAY-5/SAY-5/output/github-snake-dark.svg" alt="Contribution graph" width="100%">

<sub>Assets are generated from the portfolio's project data by <code>scripts/build.mjs</code> and refreshed daily.</sub>
`;
}

// ---------- main ----------
const data = await loadProjects();
const numbers = await githubNumbers();
const F = await loadFonts();
fs.writeFileSync(path.join(ASSETS, 'banner.svg'), banner(F, data, numbers));
fs.writeFileSync(path.join(ASSETS, 'stats.svg'), stats(F, data, numbers));
for (const p of data.flagships) {
  const i = data.projects.findIndex((q) => q.name === p.name) + 1;
  fs.writeFileSync(path.join(ASSETS, 'cards', `${p.name}.svg`), card(F, p, i));
}
fs.writeFileSync(path.join(ROOT, 'README.md'), readme(data, numbers));
console.log(`built: banner, stats, ${data.flagships.length} cards, README (${data.projects.length} projects, numbers ${JSON.stringify(numbers)})`);
