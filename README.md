# DSH Bot Avatar Sway / DSH 机器人头像摇摆

让 DeepSeek Harness 的 Bot 在思考或执行任务时左右摇摆头像，空闲时保持静止。默认左右各倾斜 18°，周期 1.2 秒；遵循系统“减少动态效果”设置。

Make bot avatars in DeepSeek Harness sway while thinking or working and stay still when idle. The default tilt is ±18° over 1.2 seconds and respects the system's reduced-motion setting.

## 兼容性 / Compatibility

- 已在 macOS 上的 `@botharness/ui` 1.4.1 本地安装包验证；其他版本尚未验证。
- 修改的是本地已安装的界面文件，不包含或重新分发 DSH / BotHarness 原始程序。应用或插件更新可能覆盖修改。
- 脚本仅接受已验证的原始文件或本项目修改后的文件哈希；其他版本或已有其他改动时会拒绝写入。
- Verified on macOS with the installed `@botharness/ui` 1.4.1 bundle. Other versions are unverified. Updates may replace the patch. The script refuses unknown or modified bundles.

## 使用 / Usage

需要 Python 3。运行前保存当前任务：重新启动 DSH 可能中断正在运行的任务。

Requires Python 3. Save work first: restarting DSH can interrupt active tasks.

```sh
python3 sway.py status
python3 sway.py install
# To remove / 恢复原状
python3 sway.py remove
```

每次修改前会在目标文件旁保留带哈希标识的备份。修改后重启 DSH 生效。可用 `--file /path/to/client.js` 指定其他安装路径；路径的兼容性仍按文件哈希校验。

A hash-labelled backup is retained next to the target before each change. Restart DSH to load it. Use `--file /path/to/client.js` for a different installation path; compatibility is still checked by hash.

## 验证范围 / Verification

本机实际运行时，通过连续截图确认工作中头像左右倾斜；空闲的另一个 Bot 头像保持静止。未验证其他操作系统、版本或所有头像布局。

On the original machine, consecutive screenshots confirmed sway during an active task and a stationary idle bot. Other platforms, versions, and avatar layouts have not been verified.
