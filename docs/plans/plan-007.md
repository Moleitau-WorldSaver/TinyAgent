# Plan-007

## 目标

建立 Session 原始事件记录和 `read_session_result`，让压缩后的上下文仍然可以引用和读取完整工具结果。

## 切片顺序

1. 核对 `tinyagent/agent.py`、`tinyagent/context.py`、`tinyagent/task.py` 和测试入口。
2. 定义 Session 事件格式和 session_id。
3. 建立项目下 `Sessions/` 目录。
4. 保存原始用户输入、模型请求、模型响应、Thinking、工具调用、工具结果和错误。
5. 为工具结果生成 result_id。
6. 实现只读 `read_session_result`，支持 offset 和 limit。
7. 接入用户取消和工具完成事件。
8. 增加跨重启和分段读取测试。

## 涉及文件

- `tinyagent/session.py` 新增
- `tinyagent/tools.py`
- `tinyagent/agent.py`
- `tinyagent/context.py`
- `tests/test_session.py` 新增
- `tests/test_agent.py`

## 每一步改动要点

- Session 使用追加式事件记录。
- 时间戳和执行耗时只进入 Session，不发送给模型。
- 原始工具结果不可被压缩结果覆盖。
- read_session_result 只读 Session。
- 非法 result_id、offset 和 limit 返回结构化错误。
- 被取消 Loop 已完成的工具结果继续保存。

## 测试命令

```bash
python -m unittest discover -s tests -v
```

重点测试：

- Session 事件顺序。
- 原始结果持久化。
- result_id 查找。
- offset 和 limit。
- 用户取消后的结果保存。
- read_session_result 只读行为。
