# AGENTS.md — giuliovalcanaia.github.io

Personal blog on GitHub Pages using Jekyll + [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) v7.6 (via `chirpy-starter`).

## Build & deploy

- **Do not rely on GitHub Pages' native Jekyll builder.** The repo contains an empty `.nojekyll` file and deploys via `.github/workflows/pages-deploy.yml` (GitHub Actions → upload-pages-artifact → deploy-pages).
- CI triggers on push to `main` or `master`.
- CI builds with `JEKYLL_ENV=production bundle exec jekyll b` and runs `htmlproofer` with `--disable-external`.

## Local development

| Task | Command |
|------|---------|
| Dev server (live reload) | `bash tools/run.sh` |
| Production build + link check | `bash tools/test.sh` |
| Production mode server | `bash tools/run.sh -p` |

- `tools/run.sh` binds to `127.0.0.1` by default; use `-H 0.0.0.0` for container/network access.
- `tools/test.sh` outputs to `_site` and runs `htmlproofer`.

## Creating posts

Use the custom helper to get the correct filename and front matter:

```bash
bash script.sh "Título do post"
```

This creates `_posts/YYYY-MM-DD-<slug>.md` with minimal front matter. If you create posts manually, the filename **must** be `YYYY-MM-DD-<slug>.md` or Jekyll will ignore it.

## Site-specific quirks

- **Language & timezone**: `lang: pt-BR`, `timezone: America/Sao_Paulo`. Date formatting and locale-aware features follow this.
- **`last_modified_at` is set from git history**: `_plugins/posts-lastmod-hook.rb` runs `git log` on each post file and populates `last_modified_at` only if the file has **more than one commit**. Do not expect this field to appear on brand-new posts until they are committed at least twice.
- **Git submodule `assets/lib`**: Points to `chirpy-static-assets` but is **not initialized** in CI (commented out in workflow) and the local directory is empty. Do not initialize it unless you are intentionally switching to self-hosted assets (`assets.self_host.enabled`). The theme works without it (uses gem/CDN assets).
- **Ruby version in CI**: 3.4. `Gemfile.lock` is gitignored; CI uses `bundler-cache: true`.
- **Math (MathJax) is opt-in per post**: Add `math: true` to a post's front matter or formulas won't render. Block math requires blank lines before and after `$$`; inline math in lists must escape the first `$` as `\$$`.

## Formatting & editor conventions

- EditorConfig: 2-space indent, LF endings.
- `*.html` is treated as Liquid in VS Code (`files.associations` in `.vscode/settings.json`).
- YAML (`_config.yml`, data files): use double quotes. JS/CSS/SCSS: single quotes.
- Markdown files: **do not trim trailing whitespace** (`trim_trailing_whitespace = false`).
