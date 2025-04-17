import pathlib
import sys
import re

REPLACEMENTS = {
    r"https://cdn.jsdelivr.net/npm/bootstrap@5.[^/]*/dist/css/bootstrap.min.css": "{{ bootstrap5_css_url }}",
    r"https://cdn.jsdelivr.net/npm/bootstrap@5.[^/]*/dist/js/bootstrap.bundle.min.js": "{{ bootstrap5_js_url }}",
    'src="script.js"': 'src="{{ script_js_url }}"',
}


def convert_file(folder_path: pathlib.Path):
    # Convert index.html
    html_file = folder_path / "index.html"
    if not html_file.exists():
        raise FileNotFoundError("No index.html found")

    content = html_file.read_text(encoding="utf-8")
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)

    (folder_path / ".auth").touch()

    html_file.rename(folder_path / "index.jinja2").write_text(content, encoding="utf-8")


if __name__ == "__main__":
    convert_file(pathlib.Path("." if len(sys.argv) <= 1 else sys.argv[1]))
