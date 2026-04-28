#!/usr/bin/env python3
"""Regenerate metrics.svg and ribbon.svg from live GitHub API data.

Claude design palette:
  bg #1A1714 · cards #22201D · terracotta #D97757 · sand #BBA68A
  cream #F5F1E8 text, warm-muted #A69B88, dim #7A6E5E

ribbon.svg renders the year of contribution data as an organic flowing
curve. Each day's contribution count drives the local thickness of the
ribbon. Cubic-bezier smoothing across daily points; gradient fill.
"""
import json
import math
import subprocess
from pathlib import Path

USER = "SAY-5"
REPO_ROOT = Path(__file__).resolve().parent.parent

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True).strip()


def fetch_metrics():
    prs_merged = int(gh("api", "-X", "GET", "search/issues",
                        "-f", f"q=author:{USER} is:pr is:merged",
                        "--jq", ".total_count"))

    urls = set()
    for page in range(1, 12):
        out = gh("api", "-X", "GET", "search/issues",
                 "-f", f"q=author:{USER} is:pr is:merged",
                 "-F", "per_page=100", "-F", f"page={page}",
                 "--jq", ".items[].repository_url")
        page_urls = [u for u in out.splitlines() if u]
        urls.update(page_urls)
        if len(page_urls) < 100:
            break
    unique_repos = len(urls)

    commits = int(gh("api", "-X", "GET", "search/commits",
                     "-f", f"q=author:{USER}",
                     "-H", "Accept: application/vnd.github.cloak-preview+json",
                     "--jq", ".total_count"))

    originals = 0
    for page in range(1, 20):
        out = gh("api", f"users/{USER}/repos?per_page=100&page={page}")
        data = json.loads(out)
        if not data:
            break
        originals += sum(1 for r in data if not r["fork"])
        if len(data) < 100:
            break

    return {
        "prs": prs_merged,
        "repos": unique_repos,
        "commits": commits,
        "originals": originals,
    }


def fetch_contributions():
    query = ('{ user(login: "%s") { contributionsCollection '
             '{ contributionCalendar { totalContributions weeks '
             '{ contributionDays { date contributionCount } } } } } }') % USER
    out = gh("api", "graphql", "-f", f"query={query}")
    return json.loads(out)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


METRICS_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 180" width="1280" height="180">
  <defs>
    <pattern id="mDots" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#F5F1E8" fill-opacity="0.03"/>
    </pattern>
  </defs>
  <rect width="1280" height="180" fill="#1A1714"/>
  <rect width="1280" height="180" fill="url(#mDots)"/>
  <line x1="0" y1="0.5" x2="1280" y2="0.5" stroke="#F5F1E8" stroke-opacity="0.08"/>
  <line x1="0" y1="179.5" x2="1280" y2="179.5" stroke="#F5F1E8" stroke-opacity="0.08"/>

  <g transform="translate(96, 44)">
    <text x="0" y="0" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="500" fill="#A69B88" letter-spacing="3.5">&#8212;&#8201;&#8201;&#8201;GITHUB ACTIVITY</text>
  </g>

  <g font-family="ui-serif, Charter, Georgia, serif" font-size="52" font-weight="500" fill="#F5F1E8" letter-spacing="-2">
    <text x="96" y="130">{prs}</text>
    <text x="340" y="130">{repos}</text>
    <text x="630" y="130">{commits}</text>
    <text x="930" y="130">{originals}</text>
  </g>

  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" font-weight="500" fill="#7A6E5E" letter-spacing="2">
    <text x="96"  y="150">PRS MERGED</text>
    <text x="340" y="150">REPOSITORIES</text>
    <text x="630" y="150">COMMITS</text>
    <text x="930" y="150">ORIGINAL PROJECTS</text>
  </g>

  <line x1="304" y1="84" x2="304" y2="154" stroke="#F5F1E8" stroke-opacity="0.06"/>
  <line x1="594" y1="84" x2="594" y2="154" stroke="#F5F1E8" stroke-opacity="0.06"/>
  <line x1="894" y1="84" x2="894" y2="154" stroke="#F5F1E8" stroke-opacity="0.06"/>
