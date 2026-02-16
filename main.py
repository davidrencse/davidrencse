from datetime import datetime, timezone
import json
import os
from urllib import request

import gifos

USERNAME = "davidrencse"
OUTPUT_GIF = "output.gif"
README_PATH = "README.md"
TOP_LANGUAGES = "Python, C++, C, JavaScript, AWS, HTML, CSS, SQL"


def _safe_stats(username):
    try:
        return gifos.utils.fetch_github_stats(username)
    except Exception:
        return None


def _get_commits_last_year(username):
    stats = _safe_stats(username)
    if stats is not None:
        commits = getattr(stats, "total_commits_last_year", None)
        if commits is not None:
            return str(commits)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "N/A"

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          totalCommitContributions
        }
      }
    }
    """
    body = json.dumps(
        {"query": query, "variables": {"login": username}}
    ).encode("utf-8")
    req = request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        commits = payload["data"]["user"]["contributionsCollection"][
            "totalCommitContributions"
        ]
        return str(commits)
    except Exception:
        return "N/A"


def _format_summary(username):
    commits = _get_commits_last_year(username)
    return (
        f"\x1b[30;46m {username}@github \x1b[0m\n"
        f"- Commits (last year): {commits}\n"
        f"- Top languages: {TOP_LANGUAGES}\n"
    )


def build_terminal_gif():
    t = gifos.Terminal(860, 520, 10, 10)

    t.gen_text("Booting profile terminal...", 1, count=10)
    t.gen_text("Initializing session for visitor", 2, count=10)
    t.gen_text("", 3, count=8)

    t.toggle_show_cursor(True)
    t.gen_prompt(4)
    t.gen_typing_text("whoami", 4, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text(USERNAME, 5, count=6)

    t.toggle_show_cursor(True)
    t.gen_prompt(6)
    t.gen_typing_text("github --summary", 6, contin=True)
    t.toggle_show_cursor(False)

    summary = _format_summary(USERNAME)
    t.gen_text(summary, 7, 2, count=2, contin=True)

    t.gen_prompt(t.curr_row + 1)
    t.toggle_show_cursor(True)
    t.gen_typing_text("echo 'thanks for visiting'", t.curr_row, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text("thanks for visiting", t.curr_row + 1, count=6)

    t.gen_text("", t.curr_row + 1, count=80, contin=True)
    t.gen_gif()


def build_readme():
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    readme = (
        f"<p align=\"center\">\n"
        f"  <img src=\"./{OUTPUT_GIF}\" alt=\"Terminal animation\"/>\n"
        f"</p>\n\n"
        f"<p align=\"center\">Last updated: {generated_at}</p>\n"
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)


def main():
    build_terminal_gif()
    build_readme()


if __name__ == "__main__":
    main()
