# Batch 31 独立 QA 报告

**结论：PASS。** 本次范围内四件候选均通过独立 QA；必修项：无。检查针对用户指定的儿童场景自然、精致的风格化低模，不把标本级复原或微观细节作为验收条件。

| 字段 | 值 |
|---|---|
| 仓库 | `s010s/lowpoly-vault` |
| 候选分支 / 提交 | `candidate/small-life-batch31-20261018` / `b94453827c90ed71df0087017a48701477944f35` |
| 候选所基于源提交 | `3d19efcbc6938cba9add455ee344eb50af2b8e82` |
| QA 分支 | `qa/independent-small-life-batch31-20261018` |
| 质量配置 | `static-stylized-v1`，规则版本 `2026-10-18.1` |
| 范围 | `asaphus`、`hazelia`、`sea-cave`、`cruziana-crawling-furrow` |
| 检查日期 | 2026-10-19 UTC |

QA 结论只记录在本报告和 [`results.json`](results.json)；没有更改候选、模型或 `approved_for_brief` 状态。候选中的审批字段仍为待审批。

## 逐件结论

| 资产 | 结论 | 视觉与范围结论 | 必修项 |
|---|---|---|---|
| `asaphus` | **PASS** | 椭圆三叶外形、头部附近成对高眼柱和甲片分节在八视图中成立；近看眼端与腹侧提示可读。侧视中远侧眼柱被近侧遮挡符合视角。按 inspired-by 表现，不主张整个属或具体标本复原。 | 无 |
| `hazelia` | **PASS** | 宽薄杯壁展开为不规则盾面，内外表面、放射纤维脊和小型附着基部可辨；近视与轮廓图都保留杯/盾形态。微纤维、骨针和微观孔道不属于本 brief 要求。 | 无 |
| `sea-cave` | **PASS** | 岩壁有厚度，横向洞口、顶壁、侧壁、底面和短盲腔内部可读；不是贴黑洞口的平板。封闭背面作为原创构图，不暗示所有海蚀洞形状相同。 | 无 |
| `cruziana-crawling-furrow` | **PASS** | 顶视和斜视可读出负印迹的双沟及重复斜向刮痕，近/正常尺度可见；识别依据是沟槽纹理而非底板轮廓。未指定制造者，也未声称复制出土标本。 | 无 |

视觉复核逐张检查了四件候选的 8 张固定源视图，共 32 张；也查看了实际 GLB 的近/正常尺度渲染和场景视图。源检查器对平滑面发出样式复核提示；这些柔和表面已结合原视图、Clay 视图和 runtime 图检查，判为有意的自然风格化表面，未见意外的阴影破面或连接缺陷，故作为已处置提示，不构成修复项。

## 技术与复现证据

| 资产 | 候选 GLB SHA-256 | 候选 Blend SHA-256 | 面数 | 材质 / primitive / 纹理 | GLB / Blend 大小 |
|---|---|---|---:|---:|---:|
| `asaphus` | `99432ec959c96f6370d9baa1cf416f76f247c414706d9cde57963a4cc14ca156` | `ad62b7efbaa1c22a99078f62bac4f08f435c0341a0c4ec7f3dd36a84d8d5ac8d` | 10,808 | 3 / 4 / 0 | 199,612 / 888,288 B |
| `hazelia` | `1922a96efff6f35434a4bc29434a22935f9ab44ee06b7f69ddbc2dd286002cf0` | `fd958ad6bd41659114acee19263c2e1123f78184c6248f5a388a5ca83c9ff052` | 8,052 | 2 / 3 / 0 | 152,600 / 753,268 B |
| `sea-cave` | `31328a5c5075ecd7ad8415850635188d72a2cdf055ff070a5fd0fa5c48b1adad` | `e251a55acd0fc61f02a27311eea75491ab69b726bb5970e1f85aa22ef975516c` | 3,456 | 1 / 1 / 0 | 63,736 / 582,784 B |
| `cruziana-crawling-furrow` | `280346aa5b63ff3d14d755f47fd809b9eed1fb1b11a2437daf639dc12a4ea019` | `925b63886927374d2b42e5aa4100d1ad12f622c9b7bff7e6e8ee971ee5819574` | 12,136 | 1 / 1 / 0 | 220,080 / 1,075,336 B |

