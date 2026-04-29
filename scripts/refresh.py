#!/usr/bin/env python3
"""Regenerate metrics.svg from live GitHub API data.

Apple keynote palette:
  pure black #000000  ·  white #FFFFFF  ·  silver #A1A1A6
  muted #86868B  ·  dim #525252
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


METRICS_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 540" width="1280" height="540">
  <defs>
    <linearGradient id="bigNumGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#525252"/>
    </linearGradient>
  </defs>

  <rect width="1280" height="540" fill="#000000"/>

  <text x="640" y="120" text-anchor="middle"
        font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif"
        font-size="14" font-weight="500" fill="#86868B" letter-spacing="3">A YEAR IN OPEN SOURCE</text>

  <text x="640" y="320" text-anchor="middle"
        font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif"
        font-size="240" font-weight="600" fill="url(#bigNumGrad)" letter-spacing="-12">{prs}</text>

  <text x="640" y="380" text-anchor="middle"
        font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif"
        font-size="32" font-weight="400" fill="#FFFFFF" letter-spacing="-0.6">pull requests merged.</text>

  <text x="640" y="430" text-anchor="middle"
        font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif"
        font-size="17" font-weight="400" fill="#86868B" letter-spacing="-0.2">Across {repos} repositories. {commits} commits authored. {originals} original projects shipped solo.</text>

  <line x1="600" y1="480" x2="680" y2="480" stroke="#525252" stroke-width="1"/>
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
