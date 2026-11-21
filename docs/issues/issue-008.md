# Issue-008

## 背景与用户目标

单条工具结果过长或结果数量过多时，模型上下文会超出预算。系统需要在每轮工具执行后使用确定性规则压缩上下文，同时保留 Session 原始结果。

## 当前现状

- 已有 `before_context_compression` 和 `after_tool_result` Hook。
- 尚无四道确定性压缩管线。
- 压缩不能覆盖 Session 原始结果。
- 最近三次工具调用结果需要完整保留。

## 预期交付物

- 单个结果 8000 字符阈值。
- 超限结果保留前 2000 字符和 result_id 引用。
- 结果条数限制，默认从 50 条压缩到 30 条。
- 前 3 条、占位符和后 26 条的保留规则。
- 最近三次工具调用结果保护。
- 更旧结果保留前 2000 字符和引用。
- 必须保留消息集合。
- 与 ContextManager 和 Hook 的集成。

## 验收标准

- Session 原始内容不变。
- 8000 字符阈值行为稳定。
- 50 条到 30 条结果的分布正确。
- 最近三次工具调用结果完整保留。
- 系统提示、当前问题、Task 状态、未完成调用和关键错误不被删除。
- 并行工具结果仍按模型原始顺序整理。
- `python -m unittest discover -s tests -v` 通过。

### 明确不做

- 摘要模型。
- 摘要工具。
- Session 恢复。
- 真实 Bash 执行。
- Task 状态修改。

## 基线

- 仓库 https://github.com/Moleitau-WorldSaver/TinyAgent
- 分支 `main`
- 已核对提交 `d62ee221cdd4f643c9a3c139612fb758917ef790`
- 开始实现前再次确认最新 head。

## 对应执行计划

[Plan-008](../plans/plan-008.md)
