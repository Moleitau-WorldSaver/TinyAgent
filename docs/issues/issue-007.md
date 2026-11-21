# Issue-007

## 背景与用户目标

上下文压缩不能丢失完整工具调用和工具结果。TinyAgent 需要保存 Session 原始记录，并提供只读的 `read_session_result` 工具，让模型按引用读取被压缩的结果。

## 当前现状

- 当前有运行中的内存上下文。
- 尚无统一 Session 目录和原始事件记录。
- 尚无 `result_id` 和分段读取工具。
- 用户取消 Loop 后，已完成工具结果需要继续保留。

## 预期交付物

- `Sessions/` 原始事件目录。
- session_id、tool_call_id、result_id。
- 原始用户输入、模型响应、Thinking、工具调用、工具结果和错误记录。
- `read_session_result` 工具。
- offset 和 limit 分段读取。
- 取消后的工具结果保存规则。

## 验收标准

- 原始结果不会被压缩内容覆盖。
- `read_session_result` 只读 Session。
- 不存在的 result_id 返回结构化错误。
- 非法 offset 或 limit 返回参数错误。
- 用户取消后，已完成工具结果仍可追踪。
- Session 事件顺序稳定。
- `python -m unittest discover -s tests -v` 通过。

### 明确不做

- 上下文压缩。
- 摘要工具。
- 完整会话恢复。
- Session UI。
- 真实 Bash 执行。
- Task 状态更新。

## 基线

- 仓库 https://github.com/Moleitau-WorldSaver/TinyAgent
- 分支 `main`
- 已核对提交 `d62ee221cdd4f643c9a3c139612fb758917ef790`
- 开始实现前再次确认最新 head。

## 对应执行计划

[Plan-007](../plans/plan-007.md)
