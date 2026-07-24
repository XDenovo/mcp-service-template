# mcp-service-template

XDenovo Compute MCP Service 的一次性 Copier 脚手架。它从当前默认 `main` 分支生成一个
完整、锁定、经过测试且可构建容器的私有下游服务；生成仓库随后独立拥有依赖、CI、Docker
和文档的全部维护责任。

## 创建项目

使用受支持的 Copier 精确版本直接从 GitHub 创建：

```bash
uvx --from copier==9.17.0 copier copy \
  --trust \
  --vcs-ref=main \
  gh:XDenovo/mcp-service-template \
  my-service
```

Copier 只询问项目名称和可选描述。`--vcs-ref=main` 有意使用运行时的默认 `main` 分支，
而不是一个可复现的模板发布版本。`--trust` 允许唯一的 post-copy task 使用固定的 uv 版本
运行 `uv lock`。

生成结果不包含 Copier answers file，也不保留与本模板的同步关系。未来执行依赖升级、调整
CI 或 Docker、扩展服务代码和维护文档，都直接在生成仓库中完成。

## 本地开发模板

模板仓库本身没有根 Python 环境。修改后从当前 checkout 渲染一个临时服务：

```bash
template_preview_dir="$(mktemp -d -t xdenovo-mcp-template.XXXXXX)"

uvx --from copier==9.17.0 copier copy \
  --trust \
  --vcs-ref=HEAD \
  --defaults \
  --data project_name=example-service \
  . "$template_preview_dir"
```

然后执行与生成仓库 CI 相同的检查：

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

`template/pyproject.toml.jinja` 定义初始依赖兼容范围，fresh render 生成的 `uv.lock` 记录精确
解析状态。模板维护只验证当前 fresh-copy 行为；已经生成的仓库不是后续模板更改的迁移目标。
