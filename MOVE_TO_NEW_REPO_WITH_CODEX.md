# Move This Clean Handoff Branch To A Dedicated Repository

当前 ChatGPT GitHub 连接可以写文件/分支，但不暴露“创建新仓库”的管理权限。

本分支已经做成**干净独立根目录**，可以由 Codex 在用户 Mac 上一键迁移为新仓库。

建议新仓库名：

```text
PP-Food-MiniProgram-Node-Handoff
```

建议：Private。

Codex 执行目标：

1. 从 `wp746/PP-Food-Runtime-001` 获取 `miniprogram-node-handoff-v1` 分支。
2. 新建 GitHub 仓库 `wp746/PP-Food-MiniProgram-Node-Handoff`。
3. 把该分支当前根目录全部内容作为新仓库 `main`。
4. 不复制 PP-Food-Runtime-001 其他分支/历史文件。
5. 不写入任何 `.env` 或 API Key。
6. Push 后返回新仓库 URL 与 HEAD commit。
7. 确认 README 首页可直接作为小程序开发公司入口。

给 Codex 的一句话：

```text
请读取这个分支根目录的 MOVE_TO_NEW_REPO_WITH_CODEX.md，使用我的 GitHub 登录创建 wp746/PP-Food-MiniProgram-Node-Handoff 私有仓库，把当前 miniprogram-node-handoff-v1 分支的干净文件树推为新仓库 main；不要带旧 Runtime 文件或任何 API Key。完成后返回新仓库链接和 commit SHA。
```
