# Plan-005

# Hook 管理系统与 Bash 三道权限闸门

## 目标

建立可扩展 Hook 系统，在模型调用、工具调用、工具结果和上下文压缩处提供拦截点，并实现 Bash 三道权限闸门。

## 切片顺序

1. 核对 `tinyagent/hooks.py`、`permissions.py` 和 Agent Loop。
2. 定义 Hook Context、Hook Decision 和 HookManager。
3. 接入六个生命周期入口。
4. 定义黑名单规则和风险正则规则。
5. 实现黑名单硬阻断。
6. 实现工作区路径和风险命令检测。
7. 实现高风险调用批量确认。
8. 将拒绝、阻断和异常回传为工具错误。
9. 接入上下文压缩 Hook。
10. 添加 Hook 和权限回归测试。

## 涉及文件

- `tinyagent/hooks.py`
- `tinyagent/permissions.py`
- `tinyagent/agent.py`
- `tinyagent/tools.py`
- `tests/test_hooks.py`
- `tests/test_permissions.py` 新增
- `README.md`

## 改动要点

- Hook 支持继续、阻断、询问和替换。
- 六个生命周期入口保持稳定顺序。
- Bash 黑名单命令直接阻断。
- 风险正则命令进入批量确认。
- 用户确认只对当前批次有效。
- Hook 异常时安全 Hook 默认阻止工具。
- 当前版本不执行未经权限检查的真实 Bash。
- ContextManager 负责压缩算法，Hook 只负责触发。

## 测试命令

```bash
python -m unittest discover -s tests -v
```

重点验证：

- Hook 注册和顺序。
- 黑名单阻断。
- 风险确认。
- 批量允许和拒绝。
- 工作区外路径。
- Hook 异常。
- 工具错误回传。

## 回滚

回滚 Hook 和权限代码时保留已有工具注册、Task 文件和 Agent Loop。
