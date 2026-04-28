#!/usr/bin/env python3
"""Regenerate metrics.svg and activity.svg from live GitHub API data.

Claude design palette:
  bg #1A1714 · cards #22201D · accent #D97757 (terracotta) · sand #BBA68A
  cream #F5F1E8 text, warm-muted #A69B88, dim #7A6E5E
"""
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


def level_color(count):
    if count == 0:
        return "#241F1B"
    if count <= 2:
        return "#4A3224"
    if count <= 9:
        return "#8C4D2F"
    if count <= 30:
        return "#C06339"
    return "#E8A27C"


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

    cells = []
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week["contributionDays"]):
            x = left + wi * stride
            y = top + di * stride
            c = level_color(day["contributionCount"])
            cells.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>')
    cells_svg = "\n  ".join(cells)

    months = []
    last_month = None
    for wi, week in enumerate(weeks):
        first_day = week["contributionDays"][0]["date"]
        m_idx = int(first_day[5:7]) - 1
        if m_idx != last_month and wi < len(weeks) - 2:
            x = left + wi * stride
            months.append(
                f'<text x="{x}" y="{top - 14}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
                f'font-size="10" font-weight="500" fill="#A69B88" letter-spacing="1.8">{MONTHS[m_idx]}</text>')
            last_month = m_idx
    months_svg = "\n  ".join(months)

    day_svgs = []
    for di, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = top + di * stride + 10
        day_svgs.append(
            f'<text x="{left - 40}" y="{y}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'font-size="10" font-weight="500" fill="#A69B88" letter-spacing="1">{label}</text>')
    days_svg = "\n  ".join(day_svgs)

    legend_y = top + grid_h + 32
    legend_x_start = width - 96 - (5 * (cell + 3) + 80)
    legend_colors = ["#241F1B", "#4A3224", "#8C4D2F", "#C06339", "#E8A27C"]
    legend_svg = (
        f'<text x="{legend_x_start}" y="{legend_y + 10}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
        f'font-size="10" font-weight="500" fill="#A69B88" letter-spacing="1.8">LESS</text>'
    )
    for i, c in enumerate(legend_colors):
        x = legend_x_start + 40 + i * (cell + 3)
        legend_svg += (
            f'<rect x="{x}" y="{legend_y}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>'
        )
    more_x = legend_x_start + 40 + 5 * (cell + 3) + 4
    legend_svg += (
        f'<text x="{more_x}" y="{legend_y + 10}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
        f'font-size="10" font-weight="500" fill="#A69B88" letter-spacing="1.8">MORE</text>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <pattern id="dotsA" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#F5F1E8" fill-opacity="0.03"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="#1A1714"/>
  <rect width="{width}" height="{height}" fill="url(#dotsA)"/>
  <g transform="translate(96, 60)">
    <text x="0" y="0" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="500" fill="#A69B88" letter-spacing="3.5">&#8212;&#8201;&#8201;&#8201;CONTRIBUTION ACTIVITY</text>
    <text x="0" y="30" font-family="ui-serif, Charter, Georgia, serif" font-size="26" font-weight="500" fill="#F5F1E8" letter-spacing="-0.8">{total} contributions in the last year.</text>
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


if __name__ == "__main__":
    main()
