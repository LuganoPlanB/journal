# Maintaining Plan-B Journal

This repository publishes a static Hugo journal at [plan-b.foundation/journal](https://plan-b.foundation/journal/). Authors submit and editors review in a separate HotCRP installation. Editors choose when to transfer accepted results to this public repository.

## Where to work

| Change | Source |
| --- | --- |
| Hero introduction and Topics | `journalSite/content/_index.md`. The description supplies the introduction. Each `###` heading and paragraph in the body supplies one topic and brief. |
| Call for Papers and submission instructions | `journalSite/content/call-for-papers.md` and `journalSite/content/authors.md`. Set `params.hotcrpURL` in `journalSite/hugo.toml` when the public submission URL is confirmed. |
| Committee, News and About | `journalSite/content/people/`, `news/` and `about/` under the same content root. Committee retains its original `/people/` route. |
| Navigation | `[[menus.main]]` entries in `journalSite/hugo.toml` drive desktop navigation, the mobile menu and the homepage directory. Journal club has no entry. |
| Appearance | Read [DESIGN.md](DESIGN.md) before changing journal layouts or `assets/journal/`. Keep public links valid under the `/journal/` base path. |

Use `journalSite/` for the published site. The inherited `exampleSite/` exercises conference compatibility. Its schedules, sessions and posters are documented in [CONFERENCE.md](CONFERENCE.md).

## When editorial results are ready

The **Issues archive already exists** at `/journal/issues/` and the Call for Papers page links to it. Publishing an issue requires data and an issue entry. Making Issues a top-level section is a separate editorial choice.

1. **Export privately.** In HotCRP, select the intended issue’s submissions and export paper information as JSON with decision labels. Save the raw file outside the checkout or in the ignored `journalSite/private_data/` directory. Confirm which decisions and manuscripts the editors have cleared for public release. A Hugo draft in a public Git repository is still readable on GitHub.
2. **Filter the export.** From the repository root, run the following with the actual issue key and decision label. The example matches the complete label “Accept”. The sanitizer uses a case-insensitive regular expression.

   ```sh
   cd journalSite
   python3 ../scripts/sanitize_hotcrp_json.py private_data/export.json \
     --decision '^Accept$' -o data/accepted-papers-vol-1-issue-1.json
   ```

   Compare the output count and paper IDs with the editor-approved list. Inspect titles, abstracts and author details before staging. The default allowlist strips emails, reviews, conflicts and decision text. Keep that allowlist for routine imports. For corrections, re-export the **complete intended issue** and review the diff: the command replaces the output file, including records omitted from the new export.
3. **Register the issue.** From here, paths are relative to `journalSite/`. Add an entry to `data/issues.yaml`, newest first. Match the key to the suffix of `accepted-papers-<key>.json`. Use the optional `date` field for the editorially confirmed publication date in `YYYY-MM-DD` format.

   ```yaml
   - key: vol-1-issue-1
     title: Volume 1, Issue 1
     draft: true
   ```

   Keep the key and each HotCRP `pid` stable after publication. IDs may repeat across issues. The `content/issues/_content.gotmpl` adapter generates the table of contents in export order, an article at `issues/<key>/<pid>/`, and `issues/<key>/papers.json`. The public sample uses `example: true` for fictional content and is excluded from the article feed. Omit that flag for real results.
4. **Attach approved files.** Put a full-text PDF at `assets/articles/<key>/<pid>.pdf`. For DOIs, add `data/proceedings-<key>.yml` with quoted paper IDs as keys and bare DOI strings as values. Check a generated article to verify the author order, affiliations, abstract and resource links.
5. **Preview and release.** Run `hugo server -D` from `journalSite/` to inspect a draft. When cleared, set `draft: false`, run a production build into a fresh directory, and check the archive, article, issue JSON and site RSS. Open a PR in `LuganoPlanB/journal` with the reviewed public files. Leave merging to the maintainer. The GitHub Pages workflow tests, builds and deploys changes merged into `main`.

To feature Issues in navigation as well, add the following alongside the existing menu entries in `journalSite/hugo.toml`. The same entry makes the archive visible in the homepage directory. The Call for Papers hero and editable Topics keep their own sources.

```toml
[[menus.main]]
  name = "Issues"
  pageRef = "/issues"
  weight = 15
```

## Checks

Use the Hugo and Dart Sass versions from [.github/workflows/check.yml](.github/workflows/check.yml). From the repository root, install the Python requirements and run:

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover tests
python3 -m unittest discover -s integration -v
(cd journalSite && hugo --panicOnWarning --destination "$(mktemp -d)")
```

The integration suite exercises a synthetic accepted/rejected import, publication links, draft visibility and private-field exclusion. Keep fixtures fictional. For changes to shared theme code, also build the conference fixture with its Node dependencies and Dart Sass as shown in the workflow. For visual changes, check the journal in a browser using the mobile and desktop cases in [DESIGN.md](DESIGN.md).
