# Issue-003

## 背景与用户目标

接入真实 DeepSeek API，验证真实文本响应、工具调用、Thinking 和错误处理。

## 当前现状

已有假的模型适配、配置读取和离线测试，但没有 DeepSeek 真实冒烟路径。

## 预期交付物

- DeepSeek 适配器。
- 本地 API 配置。
- 文本和工具调用解析。
- Thinking 内部传输。
- calculator 和 read_docs 真实冒烟测试。

## 验收标准

- API Key 不进入仓库。
- 文本响应可以输出。
- 工具调用可以回传。
- Thinking 字段正确处理。
- 离线测试继续无密钥运行。

### 明确不做

- 其他模型 Provider。
- 真实搜索和天气。
- 真实 Bash、Edit、Write。
- 权限闸门。
- 上下文压缩。

## 对应执行计划

[Plan-003](../plans/plan-003.md)