</svg>
'''


def render_metrics(m):
    return METRICS_TEMPLATE.format(**m)


def cubic_path_through(coords):
    """Smooth path through points using cubic beziers with shared control x."""
    if not coords:
        return ""
    if len(coords) == 1:
        return f"M {coords[0][0]:.2f} {coords[0][1]:.2f}"
    parts = [f"M {coords[0][0]:.2f} {coords[0][1]:.2f}"]
    for i in range(1, len(coords)):
        x0, y0 = coords[i - 1]
        x1, y1 = coords[i]
        cx = (x0 + x1) / 2
        parts.append(f"C {cx:.2f} {y0:.2f} {cx:.2f} {y1:.2f} {x1:.2f} {y1:.2f}")
    return " ".join(parts)


def render_ribbon(cal):
    days = []
    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            days.append((day["date"], day["contributionCount"]))

    total = cal["totalContributions"]
    if not days:
        return ""

    n = len(days)
    max_count = max(d[1] for d in days) or 1

    width = 1280
    height = 380
    L = 96
    R = 96
    chart_w = width - L - R
    top_y = 168
    chart_h = 152
    center_y = top_y + chart_h / 2
    max_half = chart_h / 2 - 6
    min_half = 1.5

    pts = []
    for i, (date, count) in enumerate(days):
        x = L + (i / (n - 1)) * chart_w if n > 1 else L + chart_w / 2
        scaled = math.log(1 + count) / math.log(1 + max_count)
        half_h = max(min_half, scaled * max_half)
        pts.append((x, center_y - half_h, center_y + half_h))

    top_coords = [(p[0], p[1]) for p in pts]
    bot_coords = [(p[0], p[2]) for p in reversed(pts)]

    top_path = cubic_path_through(top_coords)
    bot_smooth = cubic_path_through(bot_coords)
    if bot_smooth.startswith("M "):
        bot_smooth = "L " + bot_smooth[2:]
    full_path = f"{top_path} {bot_smooth} Z"

    month_x = []
    last_m = None
    for i, (date, _) in enumerate(days):
        m_idx = int(date[5:7]) - 1
        if m_idx != last_m:
            x = L + (i / (n - 1)) * chart_w
            month_x.append((x, MONTHS[m_idx]))
            last_m = m_idx

    month_svg = "\n  ".join(
        f'<text x="{x:.1f}" y="{top_y + chart_h + 30:.1f}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10" font-weight="500" fill="#7A6E5E" letter-spacing="1.8">{m}</text>'
        for x, m in month_x
    )

    # Faint daily tick marks below the ribbon for texture
    ticks = []
    for i, (date, count) in enumerate(days):
        if count == 0:
            continue
        x = L + (i / (n - 1)) * chart_w
        opacity = min(0.4, 0.06 + math.log(1 + count) / math.log(1 + max_count) * 0.34)
        ticks.append(
            f'<rect x="{x - 0.7:.2f}" y="{top_y + chart_h + 8:.1f}" width="1.4" height="6" fill="#D97757" fill-opacity="{opacity:.2f}"/>'
        )
    ticks_svg = "\n  ".join(ticks)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="ribbonGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#A6896B" stop-opacity="0.85"/>
      <stop offset="35%"  stop-color="#D97757" stop-opacity="0.95"/>
      <stop offset="70%"  stop-color="#E8A27C" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#F5C09B" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="ribbonShade" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="50%"  stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.22"/>
    </linearGradient>
    <radialGradient id="rGlow" cx="50%" cy="60%" r="55%">
      <stop offset="0%"   stop-color="#D97757" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#1A1714" stop-opacity="0"/>
    </radialGradient>
    <pattern id="rDots" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#F5F1E8" fill-opacity="0.025"/>
    </pattern>
    <filter id="rGlowF" x="-10%" y="-50%" width="120%" height="200%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect width="{width}" height="{height}" fill="#1A1714"/>
  <rect width="{width}" height="{height}" fill="url(#rDots)"/>
  <rect width="{width}" height="{height}" fill="url(#rGlow)"/>

  <line x1="96" y1="72" x2="1184" y2="72" stroke="#F5F1E8" stroke-opacity="0.08"/>

  <g transform="translate(96, 54)" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="500" letter-spacing="3.5">
    <text x="0" y="0" fill="#A69B88">&#8212;&#8201;&#8201;&#8201;CONTRIBUTION ACTIVITY</text>
    <text x="1088" y="0" fill="#6C5F4E" text-anchor="end">LAST 365 DAYS &#183; AS A RIBBON</text>
  </g>

  <text x="96" y="124" font-family="ui-serif, Charter, Georgia, serif" font-size="36" font-style="italic" font-weight="500" fill="#F5F1E8" letter-spacing="-1.2">{total} contributions, <tspan font-style="normal" font-size="22" fill="#7A6E5E" font-family="ui-sans-serif, -apple-system, 'Inter', sans-serif">drawn from {n} days of work.</tspan></text>

  <line x1="96" y1="{center_y:.1f}" x2="1184" y2="{center_y:.1f}" stroke="#F5F1E8" stroke-opacity="0.05" stroke-dasharray="2 6"/>

  <path d="{full_path}" fill="url(#ribbonGrad)" stroke="none" filter="url(#rGlowF)" opacity="0.55"/>
  <path d="{full_path}" fill="url(#ribbonGrad)" stroke="none"/>
  <path d="{full_path}" fill="url(#ribbonShade)" stroke="none"/>

  {ticks_svg}

  {month_svg}
</svg>
'''


def main():
    metrics = fetch_metrics()
    (REPO_ROOT / "metrics.svg").write_text(render_metrics(metrics))
    print(f"metrics.svg :: {metrics}")

    cal = fetch_contributions()
    (REPO_ROOT / "ribbon.svg").write_text(render_ribbon(cal))
    print(f"ribbon.svg :: {cal['totalContributions']} contributions over "
          f"{sum(len(w['contributionDays']) for w in cal['weeks'])} days")


if __name__ == "__main__":
    main()
