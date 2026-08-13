"""Generate the profile README from README.template.md."""

from datetime import date
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


USERNAME = "nacayu"
ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.md"


def github_get(path: str):
    """Fetch a GitHub API endpoint with a small, CI-friendly timeout."""
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "nacayu-profile-readme"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def get_github_stats():
    """Return the values used by the generated README."""
    user = github_get(f"/users/{USERNAME}")
    repos = []
    for page in range(1, 4):
        batch = github_get(f"/users/{USERNAME}/repos?per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break

    repo_map = {repo["name"]: repo for repo in repos}
    return {
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "repos": user.get("public_repos", 0),
        "stars": sum(repo.get("stargazers_count", 0) for repo in repos),
        "forks": sum(repo.get("forks_count", 0) for repo in repos),
        "radar_stars": repo_map.get("awesome-deeplearning-based-radar-perception", {}).get("stargazers_count", 0),
        "website_stars": repo_map.get("nacayu.github.io", {}).get("stargazers_count", 0),
        "crfnet_stars": repo_map.get("CRFNet_Tensorflow2.4.1", {}).get("stargazers_count", 0),
        "saf_fcos_stars": repo_map.get("SAF-FCOS", {}).get("stargazers_count", 0),
        "update_date": date.today().isoformat(),
    }


def generate_readme():
    stats = get_github_stats()
    content = TEMPLATE.read_text(encoding="utf-8")
    for key, value in stats.items():
        content = content.replace("{{ " + key + " }}", str(value))
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Updated {OUTPUT.name}: {stats['repos']} public repositories")


if __name__ == "__main__":
    try:
        generate_readme()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise SystemExit(f"GitHub API request failed: {exc}")
