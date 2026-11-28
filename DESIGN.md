---
name: Plan-B Journal
description: Editorial application of Lugano Plan B’s Civic Digital Commons identity.
colors:
  canvas: "#fffefa"
  ink: "#030b20"
  navy: "#082952"
  panel: "#f3f8fd"
  sky: "#4f97e9"
  mist: "#b0d3f1"
  focus: "#7468ff"
typography:
  display:
    fontFamily: '"Inter", "Segoe UI", Arial, sans-serif'
    fontSize: "clamp(3rem, 6vw, 4.75rem)"
    fontWeight: 800
    lineHeight: 1.06
    letterSpacing: "-0.04em"
  body:
    fontFamily: '"Inter", "Segoe UI", Arial, sans-serif'
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  card: "12px"
  panel: "16px"
  pill: "999px"
spacing:
  section: "56px"
  grid: "16px"
  panel: "28px"
components:
  button-primary:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.canvas}"
    rounded: "{rounded.pill}"
    padding: "12px 22px"
---

# Design System: Plan-B Journal

## Overview

Readers come here to understand the call, scan research topics and read papers. Give a title, a byline and an abstract enough space to do that work. The journal inherits Civic Digital Commons from the [Plan B brand guide](https://github.com/LuganoPlanB/branding/blob/ba333c6e21483e2606983bb733942812e0b35aad/DESIGN.md). Its local expression is a navy masthead, self-hosted Inter, warm reading surfaces and a photograph of Lake Lugano and Monte Brè.

For the implemented values, read [color tokens](assets/journal/tokens.css), [layout tokens](assets/journal/layout.css) and the [journal stylesheet](assets/journal/style.css). The frontmatter records the light scheme.

## Colors

Use civic ink for body text and navy for headings, links and primary actions. Pale blue panels distinguish the cover and directory from the warm canvas. The narrow multicolor band beneath the header is the page’s single bright accent. Keep type on solid surfaces.

Respect the reader’s system color preference. Dark mode uses charcoal canvas (`#171717`), a warm dark panel (`#292424`) and white text. The logo ground stays navy in both schemes because the original color artwork contains white lettering. Preserve its original proportions and SVG bytes.

## Typography

Use the bundled variable Inter face with the fallback stack above. Display headings use weight 800 and tight tracking. Article titles can wrap naturally across lines. Keep the abstract at body size with generous leading, and use the secondary text color for affiliations and short topic briefs. Preserve heading order: the homepage title is H1, Topics is H2 and each editable topic is H3.

## Layout

The outer shell is at most 1180px wide with fluid side gutters. Interior pages narrow to 56rem and paragraphs stop at 70ch. The homepage pairs masthead copy and photography, followed by a two-column Topics section and the section directory. Keep that order when content grows.

| Viewport width | Layout change |
| --- | --- |
| 900px and below | Replace desktop links with the native Menu disclosure. Directory cards use two columns. |
| 700px and below | Stack the hero copy above the photograph. Stack Topics above the topic briefs. |
| 520px and below | Directory cards use one column. |

## Elevation & Depth

Use changes in surface color, spacing and thin dividers for grouping. Article metadata sits between horizontal rules. Topic titles have a rule above them. Directory cards use a tinted surface and a single link covering the card.

## Shapes

Use the card radius for directory entries and example notices, the larger panel radius around the combined hero, and pill ends for primary actions and the mobile Menu control. Keep the inner seam between the hero photograph and the text panel square at both orientations.

## Components

- **Header and menu.** Place the intact mark on the left. Desktop links sit on the right and underline the current location. On phones the Menu control occupies the opposite edge from the mark. Opening it reveals links in the header’s normal flow. Use the same Hugo menu for both layouts.
- **Homepage.** Call for Papers is the primary action. Keep Topics as a plain heading with Markdown-editable briefs alongside it. Use the directory for navigation to Committee, author guidance and the other configured sections.
- **Issues and articles.** An issue lists linked titles and authors in reading order. An article starts with its parent issue, title and byline, then the abstract and available resources. Use the primary pill for a full-text PDF. Keep the fictional example notice legible even when a reader arrives directly at an article.

## Do's and Don'ts

- Use the original lake photograph and Hugo’s responsive image sizes for the masthead. Give factual photography meaningful alternative text.
- Keep links distinguishable on keyboard focus, with a visible outline. Aim for a minimum 44px target on standalone controls.
- Check light and dark schemes on the homepage, a long article title and a schedule table. At 320px and 390px, verify that the logo and Menu have separate hit areas, the menu opens with keyboard and touch, and the page fits without horizontal scrolling. At desktop width, verify the full navigation and the side-by-side masthead.
