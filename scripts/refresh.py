#!/usr/bin/env python3
"""Regenerate metrics.svg and activity.svg from live GitHub API data."""
import json
import subprocess
from pathlib import Path

USER = "SAY-5"
REPO_ROOT = Path(__file__).resolve().parent.parent


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


METRICS_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 340" width="1280" height="340">
  <defs>
    <linearGradient id="numGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#7C6BFF"/>
    </linearGradient>
    <linearGradient id="numGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#4AF0C0"/>
    </linearGradient>
    <linearGradient id="numGrad3" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="numGrad4" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F0A04A"/>
    </linearGradient>
    <radialGradient id="bgGlow" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#1A1D28" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#08090C" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#FFFFFF" fill-opacity="0.035"/>
    </pattern>
  </defs>
  <rect width="1280" height="340" fill="#08090C"/>
  <rect width="1280" height="340" fill="url(#dots)"/>
  <rect width="1280" height="340" fill="url(#bgGlow)"/>
  <line x1="0" y1="0.5" x2="1280" y2="0.5" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="0" y1="339.5" x2="1280" y2="339.5" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <g transform="translate(96, 60)">
    <text x="0" y="0" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="500" fill="#6B7085" letter-spacing="3.5">&#8212;&#8201;&#8201;&#8201;GITHUB ACTIVITY</text>
    <text x="0" y="28" font-family="ui-sans-serif, -apple-system, 'Inter', 'Segoe UI', sans-serif" font-size="24" font-weight="600" fill="#E8EAED" letter-spacing="-0.8">Open-source contributions and shipped work.</text>
  </g>
  <g font-family="ui-sans-serif, -apple-system, 'Inter', 'Segoe UI', sans-serif">
    <g transform="translate(96, 176)">
      <text x="0" y="0" font-size="108" font-weight="600" fill="url(#numGrad1)" letter-spacing="-5">{prs}</text>
      <text x="0" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" font-weight="500" fill="#6B7085" letter-spacing="2.5">PULL REQUESTS MERGED</text>
      <text x="0" y="62" font-size="13" font-weight="400" fill="#8B8F9E" letter-spacing="-0.2">Astro, langchain, drizzle, bun, Nim&#8230;</text>
    </g>
    <line x1="360" y1="120" x2="360" y2="280" stroke="#FFFFFF" stroke-opacity="0.06"/>
    <g transform="translate(400, 176)">
      <text x="0" y="0" font-size="108" font-weight="600" fill="url(#numGrad2)" letter-spacing="-5">{repos}</text>
      <text x="0" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" font-weight="500" fill="#6B7085" letter-spacing="2.5">REPOSITORIES CONTRIBUTED</text>
      <text x="0" y="62" font-size="13" font-weight="400" fill="#8B8F9E" letter-spacing="-0.2">Across languages, ecosystems, domains.</text>
    </g>
    <line x1="664" y1="120" x2="664" y2="280" stroke="#FFFFFF" stroke-opacity="0.06"/>
    <g transform="translate(704, 176)">
      <text x="0" y="0" font-size="108" font-weight="600" fill="url(#numGrad3)" letter-spacing="-5">{commits}</text>
      <text x="0" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" font-weight="500" fill="#6B7085" letter-spacing="2.5">COMMITS AUTHORED</text>
      <text x="0" y="62" font-size="13" font-weight="400" fill="#8B8F9E" letter-spacing="-0.2">Patches, features, test coverage.</text>
    </g>
    <line x1="920" y1="120" x2="920" y2="280" stroke="#FFFFFF" stroke-opacity="0.06"/>
    <g transform="translate(960, 176)">
      <text x="0" y="0" font-size="108" font-weight="600" fill="url(#numGrad4)" letter-spacing="-5">{originals}</text>
      <text x="0" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" font-weight="500" fill="#6B7085" letter-spacing="2.5">ORIGINAL PROJECTS</text>
      <text x="0" y="62" font-size="13" font-weight="400" fill="#8B8F9E" letter-spacing="-0.2">Built from scratch, shipped solo.</text>
    </g>
  </g>
