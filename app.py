from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_file,
    Response
)

from pathlib import Path
from email.message import EmailMessage
import os
import smtplib
import threading
import webbrowser
from urllib.parse import quote_plus


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)

# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent


def load_local_environment():
    """Load local settings from .env without overwriting existing variables."""
    env_path = BASE_DIR / ".env"
    if not env_path.is_file():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


load_local_environment()

app.secret_key = os.environ.get("SECRET_KEY", "dev-portfolio-secret-key")


PROJECT_POSTERS = (
    "credit-card-fraud-detection",
    "customer-segmentation",
    "sentiment-analysis",
    "titanic-survival-prediction",
    "on-demand",
    "deepfake-video-generation",
)


@app.context_processor
def inject_site_settings():
    """Expose safe site settings and optional local assets to templates."""
    base_url = os.environ.get("SITE_URL", request.url_root).rstrip("/")
    whatsapp_number = "".join(
        character for character in os.environ.get("WHATSAPP_NUMBER", "")
        if character.isdigit()
    )
    whatsapp_url = ""
    if whatsapp_number:
        message = quote_plus("Hello Sohaib, I found your portfolio and would like to connect.")
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message}"

    poster_urls = {}
    for project_slug in PROJECT_POSTERS:
        poster_path = BASE_DIR / "static" / "images" / "project-posters" / f"{project_slug}.jpg"
        filename = (
            f"images/project-posters/{project_slug}.jpg"
            if poster_path.is_file()
            else "images/project-poster-placeholder.svg"
        )
        poster_urls[project_slug] = url_for("static", filename=filename)

    return {
        "canonical_url": f"{base_url}{request.path}",
        "og_image_url": f"{base_url}{url_for('static', filename='images/og-image.svg')}",
        "whatsapp_url": whatsapp_url,
        "profile_image_exists": (BASE_DIR / "static" / "images" / "profile.jpg").is_file(),
        "project_posters": poster_urls,
    }


def send_contact_email(name, visitor_email, subject, message):
    """Send a contact-form notification through the configured SMTP account."""
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_username = os.environ.get("SMTP_USERNAME", "").strip()
    smtp_password = os.environ.get("SMTP_PASSWORD", "").strip()
    recipient = os.environ.get("CONTACT_EMAIL", smtp_username).strip()

    if smtp_host == "smtp.gmail.com":
        smtp_password = smtp_password.replace(" ", "")

    if not smtp_username or not smtp_password or not recipient:
        raise RuntimeError(
            "Email is not configured. Set SMTP_USERNAME, SMTP_PASSWORD, "
            "and CONTACT_EMAIL."
        )

    email = EmailMessage()
    email["From"] = smtp_username
    email["To"] = recipient
    email["Reply-To"] = visitor_email
    email["Subject"] = f"Portfolio contact: {subject or 'New message'}"
    email.set_content(
        f"Someone submitted your portfolio contact form.\n\n"
        f"Name: {name}\n"
        f"Email: {visitor_email}\n"
        f"Subject: {subject or 'Not provided'}\n\n"
        f"Message:\n{message}\n"
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(email)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# PROJECTS
# ==========================================

@app.route("/projects")
def projects():
    return render_template("projects.html")


# ==========================================
# CERTIFICATES
# ==========================================

@app.route("/certificates")
def certificates():
    return render_template("certificates.html")


# ==========================================
# CONTACT FORM
# ==========================================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        honeypot = request.form.get("website", "").strip()

        # Bots often complete hidden fields that human visitors never see.
        if honeypot:
            flash("Thank you! Your message has been sent successfully.", "success")
            return redirect(url_for("contact"))


        # -------------------------------
        # FORM VALIDATION
        # -------------------------------

        if not name or not email or not message:

            flash(
                "Please fill in all required fields.",
                "error"
            )

            return redirect(url_for("contact"))


        # Send the message to the portfolio owner's inbox.
        try:
            send_contact_email(name, email, subject, message)
        except (OSError, RuntimeError, smtplib.SMTPException, ValueError):
            app.logger.exception("Contact email could not be sent")
            flash(
                "Sorry, your message could not be sent right now. Please try again later.",
                "error"
            )
            return redirect(url_for("contact"))


        # -------------------------------
        # SUCCESS MESSAGE
        # -------------------------------

        flash(
            "Thank you! Your message has been sent successfully.",
            "success"
        )

        return redirect(url_for("contact"))


    return render_template("contact.html")


# ==========================================
# RESUME DOWNLOAD
# ==========================================

@app.route("/download-resume")
def download_resume():

    resume_path = (
        BASE_DIR
        / "static"
        / "files"
        / "Sohaib_Khan_CV.pdf"
    )


    # Check whether resume exists

    if resume_path.exists():

        return send_file(
            resume_path,
            as_attachment=True,
            download_name="Sohaib_Khan_CV.pdf"
        )


    # Resume not found

    flash(
        "Resume file is not available yet.",
        "error"
    )

    return redirect(url_for("home"))


# ==========================================
# 404 ERROR PAGE
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.route("/sitemap.xml")
def sitemap():
    base_url = os.environ.get("SITE_URL", request.url_root).rstrip("/")
    routes = ("/", "/about", "/projects", "/certificates", "/contact")
    urls = "".join(f"<url><loc>{base_url}{route}</loc></url>" for route in routes)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(xml, mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    base_url = os.environ.get("SITE_URL", request.url_root).rstrip("/")
    return Response(f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n", mimetype="text/plain")


# ==========================================
# RUN APPLICATION
# ==========================================

def open_in_browser():
    """Open the local website in Chrome, falling back to the default browser."""
    url = "http://127.0.0.1:5000"
    chrome_locations = (
        Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe",
    )

    for chrome_path in chrome_locations:
        if chrome_path.is_file():
            webbrowser.BackgroundBrowser(str(chrome_path)).open(url)
            return

    webbrowser.open(url)


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"

    # In debug mode, only the reloader's child process should launch a browser.
    if not debug_mode or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.0, open_in_browser).start()

    app.run(debug=debug_mode)
