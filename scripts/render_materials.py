from html import escape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots"


def render_markdown(md_text: str, title: str) -> str:
    body = []
    in_code = False
    code_lines = []
    list_open = False

    def close_list():
        nonlocal list_open
        if list_open:
            body.append("</ul>")
            list_open = False

    def inline(text: str) -> str:
        escaped = escape(text)
        return re.sub(
            r"\[([^\]]+)\]\((https?://[^)]+)\)",
            r'<a href="\2">\1</a>',
            escaped,
        )

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            if in_code:
                body.append("<pre><code>" + escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                close_list()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line:
            close_list()
            continue

        if line.startswith("# "):
            close_list()
            body.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            close_list()
            body.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("- "):
            if not list_open:
                body.append("<ul>")
                list_open = True
            body.append(f"<li>{inline(line[2:])}</li>")
        elif len(line) > 3 and line[0].isdigit() and line[1:3] == ". ":
            close_list()
            body.append(f"<p>{inline(line)}</p>")
        else:
            close_list()
            body.append(f"<p>{inline(line)}</p>")

    close_list()

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #111827;
      --muted: #5b6472;
      --line: #d7dde6;
      --accent: #0f766e;
      --paper: #ffffff;
      --bg: #f3f6f8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
      line-height: 1.65;
      padding: 36px;
    }}
    main {{
      width: 980px;
      margin: 0 auto;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 42px 52px;
      box-shadow: 0 18px 48px rgba(17, 24, 39, 0.08);
    }}
    h1 {{
      font-size: 34px;
      line-height: 1.18;
      margin: 0 0 22px;
      letter-spacing: 0;
    }}
    h2 {{
      font-size: 22px;
      margin: 30px 0 12px;
      padding-top: 18px;
      border-top: 1px solid var(--line);
      letter-spacing: 0;
    }}
    p, li {{
      font-size: 17px;
      margin: 8px 0;
    }}
    ul {{
      padding-left: 24px;
      margin: 8px 0 12px;
    }}
    pre {{
      background: #0b1220;
      color: #dbeafe;
      border-radius: 8px;
      padding: 16px 18px;
      overflow: hidden;
      font-size: 15px;
      line-height: 1.55;
    }}
    a {{
      color: #0f766e;
      text-decoration: none;
      font-weight: 650;
    }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
    }}
    p:first-of-type {{
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <main>
    {''.join(body)}
  </main>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    materials = [
        (ROOT / "README.md", OUT / "readme.html", "AI Quant Agent README"),
        (ROOT / "reports" / "AAPL_report.md", OUT / "aapl-report.html", "AAPL Report"),
    ]
    for source, target, title in materials:
        target.write_text(render_markdown(source.read_text(encoding="utf-8"), title), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
