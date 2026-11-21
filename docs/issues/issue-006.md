# Issue-006

## 背景与用户目标

TinyAgent 已经具备 Agent Loop、工具调用、Task 持久化和 Hook 生命周期，但上下文组装规则分散在 Agent 逻辑中。用户需要一个统一的 ContextManager，稳定管理系统提示、工具 Schema、历史消息、Task.md、工具调用和工具结果。

## 当前现状

- 当前已有 `tinyagent/context.py` 和基础上下文测试。
- DeepSeek 使用 OpenAI-compatible Chat Completions 消息结构。
- 工具调用需要使用 assistant `tool_calls` 和对应的 `tool` 消息。
- Task.md 需要每轮重新读取。
- 用户新输入需要立即取消当前 Agent Loop。
- 当前没有完整的上下文组装契约。

## 预期交付物

- ContextManager 及统一消息块结构。
- 稳定的上下文组装顺序。
- 每轮 Task.md 读取。
- DeepSeek 工具调用和工具结果消息配对。
- Thinking 内部传输字段保留。
- 用户新输入取消当前 Loop。
- 相关单元测试和集成测试。

## 验收标准

- 静态系统提示和工具 Schema 位于上下文前部。
- 历史消息位于 Task.md 之前。
- 每轮读取最新 Task.md。
- assistant `tool_calls` 与 `tool_call_id` 正确配对。
- Thinking 不作为普通展示历史重复注入，但保留 DeepSeek 所需内部字段。
- 用户输入到达后当前 Loop 停止。
- 已完成工具结果可以记录，但不进入新输入创建的上下文。
- `python -m unittest discover -s tests -v` 通过。

### 明确不做

- Session 原始历史持久化。
- `read_session_result`。
- 上下文压缩和摘要。
- 真实 Bash 执行。
- 会话恢复。
- Task 文件格式调整。

## 基线

- 仓库 https://github.com/Moleitau-WorldSaver/TinyAgent
- 分支 `main`
- 已核对提交 `d62ee221cdd4f643c9a3c139612fb758917ef790`
- 开始实现前再次确认最新 head。

## 对应执行计划

[Plan-006](../plans/plan-006.md)
