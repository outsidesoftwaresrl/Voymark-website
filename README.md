# Voymark website

Presentation site for [Voymark](https://github.com/outsidesoftwaresrl/Voymark) —
the world-passport travel app. *Every journey leaves a mark.*

## Stack

Pure static HTML/CSS. No framework, no build step.

- `index.html` — the landing page
- `assets/style.css` — brand tokens (mirrors the app's `Theme.swift`, light + dark)
- `.github/workflows/pages.yml` — deploys `main` to GitHub Pages

## Deploying

Enable Pages once in **Settings → Pages → Source: GitHub Actions**.
After that, every push to `main` deploys automatically.
