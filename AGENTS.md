# XDeNovo MCP Service Template

## Repository Role

- This repository is the Copier template for new XDeNovo Compute MCP Services. It is not a
  runnable service.
- `copier.yml` owns template questions, the derived import package name, Copier compatibility, and
  the sole post-copy lock task.
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

- `copier.yml` exposes only project identity. Dependency and tool versions are template policy,
  not generation inputs.
- The generated `pyproject.toml` owns initial dependency compatibility ranges and its generated
  `uv.lock` owns exact resolved state.
- Keep the operational Python and uv values aligned across project metadata, CI, Docker, and
  setup documentation without turning them into Copier questions.
- `project_name` is the repository and distribution name; `package_name` is its underscore-form
  Python import package.
- Keep Jinja expressions limited to template concerns. Wrap GitHub Actions expressions in
  `{% raw %}` blocks so Copier does not consume them.
- Keep third-party GitHub Actions pinned to full commit SHAs.
- Fresh renders must not contain a Copier answers file or retain a synchronization relationship
  with this template.

## Development Workflow

The template repository has no root Python environment. Validate changes by rendering a fresh
service into a temporary directory:

```bash
template_preview_dir="$(mktemp -d -t xdenovo-mcp-template.XXXXXX)"

uvx --from copier==9.17.0 copier copy \
  --trust \
  --vcs-ref=HEAD \
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
  docker build -t example-service-template-check .
)
```

Review rendered `AGENTS.md`, `README.md`, `pyproject.toml`, `uv.lock`, Dockerfile, and CI when
their source templates change. The generated pytest suites and Docker build are part of the
fresh-copy matrix.

## Version Management

Generated repositories own dependency upgrades after creation. Within the template, a change to
the initial stack must keep these fresh-rendered surfaces aligned:

- `.python-version`;
- `pyproject.toml` and `uv.lock`;
- GitHub Actions;
- Dockerfile;
- README and generated `AGENTS.md`.

Do not update a generated lockfile by hand. Render a fresh service and let the configured Copier
task resolve it.

## Generated-Service Contract

- Generated repositories use Python 3.13, uv, Ruff, ty, prek, GitHub Actions, and a non-root
  multi-stage Docker image.
- The generated package and container assemble an authenticated private MCP Server with an empty
  Tool catalog. Workers, health contracts, and service-specific behavior remain downstream work.
- Changes to generated commands must update the README, `AGENTS.md.jinja`, CI, and hook
  configuration together.
- Changes to generated structure target new copies only. Existing generated repositories are
  independent downstreams and are not migration targets.

## Git and Pull Requests

- Treat the Issue as the implementation specification and the PR as the result report.
- Follow Conventional Commits.
- Use the XDenovo organization-default Issue and PR templates.
- Preserve unrelated working-tree changes, and stage only the explicit paths intended for a
  commit.
- Describe which rendered files change and state that existing generated repositories remain
  unaffected unless the Issue explicitly scopes separate downstream work.
