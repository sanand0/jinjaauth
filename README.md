# Jinja Auth

This app converts static HTML files into Jinja templates that can only be accessed via Google auth by specific users. This improves compliance with security requirements.

## Conversion

```bash
uv run convert.py [FOLDER]
```

If the folder has an `index.html`, it renames it to `index.jinja2` and, inside the file:

- Replaces `https://cdn.jsdelivr.net/npm/bootstrap@5.*?/dist/css/bootstrap.min.css` with `{{ bootstrap5_css_url }}`
- Replaces `https://cdn.jsdelivr.net/npm/bootstrap@5.*?/dist/js/bootstrap.bundle.min.js` with `{{ bootstrap5_js_url }}`
- Replaces `src="script.js"` with `{{ script_js_url }}`

## Server

1. Create OAuth credentials at [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Set authorized redirect URI to `http://localhost:8000/googleauth/`
   - If you're deploying at `https://yourdomain.com/`, add `https://yourdomain.com/googleauth/`
2. In the folder where you want to serve files, create a `.env` file with the following variables.
   (Or set them as environment variables.) This is typically done using CI/CD pipelines.
   You can also specify a `.auth` with 1 line per email.

   ```env
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   REDIRECT_URI=http://localhost:8000/googleauth/
   PORT=8000  # Optional, defaults to 8000
   AUTH=user1@example.com,user2@example.com
   ```

3. Run the server:

   ```bash
   uv run app.py
   ```

This [`app.py`](app.py) is based on [staticauth](https://github.com/sanand0/staticauth) but

1. Renders `.jinja2` files as Jinja2 templates, passing the [conversion](#conversion) variables
2. Wildcard email IDs are not allowed in .auth / AUTH
