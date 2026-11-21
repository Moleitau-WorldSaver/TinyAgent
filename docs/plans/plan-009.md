# Plan-009

## 目标

实现第四道摘要压缩管线和超限降级流程。摘要读取 Session 原始内容，不覆盖原始记录。

## 切片顺序

1. 核对 `tinyagent/context.py`、`tinyagent/session.py`、`tinyagent/model.py` 和 Hook 入口。
2. 定义摘要工具的输入、输出和 result_id 关系。
3. 读取 Session 原始内容生成摘要。
4. 限制摘要最大长度为 1000 tokens。
5. 摘要失败最多重试一次。
6. 失败后执行确定性保留规则。
7. 仍然超限时停止模型调用并提示用户。
8. 在 Context 中标记已经发生压缩。
9. 增加摘要和失败降级测试。

## 涉及文件

- `tinyagent/compression.py`
- `tinyagent/session.py`
- `tinyagent/context.py`
- `tinyagent/model.py`
- `tinyagent/hooks.py`
- `tests/test_summary_compression.py` 新增
- `tests/test_context_compression.py`

## 每一步改动要点

- 摘要使用当前 DeepSeek，同步调用。
- 摘要读取 Session，不直接读取被截断的 Context。
- 摘要最大长度固定为 1000 tokens。
- 摘要最多重试一次。
- 原始 Session 永远不被修改。
- 摘要失败后使用前三道确定性管线的结果继续。
- 最终仍超限时不再发送模型请求。
- 用户看到明确的压缩或超限提示。

## 测试命令

```bash
python -m unittest discover -s tests -v
```

重点测试：

- 摘要读取 Session。
- 摘要长度限制。
- 一次重试。
- 确定性降级。
- 仍超限终止。
- result_id 关系。
- 原始 Session 不变。
- Task 状态保留。
