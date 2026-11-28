# Plan-B Journal

A Hugo theme and starter for publishing journal issues from HotCRP. Editors export publication-ready manuscripts, readers browse issues and articles, and authors follow the submission link to the journal’s existing HotCRP installation.

## Preview the journal

Install Hugo 0.170.0 or later and Go. From the root of this checkout, run:

```sh
cd journalSite
hugo server -D
```

Open the local address printed by Hugo. The public sample issue shows a table of contents, two fictional articles, a sample PDF and the issue’s JSON export. Its `example: true` flag labels the preview and excludes its articles from the publication feed and text indexes. Set `draft: true` on any issue to restrict it to a local `hugo server -D` build.

To edit Topics, open [the homepage Markdown](journalSite/content/_index.md). Use a `###` heading and a short paragraph for each topic. Rearrange the entries to change their display order. The hero introduction is in the same file’s `description` field. Edit the [Call for Papers page](journalSite/content/call-for-papers.md) to publish submission details.

In `journalSite/hugo.toml`, set `params.hotcrpURL` to your public HotCRP submission URL to enable the submission links. Edit `journalSite/content/authors.md` to supply author guidelines.

## Publish an issue

1. In HotCRP, export paper information as JSON for manuscripts cleared for public release. Keep the raw export outside the public repository or in the ignored `private_data/` directory. Drafts committed to a public repository are visible on GitHub.
2. From `journalSite/`, filter by the **exact decision label used by your editors**. For an installation whose decision is “Accept”, this command creates the public data file:

   ```sh
   python3 ../scripts/sanitize_hotcrp_json.py private_data/export.json \
     --decision '^Accept$' -o data/accepted-papers-vol-1-issue-1.json
   ```

   Compare the reported count with HotCRP and review the output before publishing. The sanitizer retains titles, abstracts, author names and affiliations, and supported public metadata. Emails, reviews, conflicts and decision text are excluded by default.
3. Add the issue at the top of `data/issues.yaml`. The key matches the export filename and forms part of the public URL. Keep it stable. For example:

   ```yaml
   - key: vol-1-issue-1
     title: Volume 1, Issue 1
     draft: true
   ```

   An optional `date` in `YYYY-MM-DD` format is displayed as the issue publication date. Articles appear in export order. HotCRP IDs are scoped to the issue, so two issues can have an article numbered 1.
4. To publish a full-text PDF, put the editor-approved file in `assets/articles/vol-1-issue-1/<pid>.pdf`. For DOIs, add an optional `data/proceedings-vol-1-issue-1.yml` mapping quoted paper IDs to DOI strings. Imported arXiv IDs, related paper IDs and optional recordings become article links.
5. Preview with `hugo server -D`. Set `draft: false` when the issue is ready and merge the changes into `main`. After the checks pass, GitHub Actions builds the journal using the Pages URL and deploys `journalSite/public/`. View the [public journal](https://plan-b.foundation/journal/) or [check the deployment](https://github.com/LuganoPlanB/journal/actions/workflows/check.yml). To republish the same revision, choose **Run workflow** on `main`.

The Call for Papers page links to the issue archive. Each issue exposes `/issues/<key>/papers.json` and `#paper-<pid>` anchors. Each article has its own URL at `/issues/<key>/<pid>/`. The site also publishes an article RSS feed, sitemap, structured metadata, and text indexes at `llms.txt` and `llms-full.txt`.

## Upstream features

The [original theme](https://github.com/IAQI/conference-theme) supplies the HotCRP sanitizer, paper metadata, optional schedules, sessions, posters, slides, recordings, JSON and calendar exports, and edition archiving. The [program guide](CONFERENCE.md) documents those tools and their year-based file conventions. The [conference fixture](exampleSite/) exercises them independently. When using a schedule alongside a journal issue, use the same year for the issue key and the program data.

## Design and licensing

The homepage photograph of Lake Lugano and Monte Brè comes from the [Vite theme’s image collection](https://github.com/LuganoPlanB/vite-theme/blob/78ef033/src/theme/assets/heroes/lago_e_bre.jpg). Hugo generates two JPEG sizes for the journal layout.

The journal uses the Civic Digital Commons palette, light and dark reading surfaces, Inter, and the original Plan B mark. Brand assets come from [LuganoPlanB/branding](https://github.com/LuganoPlanB/branding/tree/ba333c6e21483e2606983bb733942812e0b35aad), with publishing and shell references from [ghost-theme](https://github.com/LuganoPlanB/ghost-theme) and [vite-theme](https://github.com/LuganoPlanB/vite-theme). See the [upstream code license](LICENSE) and the [Inter font license](assets/journal/OFL.txt).

## Checks

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover tests
python3 -m unittest discover -s integration -v  # requires hugo and go on PATH
```
