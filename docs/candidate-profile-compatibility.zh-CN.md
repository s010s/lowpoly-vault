# 静态小生命候选：最小统一检查合同

前半部分保留初始设计，后半部分记录已实施的显式兼容版本与准确边界。当前 31 件发布由固定 source/QA 哈希的专用发布描述符检查；不把 profile 兼容或独立模型 QA 冒充完整 candidate gate 通过。

## 当前冲突与边界

`scripts/validate_candidate.py:213` 只接受 study/production；214 行要求 publication_authority 严格为 separate；222 行要求 turntable_frames 至少 2；228–230 行为 production 硬性要求 front/rear/left/right/top/bottom/clay/wire/detail；480 行逐条要求参考条目的 title/url/license 文本。

batch04/06 的冻结任务要求 hero/reversehero/front/side/rear/top/clay/silhouette 八个固定视图和 0 帧转台。batch04 先在参考 license 字段失败；batch06 先在 publication_authority 自由文本失败。它们的旧 checker invalid 必须保留。几何/模型独立 QA PASS、Khronos validator PASS 与 candidate 合同 PASS 是三个不同结果。项目级批量发布授权已经存在；QA 子任务不执行合并不表示项目缺少授权。

## 最小改法

1. 为明确批准的静态风格化任务新增版本化 `static-stylized-v1` profile，保留现有 study/production 路径及断言。调用时显式选择 profile，不能因旧 checker 失败自动降级。新的规范化 sidecar 绑定原始 brief、references、candidate、GLB、Blend、source commit 和 QA commit 的 SHA-256；冻结旧记录不改写。
2. 按该 profile 检查精确八视图的清单、文件存在、尺寸、哈希、同一 GLB 哈希及实际相机记录。零转台是该 profile 的明确合同值；不能把缺失转台当作已生成，不能将 side 标签臆改为 left/right。其他 profile 的转台及视图要求保留。
3. 共用现有安全路径、字节/哈希、重复 ID、GLB 结构、尺寸/轴/名义尺度、原始阈值、Khronos、源/GLB 一致性、真实 Three.js 加载及 GPU/scene 证据检查。对未改的固定证据仅复算哈希和分析报告；只在证据缺失、模型变更或有针对性疑点时重跑对应项。证据必须含正的渲染三角面且无运行错误；视觉结论绑定独立 QA 的精确源提交和每件 PASS。
4. 将 `publication_authority: separate` 保持为候选与发布分离的机器字段，把现有用户批量发布授权放在单独的 policy pin。老 brief 的自由文本通过 sidecar 明确保留原文和规范化含义；不伪造原始字段已经正确。发布协调器独占 release 描述符与生产合并。
5. 对参考资料区分“仅查阅且没有并入媒体”与“实际并入资产”。缺失旧 license 文本不能随意填成 CC BY 或猜测授权；新 sidecar 要明确 usage、incorporated=false、来源/访问范围和原文 pin。真正并入的第三方内容仍需可核验许可与署名，否则失败。科学命名和不确定性照独立 QA 的最终双语文案保留。

## 一个统一入口及输出

建议入口：`python scripts/validate_candidate_profile.py --profile static-stylized-v1 --index <batch-index.json> --json`。

每件输出独立的 technical、source_export、runtime、visual_qa、profile_contract、publication_policy 六项结果，以及原始 `legacy_checker` 的 exit code、valid=false 与完整错误证据 pin。总结果只能在新合同全部必需项通过时 PASS；明确标注 `legacy_checker: incompatible` 并不改变旧 checker 的失败。发布 manifest/descriptor 仅接受明确的新合同版本与所有 PASS 的精确 payload 集合，默认拒绝未知 profile。

最少回归用例：完整静态八视图通过；删除任何视图、篡改图/GLB/Blend/brief/reference/QA 哈希失败；错误源提交或 QA 仅审旧模型失败；非零运行错误/零渲染三角面失败；越界路径/符号链接/重复 ID 失败；混淆 separate 与用户 policy 失败；实际并入内容却无许可失败；旧 production 不足转台/视图仍失败；原有发布 31 件与下载字节不变。测试中运行旧 checker 并明确断言其历史失败被保存，不能通过删除断言完成迁移。

## 已知后续队列（不属于本次 31 件发布）

- batch04：source abc24f3289df8ccce4ef6fd29c1edb1eeec8253a；独立 QA 2404d63bf812e113c4688d14e2f456ab43b8f87c；calceola/favosites/opabinia/choia，模型全 PASS。旧 checker license/零转台/视图合同差异保留。
- batch06：source e82f82ea41221afecc140d2fc7056e87cf6c1bc6；独立 QA 614977406575b05e18f3558e2ce3a20f21eb9c25；模型全 PASS。报告已澄清项目授权；旧 checker separate/零转台/视图合同差异保留。
- batch05：source e968fab0544ce2dc41814c057b1f9dca43a2b22d；独立 QA 831253010e3a177a0ab561a16328520546645fb4 已全 PASS，排入与 04/06 合并的下一次发布。

## 已实施版本：2026-10-18.1

实际入口为原有 `scripts/validate_candidate.py`，默认 `legacy-v1` 完全保留 study/production 断言。新增 `--profile static-stylized-v1 --profile-contract <sidecar>` 是显式选择；缺失 sidecar、未知规则版本、错误候选/policy 哈希、路径越界或符号链接均拒绝，不自动回退。profile 仍要求 production 的七阶段、源/generator/config、技术预算、纹理来源、真实 GPU/scene 和独立批准。静态 manifest 要求恰好八个不同固定视图；这套合同不生成转台。

`sidecar` 仅为完整候选记录的哈希和本仓库发布 policy 建立版本化解释。它把原始自由文本授权与独立发布权分开表示；历史 brief 未列 required_deliverables 时使用其候选记录中已哈希固定的 source/generator/config；显式列出的错误清单仍拒绝。原 brief、candidate、引用和报告均不改写。

consulted-only 记录需明确 `use` 为 `consulted-only` 或本批完整固定表述、全局 `no_incorporated_third_party_assets: true` 和非空 `rights_note`，不得同时声明 incorporated，也不能作为已并入纹理的来源。其他引用和全部纹理来源的 license 要求保留，不推断第三方许可。

```sh
python scripts/candidate_profile.py path/to/candidate.json > path/to/profile-contract.json
python scripts/validate_candidate.py path/to/candidate.json --profile static-stylized-v1 --profile-contract path/to/profile-contract.json --json
python scripts/validate_candidate.py path/to/candidate.json --profile static-stylized-v1 --profile-contract path/to/profile-contract.json --require-approved --json
```

输出含 `validation_profile`、`rule_version`、`profile_contract_status` 和未改写的 `legacy_result`。`profile_contract_status: pass` 只说明已固定输入的 brief/reference 合同兼容，绝不代替 `valid`、`approved_for_brief` 或所有技术/视觉检查。完整记录有错误时仍 `valid:false`；unknown/pending 不自动批准，`--require-approved` 仍失败。正式静态批准还必须明确记录所用 profile/rule 版本。

真实 batch04/06 的兼容检查已暴露独立的记录问题：04 blockers 是字符串而非结构对象；06 unknown criterion ID 不匹配 brief。这些错误保留，未增加豁免。当前批量发布继续使用另行绑定源提交、独立 QA 和实际证据的显式发布描述符；不宣称上述完整候选记录已经通过 candidate gate。未来制作者应按现有模板生成结构化 blocker 与匹配 criterion ID；新 profile 不负责自动修补旧记录或提升 QA 状态。
