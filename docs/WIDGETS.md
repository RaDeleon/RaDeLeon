# Profile presentation and widgets

This profile combines owner-approved background, public project links, original illustrated artwork, and public GitHub data. It does not publish private project names, client details, credentials or personal usage ledgers.

## Selected widgets

- **Stats and language cards:** [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats#github-actions) recommends static cards generated in Actions to avoid shared-instance rate limits. This profile uses its current canonical [stats action](https://github.com/stats-organization/github-readme-stats-action), pinned to commit `2c498845f71017821efaad14293ebc736156ef21` and core `2.2.0`. API failures fail the job rather than replacing working images with error cards.
- **Contribution snake:** [Platane/snk](https://github.com/Platane/snk), SVG-only action pinned to `d8f6715049803e982ee5ff501b6b9b7d5deeb09b`. Light/dark variants visualize the public contribution calendar; the animation is not a productivity score.
- **Technology icons:** [Skill Icons](https://github.com/tandpfun/skill-icons), for the stack already represented in the portfolio/profile.
- **Badges:** [Shields.io](https://shields.io/), for navigation and public follower counts. No image-load counter is presented as a unique audience measurement.
- **Recent writing:** a standard-library RSS updater reads the public feed at `https://angelodeleon.com/rss.xml`, validates article destinations, and changes only the marked writing block.

## Refresh and permissions

The workflow refreshes daily and supports manual dispatch. Pull requests generate artifacts for review and cannot publish. Generation uses a read-only, repository-scoped `GITHUB_TOKEN`; no owner PAT or private-data token is configured. Only a separate publication job can write to this profile repository. It commits validated SVGs and the writing block.

Actions use immutable commit pins. Widget/feed failures stop publication, leaving the previous committed assets available. GitHub schedules may be delayed or paused for inactive public repositories; consult the Actions run for the last successful refresh. This is a generated profile, not a real-time telemetry service.

Cards reflect the widget library's public GitHub API scope and limitations. They do not establish private output, hours worked, code quality or competence. The profile uses public-only credentials rather than requesting private access for broader statistics.

## Artwork

The named San Francisco workshop banner is original profile artwork. Project imagery is reused from the owner's repositories/portfolio, including BrowserHelm, Agent Watchtower, Vibesomnia, BrowserRAD, SocialCanvas and both Claude tools. Illustrated panels are conceptual; they do not contain private conversations or measured results. Source and case-study links accompany each project.

## Validation

```sh
python3 -m unittest discover -s tests
python3 scripts/check_profile.py --source-only
python3 scripts/check_profile.py --generated path/to/downloaded/widgets
```

After initial generated assets are committed, `python3 scripts/check_profile.py` verifies every local image target. Review the actual rendered GitHub profile at desktop/mobile widths before publishing presentation changes.
