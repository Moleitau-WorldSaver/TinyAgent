# Plan-002

# 工具目录、Schema 与并行调用

## 目标

完成九个工具的独立注册、描述、参数 Schema、Provider 边界和多工具调用处理。

## 切片顺序

1. 核对 `catalog.py`、`tools.py` 和 Agent Loop。
2. 定义 bash、read、edit、write、calculator、search、read_docs、todo、weather。
3. 为每个工具补齐名称、描述和 JSON Schema。
4. 建立 Search Provider 和 Weather Provider。
5. 加入 Mock Provider。
6. 实现多个工具调用的并行执行。
7. 按模型原始调用顺序整理结果。
8. 添加失败结果、参数错误和顺序测试。

## 涉及文件

- `tinyagent/catalog.py`
- `tinyagent/tools.py`
- `tinyagent/agent.py`
- `tinyagent/model.py`
- `tests/test_catalog.py`
- `tests/test_agent.py`
- `README.md`

## 改动要点

- 每个工具独立注册。
- 未注册工具不能执行。
- 参数校验错误生成结构化工具结果。
- Search 和 Weather 使用可替换 Provider。
- Bash、Edit、Write 不产生真实副作用。
- 并行执行后按原始调用顺序写回模型。
- 一个工具失败不丢失其他结果。

## 测试命令

```bash
python -m unittest discover -s tests -v
```

重点验证：

- 九个工具 Schema。
- 单工具调用。
- 多工具并行调用。
- 结果顺序。
- 单个工具失败。
- 50 轮限制。

## 回滚

回滚新增工具目录时保留 Issue-001 的基础注册表和 echo 工具。
