# Sohaib Khan Portfolio

## Local setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Set these values in `.env` before using the contact form or WhatsApp button:

```env
SECRET_KEY=use-a-long-random-value
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-google-app-password
CONTACT_EMAIL=your-email@gmail.com
WHATSAPP_NUMBER=923001234567
SITE_URL=https://your-domain.com
```

## Assets to add later

- Add project MP4 files to `static/videos/` using the names referenced in `templates/projects.html`.
- Add certificate JPG files to `static/images/certificates/`.
- Add an optional professional photo as `static/images/profile.jpg`; the About page will use it automatically.
- Add optional project posters to `static/images/project-posters/`. See that folder's README for filenames.

## Deployment

`render.yaml` and `Procfile` support Render or Railway deployment. Add the production environment values in the hosting dashboard, then set `SITE_URL` to your deployed custom domain.
