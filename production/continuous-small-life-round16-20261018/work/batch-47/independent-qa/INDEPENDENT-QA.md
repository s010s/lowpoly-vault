# Batch 47 独立 QA

审查日期：2026-10-19
范围：仅 `ecphora`、`pteleoidea`、`karst-spring-mouth`、`shatter-cone-rock`。
交接：`4c9a811685c6fa32d67c8157dccc03c41460c135`；清单 `final-handoff.jsonl` SHA-256：`7f05a80e189c3349fde658bbd4e1daf2d1cee97ddb1170e33227bc0d27ea3886`，与 `scope.json` 中绑定值相同。
规则：`static-stylized-v1` / `2026-10-18.1`。

## 判定

| 项目 | 独立 QA | 观察 |
|---|---|---|
| `ecphora` | **PASS** | 圆壳圈与宽突出的螺旋翼肋关系清楚；顶/反视可见旋卷和脐孔，前侧及近景能读出长水管沟。各视角仍像完整壳体，没有添加不在范围内的软体。 |
| `pteleoidea` | **PASS** | 顶/反视显示连续的缺口翅轮廓和隆起纺锤形中央籽体，细柄及顶端短小花柱可辨；正侧视准确呈现翅薄。运行近景与顶像素保留中脊和两侧翅面。 |
| `karst-spring-mouth` | **PASS** | 厚顶低矮洞口、洞内空腔、向外接续的短床面/明渠在英雄、正视及灰色剖面均可辨；运行图仍显示真实开口和连接的岩床，没有靠水色或贴图造型。 |
| `shatter-cone-rock` | **PASS** | 一个具厚度的岩片上保留嵌套弧形锥面和有起伏的放射脊；灰色剖面、正视及运行近景都能读出方向层级。背面较安静，但与单面断裂露出面的表达一致。 |

本轮未发现需要模型修复的阻塞项。平滑面警告逐件结合全视角与实际运行像素审阅后均为有意的连续面处理；没有看到意外裂缝、碎面、脱接或阴影折痕。

## 核验依据

- 逐项核对的源提交为 `ecphora` **`ec87671f91c56fb3250c2456a7cac469c7d538fe`**、`pteleoidea` **`f5b6540ed573a840ec53147c3ad5adf53c803303`**、`karst-spring-mouth` **`cb33bfc72123224009c52080e15485af53632750`**、`shatter-cone-rock` **`2f0aba4ced145a0166bbce1c8a713f2725afb3e3`**。每件交接记录中的 35 个文件 SHA-256 均与该精确源树一致；各自的 `checksums.sha256` 文件另有 64–65 项逐项匹配。支持明细在同目录 `EVIDENCE-VERIFICATION.json`。
- 每件 `views/view-manifest.json` 都绑定该件 GLB 哈希，列出 `hero`、`reversehero`、`front`、`side`、`rear`、`top`、`clay`、`silhouette` 八个固定视角、零转台。八张 512×512 图（silhouette 为 128×128）均按原像素逐张打开检查；同时校验了 manifest 中透明封面。完整路径与逐图 hash 见各候选 `views/`。
- 每件实际 Chromium/Three.js GLB 运行证据另有 7 张 512×512 像素图：单体 `hero`、`reversehero`、`front`、`side`、`top`、`near`，以及九实例 `scene-9-copies`；我逐张打开检查，图像字节/哈希均匹配 `runtime/evidence-manifest.json`。每个运行视角有非零前景像素与渲染三角面、`gl_error=0`。使用 ANGLE SwiftShader 软件 WebGL，只说明此环境下解析和绘制功能正常，不说明物理 GPU 或目标设备性能。
- 四份 Khronos glTF Validator 2.0.0-dev.3.10 报告均绑定候选 GLB，结果为 0 errors / 0 warnings。源导出报告均为 `pass_with_warnings`、无错误，源/GLB 三角数一致，轴转换包围盒最大误差 0 m。Blend 复测记录显示单位比例为 1、根矩阵为单位矩阵；各源网格边界边/非流形边为 0、非有限顶点法线为 0、面面积非正数为 0，封闭网格的有向体积为正。
- 每件两份保留的语义重建证据都绑定对应 generator/config；重建输出文件实际存在，GLB 字节 SHA 与交付 GLB 完全相同，报告的 semantic hash 也匹配。该结论依据保存的受限 runner 请求、结果、输出与日志以及重建报告；本轮没有再次运行建模/导出流水线。
- 审美判断按冻结 brief 和 [低模艺术检查表](../../../../../skills/lowpoly-art-direction/references/visual-acceptance.md)进行；范围/主张边界参考 [asset-factual-review](../../../../../skills/asset-factual-review/SKILL.md)。`.agents/skills` 在此 checkout 中仅含动画相关技能，与这些静态模型 QA 不适用。静态 profile 解释遵循 [2026-10-18.1 兼容约定](../../../../../docs/candidate-profile-compatibility.zh-CN.md)。

| 项目 | 交付 GLB SHA-256 | 字节 | 三角面 |
|---|---|---:|---:|
| `ecphora` | `4f80dbae01c2e405506bc978f92925975dc35427625ab505367296aade99260b` | 237,620 | 12,960 |
| `pteleoidea` | `937258e19e0397f2bb264c65932672ecde05b894515f8f3658e2dcc23afc14c9` | 69,184 | 3,692 |
| `karst-spring-mouth` | `8b4c7607c89ff4bffbbc3d855e884d6a9a0595b8db482730763f7fb4f30451c3` | 112,164 | 6,144 |
| `shatter-cone-rock` | `8a72a9b3237f7abf81c0c672d5097024bdb20648565392956cd59132b4787e79` | 135,936 | 7,462 |

## 结论边界

PASS 是对这四个冻结 GLB 的单轮独立模型/像素 QA：符合其原创、风格化教学 brief，不要求严格古生物或地质复原。具体种级复原、母株亲缘、精确地点、事件年代和水文行为不由本报告确认；标签保持各 brief 已限定的范围。四件源树都仍记录 `valid=true`、`approved_for_brief=false`，正式阶段仍是 pending/unknown；本报告没有提升候选门禁状态，也不授予发布批准。
