from datetime import datetime, timezone

import gifos

USERNAME = "davidrencse"
OUTPUT_GIF = "output.gif"
README_PATH = "README.md"


def _safe_stats(username):
    try:
        return gifos.utils.fetch_github_stats(username)
    except Exception:
        return None


def _format_stats(stats):
    if stats is None:
        return ("N/A", "N/A", "N/A", "N/A", "N/A")

    top_langs = "N/A"
    if getattr(stats, "languages_sorted", None):
        top_langs = ", ".join(lang[0] for lang in stats.languages_sorted[:5])

    rank = "N/A"
    if getattr(stats, "user_rank", None):
        rank = getattr(stats.user_rank, "level", "N/A")

    return (
        str(getattr(stats, "total_stargazers", "N/A")),
        str(getattr(stats, "total_commits_last_year", "N/A")),
        str(getattr(stats, "total_pull_requests_made", "N/A")),
        str(rank),
        top_langs,
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

    stats = _safe_stats(USERNAME)
    stars, commits, prs, rank, languages = _format_stats(stats)

    summary = (
        f"\x1b[30;46m {USERNAME}@github \x1b[0m\n"
        f"- Stars: {stars}\n"
        f"- Commits (last year): {commits}\n"
        f"- Pull requests: {prs}\n"
        f"- Rank: {rank}\n"
        f"- Top languages: {languages}\n"
    )
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
        f"<p align=\"center\">\n"
        f"  Auto-generated with "
        f"<a href=\"https://github.com/x0rzavi/github-readme-terminal\">github-readme-terminal</a>.\n"
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
