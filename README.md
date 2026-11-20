# athospd.github.io

Personal site of Athos Damiani — built with [Quarto](https://quarto.org), R and Python.

```
_quarto.yml          site config (navbar, theme, links)
index.qmd            home page
resume.qmd           resume
projects.qmd         open-source projects
blog.qmd             blog listing (auto-lists everything in posts/)
posts/<date-slug>/index.qmd   one folder per post
theme/light.scss     simple light theme
theme/code-vibes.scss  dark "terminal" theme
.github/workflows/publish.yml  renders + deploys on every push to main
```

## One-time setup

1. Install [Quarto](https://quarto.org/docs/get-started/) (RStudio/Positron already bundle it).
2. Create a **public** GitHub repo named exactly `athospd.github.io` and push this folder to `main`:
   ```bash
   git init && git add . && git commit -m "first version"
   git branch -M main
   git remote add origin https://github.com/athospd/athospd.github.io.git
   git push -u origin main
   ```
3. Run once locally to create the `gh-pages` branch: `quarto publish gh-pages`
4. On GitHub: **Settings → Pages → Source: Deploy from a branch → `gh-pages` / root**.

Site goes live at **https://athospd.github.io**. Your existing `athospd.github.io/mestrado` keeps working.

## Writing a post

1. Create `posts/2026-12-01-my-post/index.qmd`:
   ````markdown
   ---
   title: "My post"
   description: "One line that shows up in the listing"
   date: 2026-12-01
   categories: [r, spark]
   ---

   Some text.

   ```{r}
   summary(cars)
   ```
   ````
   For a Python post add `jupyter: python3` to the header and use ```` ```{python} ```` chunks.
2. Preview: `quarto preview` (live reload in the browser).
3. `git add . && git commit -m "new post" && git push` — GitHub Actions renders and publishes.

**Tip:** run `quarto render` locally before pushing and commit the `_freeze/` folder. Then CI reuses your results and doesn't need to install every package. If CI must execute a post, add its R packages to `.github/workflows/publish.yml` and Python packages to `requirements.txt`.

Drafts: add `draft: true` to a post's header to hide it from the published site.

## Theme

The navbar has a light/dark toggle: **light** = simple, **dark** = "code vibes".
- Go full code-vibes only: in `_quarto.yml` replace the `theme:` block with `theme: [darkly, theme/code-vibes.scss]`.
- Change colours: edit the `$cv-*` variables at the top of `theme/code-vibes.scss`.
