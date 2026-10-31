# 任务配置与轻量记录

## 通用方法与项目配置分层

Skill 保留方法：有效视图、避免重复创建付费任务、形体优先、实测资源、真实 GLB、独立 QA 与明确发布边界。

项目/任务决定：物种与风格、输入来源、允许简化、尺寸坐标、目标设备、软预算、生成档位、重试额度、制作工具、并发、存储、验收范围及发布权限。配置只能记录已有授权，不能自行创造预算或权限。私有存储定位、凭据绑定与实际任务账在执行方维护，不放进公开示例。

以下是说明字段含义的匿名 YAML，**不是可直接运行的 API 请求，也不是已获授权的任务**：

```yaml
asset:
  subject: "匿名生物样本"
  representation: "evidence-informed-stylized"
  use: "静态近景展示"
  accepted_simplifications: ["眼睛简化", "非逐颗精雕牙齿"]
  critical_features: ["头身比例", "肢根连接", "承重姿态"]
execution:
  environment: "task-defined"       # local / remote / cloud 由实际任务决定
  storage: "task-defined"           # 不预设服务商
  maker_lanes: 4                   # 本项目：每条从研究到最终归档，非按阶段拆线
  independent_support_slots: 2     # 独立 QA / 归档支持；不自审代替独审
  budget_writer_and_dispatcher: "coordinator"
generation:
  provider: "meshy"
  model: "meshy-7.1"               # 调用前复核版本与费用
  geometry_resolution: "standard"
  texture_at_provider: true         # 本项目：参考驱动 2K PBR，详见 meshy-api.md
  texture_resolution: "2k"
  enable_pbr: true
  inline_remesh: {topology: triangle, target_polycount: 80000, save_pre_remeshed_model: true}
budget:
  approved_credit_cap: null         # 尚未填写授权，不能据此付费
  approved_attempt_limit: null
  reserve_for_revision: null        # 由任务决定
delivery:
  triangle_target: 80000            # 近似目标，实际 triangles / vertices 必须测量
  file_size_target_bytes: null
  texture_profile: "source-2k-pbr"   # Q90 等衍生版另验，保留原件
  required_runtime_checks: [physical_scale_and_ground, web_viewer_load, browser_gpu, published_readback]
  integration: "deferred"          # 静态通过后，等本次集成授权生效再校准/运行时验收
authorization:
  generate: false
  modify: false
  publish: false
```

## 保留足够的信息，不制造繁琐账本

每个模型一张短表或一个记录文件即可；已有项目 schema 能表达时直接复用：

- **目标与输入**：简要授权范围、来源/许可、设计选择、输入哈希及顺序；复用研究的版本与仍适用理由。
- **每次付费尝试**：参数、创建状态、可恢复的任务 ID、开始/结束、预计与已确认消费；未知费用单列待核。失败退款只在实际确认后入账。
- **产物**：底模/源/最终 GLB 的版本与哈希、修改摘要、三角面、导出顶点、primitives、材料、GLB bytes、各贴图尺寸/编码/bytes。
- **验收**：目标标准、实际观看范围、检查结果、独立复核者/方式、未测项目、接受的低模取舍和影响。
- **时间**：服务端处理、客户端等待/下载、实验墙钟与确实计时的主动操作分列；没有数据填“未记录”。

真实任务 ID、私有引用和明细账可留在私有工作记录中；公开案例用虚构 ID 和聚合统计，且明确标为示例。不要删除旧失败、篡改旧账或把费用未知改成零；新增授权另记，不把旧失败当作永远不能继续的理由。

每条制作线隔离物种 brief、参考身份/路径/哈希、候选修订与当前门禁；换执行者交接真实任务 ID 和已知 POST 状态，不重置预算。负责人持续拥有研究、参考、真实 GLB 重载、自检、必要修复/减面、最终 GLB/Blend 与归档；独立支持负责复核/归档协助，阶段切换不新增制作线。

## 检查点与恢复门禁

每张生成图成功后，先保存可取得的原始 bytes、实际 prompt、物种/视图身份、版本和检查记录到获授权的私有目录；完整远端下载核对 bytes/SHA256 后，才生成下一张。被拒图标清 rejected，不送入 API。拿不到原始 bytes/恢复入口时明确缺口并暂停依赖它的后续生成；本地副本或对话展示不算持久备份。

输入门禁、服务任务 ID、原件下载、候选冻结、每份完成的独立 QA 报告均及时形成检查点。图像与 prompt 配对保存；排除密钥、认证头和临时带令牌链接。已冻结包/manifest 不改写，后续状态、QA 与恢复更新放 sidecar，以精确 ID/哈希关联。

归档原件（含 pre-remesh/返回贴图）、参考/处理记录、请求 builder/摘要、可编辑源、精确候选、通过/失败证据、费用与恢复索引。验证目标目录与上传文件均保持 owner-only，不扩大共享；完整下载核对 SHA256，ZIP 另验 CRC、清单每个成员的路径/大小/哈希及无漏项后才写 archived。恢复索引分列标签、远端 ID、bytes、SHA256；临时 URL 不作恢复入口。

复用如下私有检查点字段；示例 null/pending 不是已完成记录：

```yaml
checkpoint:
  kind: null                       # image+prompt / input / service-task / candidate / independent-qa
  asset_revision: null
  frozen_manifest_sha256: null
  files: []                        # label, path, bytes, sha256, exact_remote_id
  privacy: pending                 # 目标与文件 owner-only 的实际元数据证据
  full_download: {status: pending, bytes: null, sha256: null}
  archive_checks: {zip_crc: pending, every_manifest_member: pending}
  evidence_availability: null       # freshly-verified / historical / changed / missing
  next_gate: pending
```

恢复后只对实际读取的 bytes 作新验证；历史账本只是快照，不授权继续消费。遗失 QA 须做标为 replacement 的新评审并保存新哈希，不能重建文本后套旧哈希。历史证据的可用性标签也不自动升级为本环境新验收。

## 与已有资产流程并用

本路线只补充外部图生底模及其后续修整。现有流程若已规定研究、美术、轻量材质、既有模型改造、导出和事实复核，复用它们的适用部分，而非复制一套平行标准。

原流程若假定“全部几何从零人工生成”、特定重建方式或固定旧试验额度，不要悄悄将外部底模塞进该合同。按当前任务明确选择兼容路线，说明生成底模的来源与可复现范围；仅有底模和编辑记录不代表能确定性重造外部服务的原始输出。需要调整项目入口或验证 profile 时另列最小改动，获批后实施，不通过改标签伪造旧验证已过。
