# Batch06 交接 — candidate，独立 QA 待安排

分支 `candidate/small-life-batch-06-20261018`；只制作 Aulopora、Thamnopora、Hallucigenia、Fenestella。每件已正常 push checkpoint；作者 Leon Made This <8357465+s010s@users.noreply.github.com>。没有 merge main、Drive 上传、强推、CI 或权限改动。

基线 main `12550349a9678398b9360e97d7908bc42667c42c`。请求的 bc73f5b 中无 batch06 TASK，因此使用 planning tip `7060ae0e5ee2c0a4c164ab1439c253d46159b561` 的 v002 四项冻结输入，原件保存在本批 planning-snapshot；未改共享 state 或其他批次。正式 claim 来自本父任务消息，见 claim.json。

| ID | checkpoint SHA | GLB bytes | triangles | POSITION vertices | materials / primitives |
|---|---|---:|---:|---:|---:|
| aulopora | `212d34e19ad234c75f477efadba223fc19eb7c51` | 178764 | 9474 | 4955 | 2 / 3 |
| thamnopora | `17b0ecb04b2f508d35cf3b06d0d4656dd585144c` | 174188 | 8866 | 4946 | 2 / 2 |
| hallucigenia | `4fcf332d31dc7295251eb3d7b765e63a52924eb9` | 285584 | 10304 | 9146 | 4 / 4 |
| fenestella | `4aa5dae9e07ef030998f2627da764e0aaae2b5ff` | 206444 | 10976 | 5732 | 2 / 3 |

所有精确 GLB / Blend / generator / config / brief / reference / evidence hashes 见 `delivery-index.json`、各项 `r001/delivery-hashes.json` 与 `final-integrity.json`。

GLB SHA-256：

- aulopora: `c652b3dec0eb541bee597922251933af32c301cb2cb8a9eba5744c66ffaa5657`
- thamnopora: `35e1e2d644be711752340b2f4b7270ca600cc39de91b418d54ae35c6fcc33c20`
- hallucigenia: `c076974098f45795fcebc3519832cf6a3b23fa45d649f1eadedeee16c6b378f1`
- fenestella: `57429dfbc0381244208a38626b38d6ced591b71f16504db85c97444793d0b3f5`

每项资源路径在 delivery-index.json.artifacts 中；每项最终目录包含可编辑 .blend、独立 GLB、中英 metadata、透明封面及 hero/reversehero/front/side/rear/top/clay/silhouette 八个源视图。`<ID>/r001/runtime-attempt-01/<ID>-contact-sheet.png` 为精确 GLB 联系表，原图同时保留；八固定 GLB 渲染约480px观看范围，另有80/160/240px运行时图。

技术自查：四件 Khronos 均零 error / zero warning；项目 GLB audit 通过；实际 Blend 重开后源/导出三角与轴转换 bounds 一致；每项两个独立 bounded queue rebuild 均 semantic equality；单位为米、ground origin 与 identity root、normals/source 拓扑检查保留。source 警告仅 intentional smooth shading；柔和主体与刻意棱面背棘有区分。全部无贴图。

实际运行时：Three.js 0.180.0 / Chromium ANGLE Vulkan SwiftShader software WebGL2；不是物理 GPU 测试。runtime-scene-attempt-01 为四种各3份，共12实例，37 draw calls / 118862 triangles（含2三角展示地面）。保持实际米制尺度；Hallucigenia 在远景极小，应前景放置或另行明确展示缩放。不宣称博物馆整合性能或跨时代共存。

如实限制：独立外观/事实/规格接受仍 pending，由父任务安排 fresh GPT-6 Luna xhigh。通用 validate_candidate.py 首先拒绝 frozen brief 的 publication_authority 字段；代码还要求最少2转台帧和旧production视图，和本轮明确0转台/八固定图冲突。失败原报表在每项 candidate-record-check.json，未改 checker/CI，也未伪造 candidate PASS。父任务需按已批准本轮契约安排独立 QA，并在需要通用 schema 接受前处理兼容问题。

来源：本轮实际只打开机构网页文字与标本/图注，没有读取或复制内嵌网格。历史 access 与本轮 maker_access 分开记录。Fenestella 明确为苔藓动物，Hallucigenia 为叶足动物；颜色、尺寸、简化数量与姿态均为原创美术选择。细微孔/爪/口器及种级鉴别不构成严格复原声明。

重建：在仓库中执行 `blender -b -t 2 --python-exit-code 1 --python production/continuous-small-life-round02-20261018/work/batch-06/build_batch06.py -- --config production/continuous-small-life-round02-20261018/work/batch-06/<ID>/r001/config.json --output /tmp/new-attempt/<ID>`；需要源图加 `--preview`。每个新尝试用新目录。依赖为当前仓库 scripts/asset_common.py 与 qa_glb.py，精确哈希已记录。运行时复核先在 repo root `python3 -m http.server 8765 --bind 127.0.0.1`，再使用本批 browser_qa.mjs 的新输出路径与 ID 参数。

本地早期失败/替代历史保留于 `/workspace/lowpoly-vault-batch06-local-recovery`，交付只引用指定最终 attempt。
