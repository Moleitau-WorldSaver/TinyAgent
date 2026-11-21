# Plan-001

# TinyAgent 最小 Agent Loop

## 目标

建立可运行的 Python Agent Loop，支持用户输入、模型响应、工具注册、工具调用、工具结果回传和 50 轮限制。

## 切片顺序

1. 核对配置和 CLI 入口。
2. 定义模型请求、模型响应和工具调用数据结构。
3. 建立工具注册表和参数校验。
4. 实现 Agent Loop。
5. 实现工具结果追加和终止判断。
6. 实现假的模型和 echo 工具。
7. 添加配置错误、工具错误和轮次限制测试。
8. 更新 README。

## 涉及文件

- `tinyagent/agent.py`
- `tinyagent/model.py`
- `tinyagent/config.py`
- `tinyagent/tools.py`
- `tinyagent/cli.py`
- `tests/test_agent.py`
- `tests/test_model.py`
- `tests/test_config.py`
- `README.md`

## 改动要点

- Agent 每轮读取当前消息并调用模型。
- 没有工具调用时返回最终文本。
- 有工具调用时校验名称和参数。
- 工具结果加入上下文后继续下一轮。
- 达到 50 轮时停止。
- 假模型用于无密钥自动化测试。
- API Key 只从本地配置或环境变量读取。

## 测试命令

```bash
python -m unittest discover -s tests -v
python -m tinyagent.cli "Say hello"
```

## 回滚

回滚本切片时保留 README 和配置示例，不删除用户本地配置文件。
