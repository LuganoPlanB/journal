# Example site

A small, fictional conference website built on
[conference-theme](https://github.com/IAQI/conference-theme). All people,
papers and places are made up. Copy this folder to start a new site; see the
fork's [upstream program guide](../CONFERENCE.md). The [journal starter](../journalSite/) is the entry point for Plan-B Journal.

To run it inside the theme's repository:

```sh
npm install
hugo server
```

The build warns that the current year still shows stand-in images; that is
expected here. In your own site, set `[params.YEAR.logos]` in `hugo.toml`.
