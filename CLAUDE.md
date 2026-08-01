# Voymark website — working notes for Claude

Presentation site for the Voymark iOS app (repo: outsidesoftwaresrl/Voymark).

## Conventions

- **Pure static** — HTML/CSS, no framework, no npm. Deployed by
  `.github/workflows/pages.yml` (GitHub Pages, Linux, cheap) on every push
  to `main`. No CI-approval dance here — that rule is for the app repo's
  macOS minutes only.
- **Pages are GENERATED** — all six `index.html` files (root EN + fr/ es/
  it/ de/ ro/) come from `scripts/build_i18n.py`, which holds the template
  and every translation. NEVER edit the HTML directly: edit the script,
  run `python3 scripts/build_i18n.py` from the repo root, and commit the
  regenerated pages together with the script. Copy changes must land in
  all six languages (same parity rule as the app).
- **Two domains, one build.** The same files are served from `voymark.app`
  (via `CNAME`) and from the GitHub Pages project URL
  `outsidesoftwaresrl.github.io/Voymark-website/`. So:
  - **Anything a person clicks is relative** — language switcher, footer
    nav, the subpage home link, in-copy cross-links. Use `rel_url()`.
    Absolute hrefs bounced a visitor testing the Pages copy onto the apex
    domain mid-visit; root-relative (`/fr/...`) breaks under the Pages
    path prefix.
  - **Anything a crawler reads is absolute and names `voymark.app`** —
    `rel=canonical`, `og:url`, `hreflang`, JSON-LD `@id`/`url`,
    `sitemap.xml`. That is what stops the Pages copy competing with the
    apex domain as a duplicate. All built from `BASE_URL`.
  Verify after touching navigation: serve the repo under a
  `/Voymark-website/` path prefix and crawl it — no link may leave the
  prefix.
- Company name is **Outside Software SRL** (footer, legal mentions).
- **Brand tokens** live in `assets/style.css` as CSS variables and MUST stay
  in lockstep with the app's `Voymark/DesignSystem/Theme.swift`
  (light + dark hex values, Marcellus display font, IBM Plex Mono).
- Work directly on `main`, push with `git push -u origin main`.
- Copy tone: the app is a passport. Say "stamps", "passport", "mark".
  Tagline: "Every journey leaves a mark."
- Never claim features the app doesn't have; the source of truth is the app
  repo's `docs/FEATURES.md`.
- The site stays honest about privacy: offline-first, on-device photo
  scanning, no accounts/tracking/ads, free.
