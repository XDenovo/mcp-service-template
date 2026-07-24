# XDeNovo MCP Service Template

## Repository Role

- This repository is the Copier template for new XDeNovo Compute MCP Services. It is not a
  runnable service.
- `copier.yml` owns template questions, derived values, shared tool versions, and post-copy tasks.
- `template/` owns the files rendered into each generated service repository.
- Repository-root instructions guide template maintainers. `template/AGENTS.md.jinja` provides
  instructions to agents working in a generated service; keep those two audiences distinct.
- Use the canonical
  [Platform architecture](https://github.com/XDenovo/platform/blob/main/docs/architecture.md) and
  [approved technology stack](https://github.com/XDenovo/platform/blob/main/docs/techstack.md) as
  supplemental platform-wide context.

## Template Boundaries

- Generate only engineering structure and behavior shared by all Compute MCP Services.
- Service-specific Tools, scientific dependencies, domain models, repositories, Workflows,
  Activities, and Compute Job images belong in the generated service.
- Shared authentication, configuration, persistence, storage, Workflow, and observability
  foundations belong in `XDenovo/mcp-runtime`; do not copy parallel implementations into this
  template.
- Generated services are private downstreams called by Gateway. The template must not create a
  second public MCP endpoint or accept external access tokens.
- Each generated service must retain ownership boundaries for its database Schema, Job and
  Artifact metadata, object-storage namespace, Temporal Namespace, and Task Queue.
- Copier tasks run only after a user grants `--trust`. Keep `_tasks` minimal, deterministic, and
  free of credentials or unreviewed shell interpolation.

## Template Sources of Truth

- Shared Python and tool versions are declared once in `copier.yml` and rendered into project
  metadata, CI, Docker, and documentation.
- `project_name` is the repository and distribution name; `package_name` is its underscore-form
  Python import package.
- Keep Jinja expressions limited to template concerns. Wrap GitHub Actions expressions in
  `{% raw %}` blocks so Copier does not consume them.
- Keep third-party GitHub Actions pinned to full commit SHAs.
- `.copier-answers.yml` records the template source and answers used for future updates; its
  rendered warning and field structure must remain intact.

## Development Workflow

The template repository has no root Python environment. Validate changes by rendering a fresh
service into a temporary directory:

```bash
template_preview_dir="$(mktemp -d -t xdenovo-mcp-template.XXXXXX)"

uvx --from copier==9.17.0 copier copy \
  --trust \
  --defaults \
  --data project_name=example-service \
  . "$template_preview_dir"
```

The post-copy task creates `uv.lock` with the uv version configured in `copier.yml`.

Validate the rendered service with the same commands as its CI:

```bash
(
  cd "$template_preview_dir"
  uvx --from uv==0.11.30 uv sync --locked
  uvx --from uv==0.11.30 uv run --no-sync ruff check .
  uvx --from uv==0.11.30 uv run --no-sync ruff format --check .
  uvx --from uv==0.11.30 uv run --no-sync ty check
  uvx --from uv==0.11.30 uv run --no-sync pytest
  uvx --from uv==0.11.30 uv build
)
```

When Docker inputs change, also build the rendered image:

```bash
(
  cd "$template_preview_dir"
  docker build -t example-service-template-check .
)
```

Review rendered `AGENTS.md`, `README.md`, `pyproject.toml`, `uv.lock`, Dockerfile, CI, and Copier
answers when their source templates change.

The generated pytest suites are part of the fresh-copy matrix. Before changing an update-sensitive
path, also render the latest released template, add representative downstream changes, run
`copier update --trust` against the local candidate, and inspect the merge. Keep this update
scenario manual until the repository owns an automated fixture that preserves the same evidence.

## Version Management

`copier.yml` currently centralizes Python, the Python image, uv, `uv_build`, FastMCP, httpx,
`mcp-runtime`, prek, pytest, pytest-asyncio, Ruff, and ty versions. A version change must keep
these rendered surfaces aligned:

- `.python-version`;
- `pyproject.toml` and `uv.lock`;
- GitHub Actions;
- Dockerfile;
- README and generated `AGENTS.md`.

Do not update a generated lockfile by hand. Render a fresh service and let the configured Copier
task resolve it.

## Releases and Copier Compatibility

- Release tags and GitHub Releases use `vMAJOR.MINOR.PATCH`. The first consumable release is
  `v0.1.0`.
- A patch release fixes the template without intentionally changing the generated service
  contract. A minor release adds a backward-compatible generated capability or default. A major
  release may require downstream source or deployment migration.
- Validate a fresh default render, its Docker image, and an update from the latest release before
  tagging the exact validated commit. Release notes must list rendered paths that change and any
  manual migration needed by existing generated repositories.
- Generated repositories consume a released template ref and keep their Copier answers. They
  commit local work before `copier update --trust`, review Copier's merge, preserve
  service-specific code, and apply any release-note migration. Template releases do not promise
  conflict-free updates across arbitrary downstream edits.

## Generated-Service Contract

- Generated repositories use Python 3.13, uv, Ruff, ty, prek, GitHub Actions, and a non-root
  multi-stage Docker image.
- The generated package and container assemble an authenticated private MCP Server with an empty
  Tool catalog. Workers, health contracts, and service-specific behavior remain downstream work.
- Changes to generated commands must update the README, `AGENTS.md.jinja`, CI, and hook
  configuration together.
- Changes to generated structure must consider both new copies and updates of repositories that
  have local service code.

## Git and Pull Requests

- Treat the Issue as the implementation specification and the PR as the result report.
- Follow Conventional Commits.
- Use the XDenovo organization-default Issue and PR templates.
- Preserve unrelated working-tree changes, and stage only the explicit paths intended for a
  commit.
- Describe which rendered files change and whether existing generated repositories require a
  Copier update or manual migration.
