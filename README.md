# mcp-service-template

XDenovo 内部 MCP 服务的 Copier 模板。模板统一 Python、uv、FastMCP、Ruff、ty、prek、GitHub Actions 和 Docker 配置，不包含具体业务实现或测试。

## 创建项目

模板发布到 GitHub 并创建 release tag 后，运行：

```bash
uvx --from copier==9.17.0 copier copy --trust gh:XDenovo/mcp-service-template my-service
```

开发模板时可以直接使用本地路径：

```bash
uvx --from copier==9.17.0 copier copy --trust . /tmp/my-service
```

## 更新已生成项目

Copier 更新依赖 Git tag 定位模板版本。先提交生成项目中的修改，再运行：

```bash
uvx --from copier==9.17.0 copier update --trust
```

## 版本维护

Python 与 Python 工具的版本集中在 `copier.yml`。升级后应重新生成一个临时项目，提交生成的 `uv.lock`，并执行 README 中列出的质量检查。
