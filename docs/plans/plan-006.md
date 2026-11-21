# Plan-006

## 目标

建立 ContextManager，统一组装 DeepSeek 请求所需的系统提示、工具 Schema、历史消息、Task.md、用户输入、工具调用和工具结果。

## 切片顺序

1. 核对 `tinyagent/context.py`、`tinyagent/agent.py`、`tinyagent/model.py` 和现有上下文测试。
2. 定义 ContextManager 的消息块和上下文状态。
3. 固定消息顺序，静态内容放在前部，历史消息放在 Task.md 之前。
4. 每轮读取项目根目录下的 Task.md。
5. 使用 DeepSeek Chat Completions 的 assistant `tool_calls` 和 `tool` 消息。
6. 保留 Thinking 的内部字段，但不重复作为普通展示历史注入。
7. 接入用户新输入取消当前 Agent Loop。
8. 增加回归测试。

## 涉及文件

- `tinyagent/context.py`
- `tinyagent/agent.py`
- `tinyagent/model.py`
- `tinyagent/hooks.py`
- `tests/test_context.py`
- `tests/test_agent.py`
- `tests/test_model.py`

## 每一步改动要点

- ContextManager 统一维护消息块。
- Agent 只通过 ContextManager 添加用户、助手和工具消息。
- 模型适配层负责 DeepSeek 外层请求格式。
- 工具调用和工具结果使用 tool_call_id 配对。
- Task.md 在每轮模型请求前重新读取。
- 新用户输入立即取消当前 Loop，旧 Loop 结果只进入 Session。
- 保持 50 轮限制和现有 Hook 调用顺序。

## 测试命令

```bash
python -m unittest discover -s tests -v
```

重点测试：

- 上下文顺序。
- Task.md 每轮刷新。
- DeepSeek tool_calls 配对。
- Thinking 传输字段。
- 用户输入取消。
- 现有 Agent Loop 回归。
