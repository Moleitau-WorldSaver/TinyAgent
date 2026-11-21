# Plan-003

# DeepSeek 真实 API 接入

## 目标

在保留假的模型测试的同时，接入 DeepSeek 真实 API，验证文本响应、工具调用、Thinking 和错误处理。

## 切片顺序

1. 核对 `config.py`、`model.py` 和配置示例。
2. 确认 DeepSeek OpenAI-compatible 请求结构。
3. 接入本地 API Key、Base URL 和模型配置。
4. 解析文本响应。
5. 解析 assistant `tool_calls`。
6. 传回工具结果和 Thinking 字段。
7. 用 calculator 和 read_docs 做真实冒烟测试。
8. 更新 README。

## 涉及文件

- `tinyagent/config.py`
- `tinyagent/model.py`
- `tinyagent/agent.py`
- `config.example.toml`
- `.gitignore`
- `tests/test_model.py`
- `tests/test_agent.py`
- `README.md`

## 改动要点

- 真实 API Key 只存在本地配置。
- 自动化测试继续使用假模型。
- DeepSeek 工具调用保持 assistant/tool 消息结构。
- Thinking 内部字段保留，界面显示由开关控制。
- API 错误、未知工具和缺少参数都转换为结构化结果。
- 不接入其他模型 Provider。

## 测试命令

```bash
python -m unittest discover -s tests -v
python -m tinyagent.cli "Use calculator to compute 2 + 3"
```

真实冒烟测试需要本地配置，不把密钥写入仓库或日志。

## 回滚

保留 FakeModel 作为离线入口。真实 DeepSeek 适配失败时不影响离线测试。