四个 GLB 均低于 brief 中 14,000 三角面、6 材质、30 primitives、1 MB 的硬上限；均无纹理。独立 GLB 项目审计和重跑的 Khronos glTF Validator 均为 0 errors、0 warnings。

- 候选 Blend 在 Blender 4.3.2 中以关闭脚本自动执行的方式打开；逐件核对导出集合、单位/根变换、顶点/面数、包围盒和源场景摄像机/灯光。四件的源/GLB 三角面数一致，包围盒误差不超过 `2.33e-10 m`，根变换为单位变换，源场景没有摄像机或灯光。
- 对每件分别执行两次新鲜生成，共 8 次。八次均成功；每次重建 GLB 都与对应冻结候选 GLB 逐字节相同，语义摘要也相同。重新保存得到的 `.blend` 二进制 SHA 与候选 Blend 不同，因此不声称 Blend 文件字节相同；重建 Blend 已重新打开并独立检查其结构、计数、边界和导出结果。逐次 SHA、请求、结果和源导出检查见 [`evidence/rebuild/`](evidence/rebuild/)。
- 静态候选校验器对四件均返回有效，profile contract `pass`，规则版本 `2026-10-18.1`。

## Runtime 检查和限制

使用固定的 Three.js `0.180.0` viewer 和 Chromium，对精确候选 GLB 重新跑每件 10 个单件视图及 2 个六实例场景视图。四件共 48 张新截图均与候选 handoff 中锁定的 runtime PNG **字节完全一致**；所有模式均通过，WebGL2 可用，没有运行错误或请求失败。

| 资产 | 六实例场景 draw calls | 场景三角面总数 |
|---|---:|---:|
| `asaphus` | 24 | 64,848 |
| `hazelia` | 18 | 48,312 |
| `sea-cave` | 6 | 20,736 |
| `cruziana-crawling-furrow` | 6 | 72,816 |

渲染器是 **ANGLE / SwiftShader 软件 WebGL2**。这证明了声明环境下的加载、解析和功能渲染；它不构成硬件性能认证、实体设备验证，也不代表完整生产场景负载的性能结论。

## 哈希与继承的规划证据

- 候选 `HANDOFF.json` 中的 **155 组 path/SHA-256/byte** 声明全部重算通过；handoff 与 `QA-HANDOFF-SCOPE.json` 的 ID 集合及源提交一致。
- 四件各自 8 张源图与 12 张锁定 runtime 图均核验，结果见 [`evidence/hashes/hash-audit.json`](evidence/hashes/hash-audit.json)。冻结规划 checksum manifest 的 **72/72** 文件项均核验通过。
- 存档的规划 verifier 另有一项继承性管理问题：它引用的旧路径 `production/continuous-small-life-20261018/queue.json` 在候选中缺失，因而该 verifier 记录为受阻。当前 72 项冻结 checksum 清单和本批 155 组 handoff 声明均独立通过；该缺失不属于四件资产，也不影响本次资产结论。
- QA 证据目录的逐文件清单见 [`evidence.sha256`](evidence.sha256)（SHA-256；清单不对自身做摘要）。

## Factual scope 与参考资料

参考资料仅用来核对宽泛形态与避免越界表述，不作为复制几何的来源。简要核对依据：AMNH 对一种 *Asaphus* 高眼柱形态的说明；ROM 对 *Hazelia palmata* 杯/盾体与放射状结构的介绍；NPS 对海蚀洞可能形成过程的概述；Kansas Geological Survey 对 *Cruziana* 双叶轨迹和刮痕、制造者不确定性的说明。它们支持本批采用的有限启发式标签，不要求做标本级复原。

- [AMNH, Trilobites: Hall of Fame (PDF)](https://www.amnh.org/content/download/432038/6245021/file/trilobites-hall-of-fame.pdf)
- [Royal Ontario Museum, Hazelia palmata](https://burgess-shale.rom.on.ca/fossils/hazelia-palmata/)
- [National Park Service, Rocky Coast Landforms](https://www.nps.gov/articles/rocky-coast-landforms.htm)
- [Kansas Geological Survey, Cruziana](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno.html)
