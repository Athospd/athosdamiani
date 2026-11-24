# athosdamiani: personal site and blog (Quarto)

Live at https://athospd.github.io/athosdamiani/. The owner is Athos Damiani, a data scientist with a statistics background and data engineering experience. The audience is recruiters and R/data people.

## Publishing: a push to `main` is a live deploy

- `.github/workflows/publish.yml` renders the site and pushes it to `gh-pages` on every push to `main`. A second run, "pages build and deployment", then serves it. The whole thing takes about 3 minutes.
- Before you commit, render locally: `quarto render <file>`. Also run `quarto render blog.qmd index.qmd` when the post listings change. Check `_site/` for the result, for example with grep. `_site/` is gitignored.
- **Commit `_freeze/`.** `freeze: auto` re-runs a post's code only when its source changes. CI uses the frozen results and only has the packages listed in `publish.yml` and `requirements.txt`. If a post's code changed and its freeze isn't committed, CI fails.
- Commit to `main` directly, one commit per logical change. Message style: `Area: what changed`, for example `Projects: link the targetfy video` or `targetfy post: use the real tar_glimpse() graph…`.
- After pushing, check the deploy:
  - `gh run list -L 3` shows both runs as `success`.
  - `curl -s https://athospd.github.io/athosdamiani/<page>.html | grep -o '<new text>'` confirms the change is live.
  - Only report "live" after that check passes.
  - Wait with an `until` loop, because `sleep` is blocked. Match the run to your commit: `H=$(git rev-parse HEAD); until id=$(gh run list -R Athospd/athosdamiani -w publish.yml -L 1 --json databaseId,headSha -q ".[] | select(.headSha==\"$H\") | .databaseId") && [ -n "$id" ]; do :; done; gh run watch $id -R Athospd/athosdamiani --exit-status`. Then loop on `curl` until the new text appears.
- GitHub Pages sends `Cache-Control: max-age=600`. If the owner still sees an old version after the live check passes, it's their browser cache: tell them to hard-refresh.

## Writing a post

- Each post gets its own folder: `posts/YYYY-MM-DD-slug/index.qmd`. Legacy posts are `index.Rmd`, so keep them as `.Rmd`.
- Front matter: `title`, `description` (one line, shown in listings and previews), `date`, `author: "Athos Damiani"`, `categories` (lowercase, reuse existing ones such as `r`, `targets`, `claude code`, `ai`), and `image:` (the thumbnail). Python posts add `jupyter: python3`. Add `execute: warning: false` when "built under R version" noise appears.
- Voice is first person, plain and concrete. State facts. No self-praise ("reliable", "powerful", "best-known") and no hype. Say what the thing does, why the owner built it, and how to try it, with short paragraphs and real code or output. A new project post links its GitHub repo, and the Projects page links back to it.
- Use real artifacts, never mock-ups. Example: the targetfy post shows the actual `tar_glimpse()` graph from running the pipeline.
- Run code that the post shows but doesn't execute (an ```` ```r ```` block in a `.qmd`, a generated `_targets.R`) in a scratchpad project before publishing, so what readers copy works.
- Check every version, date or ranking claim against its source (package NEWS, CRAN, cranlogs) before publishing. Earlier drafts got "added in purrr 1.0" (it was 1.1) wrong this way.
- A post based on a LinkedIn post or a gist links both in its opening paragraph.
- Helper files for a post (generator scripts, intermediate images) go in the post folder with a `_` prefix (`_make_thumb.py`, `_glimpse.R`). Quarto doesn't publish them, and they keep the image reproducible. Start each script with a comment that says how to regenerate the image.
- Check the rendered output: `grep -lE '## Warning|## Error' _site/posts/*/index.html` should print nothing.

## Thumbnails

- 1600×900 PNG, named in `image:`. It's shown at the top of the post (`![](file.png)`) and in the cards view, RSS and social previews.
- Match the site's look: a dark background (`#0b0d10`) with a faint dot grid, and panels in `#12161b` with 4px solid "pixel ring" borders, a hard drop shadow and three square window dots. Accent colours are mint `#6ee7a0`, amber `#f2b84b`, pink `#ff7eb6`, sky `#6cc4ff` and lilac `#b69cff`. Fonts: Silkscreen for the title, IBM Plex Mono for everything else. No rounded corners.
- Method: a Python script writes `_thumb.html` (an inline SVG with `shape-rendering="crispEdges"` and Google Fonts with `display=block`). Then screenshot it with headless Chrome:
  `"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --hide-scrollbars --window-size=1600,900 --virtual-time-budget=6000 --screenshot=<out>.png _thumb.html`.
  Look at the PNG with Read before using it. Model to copy: `posts/2026-11-21-targetfy/_make_thumb.py`.
- Real R output in an image (a `tar_glimpse()` graph, an htmlwidget): save it with `htmlwidgets::saveWidget(..., selfcontained = FALSE)`, screenshot it with `--force-device-scale-factor=2`, crop it to its content with PIL, and embed the PNG in the SVG as base64. See `posts/2026-11-21-targetfy/_glimpse.R`.
- Before using a PNG, check that no text overflows a panel or runs into a border, and that arrows read as arrows.
- Headless Edge is unreliable on this machine. Use Chrome.

## Site pages

- `projects.qmd`: a definition list per section. Each entry is `**[name](repo)**` followed by a `: description` line. Keep descriptions **under 300 characters**. Put extra links, such as a video or a post, at the end of the description line (`[▶ Watch the video](…)`).
- `blog.qmd`: the listing of `posts/` (search, sort, a list/cards switch). `index.qmd`: home, which lists all posts.
- Theme profile is `pixel` (`_quarto.yml` → `_quarto-pixel.yml`). CSS is in `theme/pixel.scss`, and palettes are in `theme/pixel-dark.scss` and `theme/pixel-light.scss`. `h2` headings get automatic `01/02…` numbers.
- Design rules: professional, not childish. Keep it compact. The pixel font is for tiny labels only. Borders are 2px pixel rings, dividers are dashed, and there are no rounded corners.
- `_quarto.yml` includes GoatCounter and the Search Console verification meta tag. Don't remove them.
- `https://athospd.github.io/` is a separate repo, `Athospd/Athospd.github.io` (branch `master`). Its `index.html` redirects to this site, and its `robots.txt` points crawlers to `athosdamiani/sitemap.xml`.
- Check layout changes on a phone width. Headless Chrome won't go below about 500px, so screenshot a page that holds the site in a `<iframe width=390>`, with `--allow-file-access-from-files`.

## Environment gotchas (Windows)

- Quarto: `export PATH="/c/Users/ap_da/AppData/Local/Programs/Quarto/bin:$PATH"` in bash. Quarto uses **R 4.4.1**, and only that version has the post packages.
- `Rscript` isn't on the bash PATH. Use `"/c/Program Files/R/R-4.4.1/bin/Rscript.exe"`.
- When you write LaTeX or regexes through Python or a heredoc, use raw strings. In a normal Python string, `"\text"` becomes a TAB followed by `ext`, which once broke an equation on the live site.
- Never `cd` into `_site`. It locks the folder, and the next render fails with "file in use".
- The tabulizer post needs Java 11 to re-render. Its output is frozen, so a normal render doesn't need Java.
- `_HANDOFF*.md` files at the root are local, gitignored history notes from earlier sessions. Read them for background, and don't commit them.
