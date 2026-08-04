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
- If `bundle` is not found (local gem path not in `PATH`), add it to your shell config (e.g. `~/.zshrc`):
  ```bash
  export PATH="$HOME/.local/share/gem/ruby/3.4.0/bin:$PATH"
  ```
  Then reload: `source ~/.zshrc`.

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

## Charts & interactive plots

All self-contained interactive charts (e.g., `assets/plots/*.html`) should follow the same aesthetic used in `diabetes_scatter.html`:

### Embedding in posts
Use a responsive wrapper so the iframe never creates extra whitespace on mobile:
```html
<div style="position: relative; width: 100%; aspect-ratio: 4 / 3; margin: 1.5em auto;">
  <iframe src="/assets/plots/CHART_NAME.html" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"></iframe>
</div>
```

### Chart styling standards
| Element | Rule |
|---------|------|
| **Container** | `width: 100%; height: 100%` (fills the iframe wrapper) |
| **Canvas** | Scale to container size; use `devicePixelRatio` for sharp rendering on retina screens |
| **Background** | `#ffffff` (white) |
| **Grid** | `#e5e5e5`, 1 px line |
| **Axis lines** | `#444444`, 1.5 px |
| **Axis labels** | `#444444`, proportional font (`Math.max(10, width * 0.015)`) |
| **Axis titles** | `#333333`, proportional font (`Math.max(11, width * 0.018)`) |
| **Chart title** | `#333333`, bold, proportional font (`Math.max(13, width * 0.02)`) |
| **Point radius** | Proportional: `Math.max(2.5, width * 0.005)` |
| **Point opacity** | `0.7` (use `ctx.globalAlpha`) |
| **Colors** | Blue `#1f77b4` (negative class), Red `#d62728` (positive class) — keep consistent for binary classification |
| **Legend** | White background with `#cccccc` border, placed top-right inside the plot area |
| **Tooltip** | White bg, `#cccccc` border, `box-shadow: 0 2px 6px rgba(0,0,0,0.15)`, 12 px font, follows cursor on desktop, appears on touch for mobile |
| **Margins** | Proportional to canvas size (≈ 10% top/bottom, 5–10% sides) |

### Axis ticks (nice numbers)
Never divide a range into equal fractional steps. Use a `niceTicks(min, max, count)` helper that rounds the step to the nearest power-of-ten multiple of **1, 2, 5, or 10**, then rounds `min` down and `max` up to that step. Example:
```javascript
function niceTicks(min, max, count) {
  const span = max - min;
  const step = span / count;
  const mag = Math.pow(10, Math.floor(Math.log10(step)));
  const err = step / mag;
  let niceStep;
  if (err <= 1) niceStep = mag;
  else if (err <= 2) niceStep = 2 * mag;
  else if (err <= 5) niceStep = 5 * mag;
  else niceStep = 10 * mag;
  const niceMin = Math.floor(min / niceStep) * niceStep;
  const niceMax = Math.ceil(max / niceStep) * niceStep;
  const ticks = [];
  for (let v = niceMin; v <= niceMax + niceStep * 0.001; v += niceStep) {
    ticks.push(parseFloat(v.toPrecision(12)));
  }
  return { min: niceMin, max: niceMax, step: niceStep, ticks };
}
```
- X-axis (integer data): `Math.round(val)` labels
- Y-axis (decimal data): `val.toFixed(1)` labels

### Interactivity
- **Desktop:** `mousemove` hover with 8 px detection radius
- **Mobile:** `touchstart` with larger 12 px radius; tooltip hides after 1.5 s on `touchend`
- Always redraw on `window.resize`

## Responsive images in posts

Images inserted in posts must be responsive and use CSS classes to control width on desktop vs mobile. Define the styles once per post with a `<style>` block and reuse the classes.

### Size classes

| Class | Desktop (> 768 px) | Mobile (<= 768 px) | Use case |
|-------|---------------------|--------------------|----------|
| `.diagram-75` | 75 % | 100 % | **Default for graphs, charts and educational images** (e.g. sigmoid plot, cross-entropy diagram). |
| `.responsive-diagram` | 50 % | 100 % | Smaller diagrams or secondary images (e.g. compact neural-network illustration). |

### Markup pattern

```html
<div style="margin: 1.5em auto;">
  <img class="diagram-75" src="/assets/img/..." alt="..." style="height: auto; display: block; margin: 0 auto;" />
</div>
```

Place the shared styles once per post (usually after the first image that needs them):

```html
<style>
  .diagram-75 { width: 75%; }
  .responsive-diagram { width: 50%; }
  @media (max-width: 768px) {
    .diagram-75 { width: 100%; }
    .responsive-diagram { width: 100%; }
  }
</style>
```

> When in doubt, default to `.diagram-75` for any graph, plot or image that needs to be easily readable. Reserve `.responsive-diagram` only when the image is intentionally small.

## Formatting & editor conventions

- EditorConfig: 2-space indent, LF endings.
- `*.html` is treated as Liquid in VS Code (`files.associations` in `.vscode/settings.json`).
- YAML (`_config.yml`, data files): use double quotes. JS/CSS/SCSS: single quotes.
- Markdown files: **do not trim trailing whitespace** (`trim_trailing_whitespace = false`).

## Calculator key notation

When writing tutorials or instructions involving calculator keys (e.g., HP-12C), always use the `<kbd>` HTML tag to render keys as button-like elements. Highlight prefix keys <kbd>f</kbd> and <kbd>g</kbd> separately when applicable.
