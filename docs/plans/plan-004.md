# Plan-004

# 项目 Task 目录与 Todo 持久化

## 目标

建立项目级 Task 目录、总任务文档、具体任务文件、任务 ID、任务状态和 Todo 持久化。

## 切片顺序

1. 核对 `tinyagent/task.py`、`tinyagent/tools.py` 和当前 Task 文件。
2. 定义 `Task/Task.md` 总规划格式。
3. 定义编号任务文件格式。
4. 实现任务 ID 和状态读取。
5. 实现 Todo 创建、读取、更新、完成和取消。
6. 使用 write 写入 Task 目录。
7. 保留用户手动修改。
8. 添加跨会话和路径边界测试。

## 涉及文件

- `tinyagent/task.py`
- `tinyagent/tools.py`
- `tinyagent/agent.py`
- `Task/Task.md`
- `Task/001-*.md`
- `tests/test_task.py`
- `README.md`

## 改动要点

- Task 文件按项目保存。
- 每个任务保留稳定 ID 和状态。
- 第一版不执行任务依赖。
- Todo 只管理 Task 目录。
- Write 只能写入 Task 目录。
- 用户可以直接编辑 Markdown。
- 完成任务由 Todo 或提交任务工具更新状态。
- 不执行真实 Bash 命令。

## 测试命令

```bash
python -m unittest discover -s tests -v
```

重点验证：

- 创建任务。
- 读取任务。
- 更新状态。
- 完成和取消。
- 跨会话读取。
- 重复 ID。
- Task 目录外路径拒绝。
- 用户手动修改保留。

## 回滚

回滚代码时保留用户已经创建的 Task 文件。
