#!/usr/bin/env python3
"""Regenerate metrics.svg from live GitHub API data.

Pure monochrome palette:
  bg #0A0A0A · cards #141414 · borders #262626
  text #FAFAFA · secondary #A1A1A1 · muted #737373 · dim #525252
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


METRICS_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 180" width="1280" height="180">
  <defs>
    <pattern id="mDots" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#FFFFFF" fill-opacity="0.025"/>
    </pattern>
  </defs>
  <rect width="1280" height="180" fill="#0A0A0A"/>
  <rect width="1280" height="180" fill="url(#mDots)"/>
  <line x1="0" y1="0.5" x2="1280" y2="0.5" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="0" y1="179.5" x2="1280" y2="179.5" stroke="#FFFFFF" stroke-opacity="0.08"/>

  <g transform="translate(96, 44)">
    <text x="0" y="0" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="500" fill="#A1A1A1" letter-spacing="3.5">&#8212;&#8201;&#8201;&#8201;GITHUB ACTIVITY</text>
  </g>

  <g font-family="ui-serif, Charter, Georgia, serif" font-size="52" font-weight="500" fill="#FAFAFA" letter-spacing="-2">
    <text x="96" y="130">{prs}</text>
    <text x="340" y="130">{repos}</text>
    <text x="630" y="130">{commits}</text>
    <text x="930" y="130">{originals}</text>
  </g>

  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" font-weight="500" fill="#525252" letter-spacing="2">
    <text x="96"  y="150">PRS MERGED</text>
    <text x="340" y="150">REPOSITORIES</text>
    <text x="630" y="150">COMMITS</text>
    <text x="930" y="150">ORIGINAL PROJECTS</text>
  </g>

  <line x1="304" y1="84" x2="304" y2="154" stroke="#FFFFFF" stroke-opacity="0.06"/>
  <line x1="594" y1="84" x2="594" y2="154" stroke="#FFFFFF" stroke-opacity="0.06"/>
  <line x1="894" y1="84" x2="894" y2="154" stroke="#FFFFFF" stroke-opacity="0.06"/>
</svg>
'''


def render_metrics(m):
    return METRICS_TEMPLATE.format(**m)


def main():
    metrics = fetch_metrics()
    (REPO_ROOT / "metrics.svg").write_text(render_metrics(metrics))
    print(f"metrics.svg :: {metrics}")


if __name__ == "__main__":
    main()
