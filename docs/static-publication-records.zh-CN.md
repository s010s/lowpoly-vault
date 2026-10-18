# 冻结候选与显式发布记录分开保存

07–09 使用既有 `static-stylized-v1` / `2026-10-18.1`，没有修改旧 profile 或放宽阈值。原候选及旧 QA 的 BLOCKED/MUST FIX 保留。发布目录另存有原始 candidate SHA 与源提交的派生记录，规范化 consulted-only 的等义表述、记录归档依赖路径，并保留全部第三方 URL、访问限制、rights_note 和 license 缺失状态。阶段、blocker、原证据和批准状态不升级。

派生记录只说明当前合同兼容；`valid:true` 仍不等于 `approved_for_brief:true`。本次仍由明确的用户项目发布授权、独立模型 QA 与精确源/GLB/格式/视图/场景证据形成闭合的固定资产发布描述符，不将旧 checker 失败改成通过。

原创嵌入纹理与 consulted-only 参考资料必须使用不同来源记录。Meandrina 的 PNG 从冻结生成器程序生成，源资产已明确作者与许可，且原图与 GLB 嵌入字节一致。其派生记录仅将该原有作者/资产许可关联到这张原创图；不替外部文献、图片或网格虚构许可。`scripts/check_release_textures.py` 独立检查嵌入字节、尺寸、原图哈希、作者/许可记录及原始纹理预算，不授予候选批准或发布权限。

复核入口和原始证据见 [07–09 发布审计](../qa/continuous-release-round03-20261018/README.md)；通用 profile 命令和批准边界见 [profile 兼容说明](candidate-profile-compatibility.zh-CN.md)。
