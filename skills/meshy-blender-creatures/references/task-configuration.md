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
  concurrency: 1                   # 示例值，按资源与服务限制调整
generation:
  provider: "meshy"
  model: "verify-at-execution"
  geometry_resolution: "standard" # 可选起点，不是全局强制
  texture_at_provider: false        # 适用于计划自行处理表面的任务
budget:
  approved_credit_cap: null         # 尚未填写授权，不能据此付费
  approved_attempt_limit: null
  reserve_for_revision: null        # 由任务决定
delivery:
  triangle_target: null             # 先按用途确定，允许说明例外
  file_size_target_bytes: null
  texture_profile: "decide-after-clay-review"
  required_runtime_checks: []       # 按交付用途填写；空表不表示免检
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

## 与已有资产流程并用

本路线只补充外部图生底模及其后续修整。现有流程若已规定研究、美术、轻量材质、既有模型改造、导出和事实复核，复用它们的适用部分，而非复制一套平行标准。

原流程若假定“全部几何从零人工生成”、特定重建方式或固定旧试验额度，不要悄悄将外部底模塞进该合同。按当前任务明确选择兼容路线，说明生成底模的来源与可复现范围；仅有底模和编辑记录不代表能确定性重造外部服务的原始输出。需要调整项目入口或验证 profile 时另列最小改动，获批后实施，不通过改标签伪造旧验证已过。
