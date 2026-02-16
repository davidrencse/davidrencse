from __future__ import annotations

from datetime import datetime, timezone

import gifos

USERNAME = "davidrencse"
OUTPUT_GIF = "output.gif"
README_PATH = "README.md"


def _safe_stats(username: str):
    """Fetch stats without failing generation if the API call is rate-limited."""
    try:
        return gifos.utils.fetch_github_stats(user_name=username)
    except Exception:
        return None


def _format_stats(stats) -> tuple[str, str, str, str, str]:
    if stats is None:
        return ("N/A", "N/A", "N/A", "N/A", "N/A")

    top_langs = (
        ", ".join(lang for lang, _ in stats.languages_sorted[:5])
        if getattr(stats, "languages_sorted", None)
        else "N/A"
    )

    rank = getattr(getattr(stats, "user_rank", None), "level", "N/A")

    return (
        str(getattr(stats, "total_stargazers", "N/A")),
        str(getattr(stats, "total_commits_last_year", "N/A")),
        str(getattr(stats, "total_pull_requests_made", "N/A")),
        str(rank),
        top_langs,
    )


def build_terminal_gif() -> None:
    t = gifos.Terminal(
        width=860,
        height=520,
        xpad=10,
        ypad=10,
        font_file="",
        font_size=16,
        line_spacing=1,
        prompt="",
        fps=24,
    )

    t.set_bg("#0d1117")
    t.set_font_color("#c9d1d9")

    t.gen_text("Booting profile terminal...", row_num=1, count=12)
    t.gen_text("Initializing session for visitor", row_num=2, count=12)
    t.gen_text("", row_num=3, count=10)

    t.toggle_show_cursor(True)
    t.gen_prompt(row_num=4)
    t.gen_typing_text(text="whoami", row_num=4, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text(text="davidrencse", row_num=5, count=8)

    t.toggle_show_cursor(True)
    t.gen_prompt(row_num=6)
    t.gen_typing_text(text="github --summary", row_num=6, contin=True)
    t.toggle_show_cursor(False)

    stats = _safe_stats(USERNAME)
    stars, commits, prs, rank, languages = _format_stats(stats)

    summary = (
        f"\\x1b[30;46m {USERNAME}@github \\x1b[0m\n"
        f"- Stars: {stars}\n"
        f"- Commits (last year): {commits}\n"
        f"- Pull requests: {prs}\n"
        f"- Rank: {rank}\n"
        f"- Top languages: {languages}\n"
    )
    t.gen_text(text=summary, row_num=7, col_num=2, count=3, contin=True)

    t.toggle_show_cursor(True)
    t.gen_prompt(row_num=t.curr_row + 1)
    t.gen_typing_text(text="echo 'thanks for visiting'", row_num=t.curr_row, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text(text="thanks for visiting", row_num=t.curr_row + 1, count=8)

    t.gen_text(text="", row_num=t.curr_row + 1, count=120, contin=True)
    t.gen_gif()


def build_readme() -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    readme = f"""<p align=\"center\">\n  <img src=\"./{OUTPUT_GIF}\" alt=\"Terminal animation\"/>\n</p>\n\n<p align=\"center\">\n  Auto-generated with <a href=\"https://github.com/x0rzavi/github-readme-terminal\">github-readme-terminal</a>.\n</p>\n\n<p align=\"center\">Last updated: {generated_at}</p>\n"""

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)


def main() -> None:
    build_terminal_gif()
    build_readme()


if __name__ == "__main__":
    main()
