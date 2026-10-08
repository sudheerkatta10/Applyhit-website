# ApplyHit website

Landing page for **ApplyHit** — IT job applications and candidate marketing. *Aim. Apply. Hit.*

A single static page: plain HTML, CSS and JavaScript with no build step and no dependencies.

## Project structure

```
public/                    ← the website (deploy this folder only)
├── index.html             page, styles and scripts
└── brand_assets/
    ├── applyhit-icon.png  logo used on the page
    ├── apple-touch-icon.png
    ├── favicon-32.png
    └── favicon-64.png
serve.mjs                  local preview server
tools/make_logo_assets.py  regenerates the logo files from the original artwork
```

## Run it locally

Requires [Node.js](https://nodejs.org/) 18 or newer.

```bash
node serve.mjs
```

Then open http://localhost:3000. Set `PORT=8080 node serve.mjs` to use a different port.

## Deploy

Upload or publish the **`public/`** folder to any static host (GitHub Pages, Netlify, Vercel, Cloudflare Pages, or a regular web server). `public/index.html` is the home page; nothing needs to be built.

## Contact form

The "Send a request" form sends submissions to **applyhit01@gmail.com** through [FormSubmit](https://formsubmit.co/) — no server or account needed.

- FormSubmit only delivers after the inbox owner clicks the **Activate Form** link it emails on first use. If the site moves to a new domain, it may ask to activate again.
- If FormSubmit can't be reached, the form opens the visitor's email app with their message pre-filled, addressed to the same inbox.
- To change the receiving address, update `TO` in the form script and the form's `action` in `public/index.html`.

## Editing content

- **Hero slider:** in `public/index.html`, find the `HERO SLIDER` comment. Each `<article class="slide">` is one slide; copy a whole block to add another. Dots and arrows update automatically.
- **Colours and fonts:** the `:root` variables at the top of the `<style>` block.
- The dashboard cards and application tables show **sample data** (fictional companies) for illustration.

## Regenerate the logo files

Needs Python 3 and Pillow (`pip install pillow`):

```bash
python tools/make_logo_assets.py "path/to/Actual Logo.jpeg" public/brand_assets
```

The script removes the plain background, crops, and writes small compressed PNGs (page logo, favicons and iOS home-screen icon).