</svg>
'''


def render_metrics(m):
    return METRICS_TEMPLATE.format(**m)


def level_color(count):
    if count == 0:
        return "#14161C"
    if count <= 2:
        return "#2D2A5E"
    if count <= 9:
        return "#4E44A8"
    if count <= 30:
        return "#6353D8"
    return "#8B7EFF"


MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def render_activity(cal):
    weeks = cal["weeks"]
    total = cal["totalContributions"]

    cell = 13
    gap = 3
    stride = cell + gap

    left = 96
    top = 160
    width = 1280
    grid_h = 7 * stride
    height = top + grid_h + 80

    # cells
    cells = []
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week["contributionDays"]):
            x = left + wi * stride
            y = top + di * stride
            c = level_color(day["contributionCount"])
            cells.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>')
    cells_svg = "\n  ".join(cells)

    # month labels
    months = []
    last_month = None
    for wi, week in enumerate(weeks):
        first_day = week["contributionDays"][0]["date"]
        m_idx = int(first_day[5:7]) - 1
        if m_idx != last_month and wi < len(weeks) - 2:
            x = left + wi * stride
            months.append(
                f'<text x="{x}" y="{top - 14}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
                f'font-size="10" font-weight="500" fill="#6B7085" letter-spacing="1.8">{MONTHS[m_idx]}</text>')
            last_month = m_idx
    months_svg = "\n  ".join(months)

    # day labels (Mon, Wed, Fri)
    day_svgs = []
    for di, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = top + di * stride + 10
        day_svgs.append(
            f'<text x="{left - 40}" y="{y}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'font-size="10" font-weight="500" fill="#6B7085" letter-spacing="1">{label}</text>')
    days_svg = "\n  ".join(day_svgs)

    # legend
    legend_y = top + grid_h + 32
    legend_x_start = width - 96 - (5 * (cell + 3) + 80)
    legend_colors = ["#14161C", "#2D2A5E", "#4E44A8", "#6353D8", "#8B7EFF"]
    legend_svg = (
        f'<text x="{legend_x_start}" y="{legend_y + 10}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
        f'font-size="10" font-weight="500" fill="#6B7085" letter-spacing="1.8">LESS</text>'
    )
    for i, c in enumerate(legend_colors):
        x = legend_x_start + 40 + i * (cell + 3)
        legend_svg += (
            f'<rect x="{x}" y="{legend_y}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>'
        )
    more_x = legend_x_start + 40 + 5 * (cell + 3) + 4
    legend_svg += (
        f'<text x="{more_x}" y="{legend_y + 10}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
        f'font-size="10" font-weight="500" fill="#6B7085" letter-spacing="1.8">MORE</text>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <pattern id="dotsA" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#FFFFFF" fill-opacity="0.03"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="#08090C"/>
  <rect width="{width}" height="{height}" fill="url(#dotsA)"/>
  <g transform="translate(96, 60)">
    <text x="0" y="0" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="500" fill="#6B7085" letter-spacing="3.5">&#8212;&#8201;&#8201;&#8201;CONTRIBUTION ACTIVITY</text>
    <text x="0" y="28" font-family="ui-sans-serif, -apple-system, 'Inter', 'Segoe UI', sans-serif" font-size="24" font-weight="600" fill="#E8EAED" letter-spacing="-0.8">{total} contributions in the last year.</text>
  </g>
  {months_svg}
  {days_svg}
  {cells_svg}
  {legend_svg}
</svg>
'''


def main():
    metrics = fetch_metrics()
    (REPO_ROOT / "metrics.svg").write_text(render_metrics(metrics))
    print(f"metrics.svg :: {metrics}")

    cal = fetch_contributions()
    (REPO_ROOT / "activity.svg").write_text(render_activity(cal))
    print(f"activity.svg :: {cal['totalContributions']} contributions, {len(cal['weeks'])} weeks")


if __name__ == "__main__":
    main()
