"""Create a static GitHub Pages version of this Flask portfolio.

Run: python scripts/build_github_pages.py
The generated `docs` folder is the directory GitHub Pages should publish.
"""

from pathlib import Path
import shutil
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import app  # noqa: E402


OUTPUT_DIR = PROJECT_ROOT / "docs"
PAGES = {
    "/": "index.html",
    "/about": "about.html",
    "/projects": "projects.html",
    "/certificates": "certificates.html",
    "/contact": "contact.html",
}


def make_static(html: str) -> str:
    """Convert Flask-root URLs to paths that work under a GitHub Pages repo."""
    replacements = {
        'href="/static/': 'href="static/',
        'src="/static/': 'src="static/',
        'poster="/static/': 'poster="static/',
        'href="/about"': 'href="about.html"',
        'href="/projects"': 'href="projects.html"',
        'href="/certificates"': 'href="certificates.html"',
        'href="/contact"': 'href="contact.html"',
        'href="/download-resume"': 'href="static/files/Sohaib_Khan_CV.pdf" download',
        'href="/#skills"': 'href="index.html#skills"',
        'href="/"': 'href="index.html"',
        'action="/contact"': 'action="https://formsubmit.co/"',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    # The Flask email route is not available on static hosting.  Keep the form
    # visible, but direct visitors toward the working WhatsApp contact option.
    html = html.replace(
        'action="https://formsubmit.co/"',
        'action="#" onsubmit="alert(\'Please use the WhatsApp button to contact me.\'); return false;"',
    )
    return html


def main() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    shutil.copytree(PROJECT_ROOT / "static", OUTPUT_DIR / "static")

    client = app.test_client()
    for route, filename in PAGES.items():
        response = client.get(route)
        if response.status_code != 200:
            raise RuntimeError(f"Could not build {route}: HTTP {response.status_code}")
        (OUTPUT_DIR / filename).write_text(
            make_static(response.get_data(as_text=True)), encoding="utf-8"
        )

    (OUTPUT_DIR / ".nojekyll").touch()
    (OUTPUT_DIR / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    print("GitHub Pages files created in docs/")


if __name__ == "__main__":
    main()
