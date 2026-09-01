# Portfolio Site — Deployment Guide

## 1. Push to GitHub
```bash
cd task1-portfolio
git init
git add .
git commit -m "Initial portfolio site"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## 2. Enable GitHub Pages
1. Open the repo on GitHub → **Settings** → **Pages**.
2. Under "Build and deployment", set **Source** to `Deploy from a branch`.
3. Branch: `main`, folder: `/ (root)`. Save.
4. Wait 1–2 minutes, then visit `https://<your-username>.github.io/<your-repo>/`.

## 3. Test across browsers
Open the live URL in Chrome, Firefox, and Edge/Safari. Use each browser's
device toolbar (F12 → toggle device toolbar) to check the mobile layout —
the site is responsive from ~360px wide.

## 4. (Bonus) Custom domain
1. Get a free subdomain (e.g. from [is-a.dev](https://www.is-a.dev/) or a free DNS provider).
2. Add a file named `CNAME` (no extension) to the repo root containing just your domain, e.g.:
   ```
   yourname.is-a.dev
   ```
3. At your DNS provider, add a CNAME record pointing your subdomain to
   `<your-username>.github.io`.
4. Back in GitHub Pages settings, enter the custom domain and enable
   "Enforce HTTPS" once it's verified.

## Personalize before deploying
- Replace `you@example.com`, the GitHub link, and the LinkedIn link in `index.html`.
- Swap in real project links once repos are public.
