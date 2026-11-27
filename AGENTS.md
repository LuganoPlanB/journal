# AGENTS.md: journal-theme

This fork publishes the Plan-B Journal. Start with README.md and journalSite/.
Use synthetic HotCRP exports for tests. Check the script suite, the publishing
integration tests, and the inherited exampleSite fixture before proposing a change.
Keep changes on a branch, open the pull request in LuganoPlanB/journal-theme,
and leave merging to a maintainer.

## Upstream maintenance notes

The notes below describe work in IAQI/conference-theme and its three consuming
sites. They are relevant when porting changes back to that project.

Instructions for AI coding assistants (Claude Code, Codex, Cursor, Copilot, ...)
working on this module, and a checklist for the humans supervising them.
`CLAUDE.md` imports this file; edit this one.

## What this is

The shared Hugo module behind three conference websites:

| site | repository | live |
|---|---|---|
| QCrypt | [IAQI/qcrypt-website](https://github.com/IAQI/qcrypt-website) | https://qcrypt.net |
| TQC | [IAQI/tqc-website](https://github.com/IAQI/tqc-website) | https://tqc-conference.org |
| QIP | [IAQI/qip-website](https://github.com/IAQI/qip-website) | https://qipconference.org |

It holds the layouts, styles (`assets/style/_theme.scss` and friends), shortcodes,
i18n, the schedule / session / accepted-papers templates, and the Python
scripts in `scripts/` (HotCRP export → data files → schedule → presenters →
videos, and `new_year.py`). Each site pins a commit of this module in its
`go.mod` / `go.sum` and keeps only content, data, colours, logos and a few
deliberate overrides (listed in each site's README and AGENTS.md).

Read before making changes:

- **README.md**: the program pipeline and how sites use the module.
- **docs/website-guide.md**: how to work on a site (for site maintainers).

## Commands

```bash
python3 -m unittest discover tests        # from the repository root
# preview a change in a site (sites cloned next to this repository):
cd ../qcrypt-website
HUGO_MODULE_REPLACEMENTS="github.com/IAQI/conference-theme -> ../conference-theme" hugo server
```

## Rules

1. **Every change reaches three sites.** Keep the module site-agnostic: no
   conference names, years, URLs or colours in layouts, styles or scripts.
   Site-specific values come from the site's `hugo.toml` params, `i18n/en.toml`
   or the CSS variables in its `theme-<year>.scss`. New behaviour is optional,
   with defaults that leave the existing sites unchanged, and is documented
   (the parameter table in README.md, or the guide).
2. **Check all three sites.** Before opening a pull request, build each site
   against your local module, without and with drafts:
   ```bash
   HUGO_MODULE_REPLACEMENTS="github.com/IAQI/conference-theme -> ../conference-theme" hugo --gc -d /tmp/<site>-new
   ```
   If the change is not meant to be visible, compare the HTML with a build
   against the pinned version. TQC and QIP override some styles and layouts:
   a fix there may not reach them, or may clash with their copy; say so in the
   pull request.
3. **Scripts:** `python3 -m unittest discover tests` must pass, and changes to a
   script come with a test. Scripts run from a site's root as
   `python3 ../conference-theme/scripts/<script>.py`, must work with Python 3.9,
   and may only depend on `requirements.txt`. They print what they wrote and
   what is left to do by hand; `--check` style dry runs are welcome.
4. **Never invent conference facts** in examples, defaults or generated pages:
   dates, venues, people and sponsors come from the organizers. Generated pages
   get "TBA" or `<!-- TODO: ... -->` and `draft: true`.
5. **Personal data:** HotCRP exports and registration lists contain personal
   data. Never commit them, put them in test fixtures or send them to an
   external service; tests use made-up names.
6. **Docs follow behaviour:** update README.md (pipeline, parameters) or
   docs/website-guide.md (site work) in the same pull request.
7. **Releasing to the sites:** a site only changes when its pin is updated.
   After a module pull request is merged, open a pull request in each site that
   needs it with `go get github.com/IAQI/conference-theme@<commit>` (`hugo mod
   get` fails here) and the updated `go.mod` / `go.sum`; its Netlify deploy
   preview shows the result. Netlify builds previews only for pull requests
   against `main`, so stacked pull requests get none.
   The tool versions (`HUGO_VERSION`, `DART_SASS_VERSION`, `GO_VERSION`) are set
   once in each site's `netlify.toml` and must be the same in all three sites;
   `min` in this module's `hugo.toml` follows `HUGO_VERSION`. Use the current
   Hugo API (`hugo.Data`, `site.Pages`, `.Type`), not deprecated calls.
8. **Git:** work on a branch and open a pull request; never push to `main` and
   leave merging to a human maintainer. Commit only the files you meant to
   change.
