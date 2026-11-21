# Plan-008

## 目标

实现前三道确定性上下文压缩管线，不调用摘要模型，不修改 Session 原始记录。

## 切片顺序

1. 核对 `tinyagent/context.py`、`tinyagent/hooks.py`、Session 模块和测试。
2. 实现单个工具结果 8000 字符阈值。
3. 超限时保留前 2000 字符和 result_id 引用。
4. 实现工具结果数量限制，默认将 50 条压缩为 30 条。
5. 保留前 3 条、占位符和后 26 条。
6. 保护最近三次工具调用结果。
7. 更旧结果保留前 2000 字符和引用。
8. 接入 after_tool_result 和 before_context_compression。
9. 增加组合压缩测试。

## 涉及文件

- `tinyagent/context.py`
- `tinyagent/hooks.py`
- `tinyagent/session.py`
- `tinyagent/compression.py` 新增
- `tests/test_context_compression.py` 新增
- `tests/test_hooks.py`
- `tests/test_context.py`

## 每一步改动要点

- 压缩结果只影响发送给模型的 Context。
- Session 保留完整原始工具结果。
- 系统提示、当前问题、Task 状态、未完成调用和关键错误不可删除。
- 并行工具结果按模型原始调用顺序整理。
- 压缩后的结果包含可读取的 result_id。
- 仍然超限时交给 Plan-009。

## 测试命令

```bash
python -m unittest discover -s tests -v
```

重点测试：

- 8000 字符阈值。
- 前 2000 字符和引用。
- 50 条到 30 条。
- 最近三次工具调用保护。
- 必须保留内容。
- Session 原始结果不变。
