# Meshy 接入：只保留易错点

本页为 **2026-10-30** 查验的官方 API 摘要，不是永久价格表。正式调用前复核 [Multi-Image to 3D API](https://docs.meshy.ai/en/api/multi-image-to-3d) 和 [API 价格](https://docs.meshy.ai/en/api/pricing)。API 与网页工作区的选项、费用可能不同；账户余额也不等于任务获批预算。

## 参数与估价

- 创建多图任务使用 `POST /openapi/v1/multi-image-to-3d`；`image_urls` 接受 1–4 张独立图片。当前 `meshy-7.1` / `latest` 将首张作为 front，不能继续盲用旧模型的图序假设。
- 当前 `latest` 指向 `meshy-7.1`；为可解释的比较，记录实际选择与服务响应，避免把漂移的 `latest` 当作永久版本。`meshy-7` 已弃用。
- 多图几何档位为 `geometry_resolution: "standard"` 或 `"2k"`；后者为 Ultra。旧 `ultra_mode` 已弃用，此接口不支持 `"4k"` 几何。
- 自行处理表面时明确设 `should_texture: false`，不要依赖其默认值。若开启服务端减面，确认其适用参数，并实测输出；目标面数不是结果保证。
- 当前 7.1 多图：纯底模 Standard **20 积分**；Ultra 几何增加 **5 积分**；2K/4K 贴图整任务 **30 积分**、8K 为 **35 积分**，Ultra 另加。该表只是 API 当前报价；以所选模型/参数及实际消费记录为准。图像生成、其他服务调用、算力与人工成本另计。

不把“额度 ÷ 每次单价”说成合格成品数量；预算需容纳修订、无收益候选及其他实际使用的服务。高档位能增加几何细节，但不保证纠正错误比例或输入歧义。

## 本项目参考驱动预设

以下为请求参数片段，须另外附已通过门禁的输入，不含预算授权。2026-10-30 再核官方参数：`geometry_resolution` 默认 `standard`，`should_texture` 默认 true，`enable_pbr` 默认 false，`texture_resolution` 默认 `2k`；7.1 的 `should_remesh` 默认 false，`topology` 默认 `triangle`，`target_polycount` 默认 30000，`save_pre_remeshed_model` 默认 false。明确写值，避免依赖默认：

```json
{
  "ai_model": "meshy-7.1",
  "geometry_resolution": "standard",
  "should_texture": true,
  "enable_pbr": true,
  "texture_resolution": "2k",
  "should_remesh": true,
  "topology": "triangle",
  "target_polycount": 80000,
  "save_pre_remeshed_model": true,
  "image_enhancement": false,
  "target_formats": ["glb"]
}
```

`target_polycount` 为近似目标（当前允许 100–300000），不能同时用会覆盖它的 `decimation_mode` 做固定面数比较。本轮历史报告常见约 82k–84k 三角面；交付记录实际三角面、源顶点与导出顶点，不宣称硬性 80k 上限。检查并保留所有返回原件、贴图及 `model_urls.pre_remeshed_glb`；pre-remesh 可能很大且没有 UV/贴图，不能冒充带纹理高模对照源。

本项目分别发送 4 张结构灰图到 `image_urls`、4 张对应彩图到 `texture_image_urls`，两组均 front first，使用独立精确路径/哈希；不是一个数组放 8 张。两数组各允许 1–4 张，其他任务不必凑满。7.1 的多图纹理不能与 `texture_image_url`、`texture_prompt` 或 `should_texture:false` 混用。

## 传输与冻结输入

可采用本轮的 1024 长边 LANCZOS 缩放 + lossless WebP：保留原图、缩放尺寸/工具版本，将 WebP 解码后与**缩放结果**逐像素比较。无损编码不撤销重采样，不能声称等同高分原始像素；实际发送图仍须通过结构和颜色门禁。

紧凑交接包只存图片、非敏感 params、确定性 body builder 与摘要，不重复装入巨大 base64 正文。固定排序、序列化与编码，记录最终请求 UTF-8 byte length/SHA256；恢复时重建并核对。文件标签与远端精确 ID 分开记录。冻结已评审 manifest；后续 QA、状态和恢复更新用带引用的 sidecar，不静默改旧哈希。

本轮曾观察到大正文 POST 返回 401、同环境 GET 鉴权成功；这是传输相关观察，未证明凭据失效、唯一根因或通用正文硬上限。保留去敏请求摘要与响应，按官方错误信息排查；不抽取凭据、不绕过代理。任何缩小/改图重试仍先对账，并重做受影响输入门禁。

## 创建、恢复与重试

1. 先检查参数、图像可读性和任务授权，记录输入与参数的摘要；协调者是唯一预算写者与 API dispatcher。每个 allocation 使用持久化 one-POST 锁/日志，先预留含未知费用的预算；制作线只交请求包，不能各自创建。
2. 创建成功即持久化返回 ID。按该 ID 查询状态、取回产物并记录实际消费，任务 `consumed_credits` 为实际任务费用依据；并发账户余额差不能当单任务费用。下载后校验完整性；响应中的临时下载地址不作为长期资产索引。余额不足停止，不自动充值。
3. 创建返回超时或断线时，区分“任务不存在”和“结果未知”。有 ID 就查询；无 ID 时核对服务任务记录/用量或可用的请求追踪证据。不能以暂未查到任务作为确定未扣费的证明。未对账的创建保留为待核尝试，不释放其可能占用的次数与积分。若仍无法排除已创建，报告不确定状态，暂停自动新建，等待对账或明确接受该风险的新授权；新授权须覆盖重复创建风险及最坏可预见总消费，不能只凭“再试一次”忽略原上限。
4. 轮询/下载的可恢复错误用退避和有界重试处理，不重新 POST 生成。确认失败或计划变更后，在授权与预算覆盖内可以新建下一次尝试；保留前次记录和具体修正理由。

这些是客户端恢复策略，不代表 API 保证幂等。不要自行发明幂等请求头，也不要假设所有重试免费。鉴权材料只通过执行环境安全传入；日志保留去敏后的参数与状态，不存认证头、图像 data URI 全文或带访问令牌的下载地址。

## 可用官方来源

- [任务生命周期](https://docs.meshy.ai/en/api/task-lifecycle)：查状态及处理时序。
- [API 价格](https://docs.meshy.ai/en/api/pricing)：按实际参数核价。
- [Multi-Image to 3D API](https://docs.meshy.ai/en/api/multi-image-to-3d)：模型、参数及接口限制。
