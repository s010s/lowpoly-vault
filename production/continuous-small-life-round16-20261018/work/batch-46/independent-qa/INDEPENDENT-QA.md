# Batch 46 独立 QA

审查日期：2026-10-19  
范围：仅 `eiffelia`、`pseudofrenelopsis`、`alluvial-fan`、`diplichnites-paired-trackway`。  
精确候选：`candidate/small-life-batch46-20261018` @ `1e100d5b274a40fa264a2aad7c7df884e4381ca5`。  
HANDOFF 中的模型源提交及 QA scope 预期源：`dcba545b6841ed0d9fbb213a3a20f014d6669bbf`。  
规则：`static-stylized-v1` / `2026-10-18.1`。

## 判定

| 项目 | 独立 QA | 观察 |
|---|---|---|
| `eiffelia`（attempt-02） | **PASS** | 圆囊、开口的上部 osculum、薄壁及星状骨针格架在源视图与 GLB 运行图中连贯可辨；小 ostia 也保留。微观细节和准确格目数按简化艺术表达处理。 |
| `pseudofrenelopsis`（attempt-02） | **PASS** | 保留化石枝段范围；可见渐细节间、节鞘、两条侧枝和微小叶尖，没有扩成整株树冠。叶尖刻意细小，但在近景英雄视图可读，未形成阻塞。 |
| `alluvial-fan`（attempt-01） | **PASS** | 扇顶单入流、连续下倾并展宽的扇面和浅放射分流在顶视、斜视及运行像素中可辨；与干燥教学裁片的声明相符。 |
| `diplichnites-paired-trackway`（attempt-01） | **PASS** | 中性灰顶视及运行图显示两列独立浅凹印迹、空白中央带和真实负浮雕；没有轴沟，也没有用贴图替代凹陷。 |

本轮没有发现需要模型修复的阻塞问题。

## 核验依据

- 精确 GLB、Blend、candidate、freeze、generator、config、source-scene、source-export、view manifest、源/运行 contact sheet 与 reproducibility 文件均按冻结 HANDOFF 对照 SHA-256；四个 GLB 另与 `QA-HANDOFF-SCOPE.json` 的逐项 hash 一致。
- 四项均有八个静态源视图：`hero`、`reversehero`、`front`、`side`、`rear`、`top`、`clay`、`silhouette`。我打开并检查了源视图及对应 runtime 像素，而不只依据文件名；每份 manifest 中 20 张帧图及两个 contact sheet 的记录 hash 均与文件一致。运行部分包括十个单体视图和两个六实例场景视图，零转台帧，符合固定视图 profile。
- runtime manifest 和运行记录标注 Three.js 0.180.0 / GLTFLoader 与 ANGLE SwiftShader 软件 WebGL。渲染像素按软件运行证据审查；没有将其表述为硬件 GPU 测试或设备性能结果。
- `source-scene.json`、重开记录和 `source-export.json` 均绑定到所选 Blend/GLB。导出报告无错误，源/GLB 三角数一致；边界误差依次为 0、0、约 `5.96e-8 m`、约 `4.66e-10 m`。Eiffelia 与 Pseudofrenelopsis 的 `pass_with_warnings` 仅列出平滑面需人工审视；已结合源图与运行图审阅，没有发现意外碎裂或阴影折痕。四项 Khronos 记录均为 0 errors / 0 warnings。
- 每项两份实际重建 GLB 的文件 SHA-256 都与交付 GLB 相同，重建记录的语义 hash 也一致。未重跑已留存的生成、验证或检查流水线。

| 项目 | 交付 GLB SHA-256 | 源/运行像素证据 |
|---|---|---|
| `eiffelia` | `02dc898813784aaa8c31499ae4e6194785e198d1cc8fd8764a69e45ec2425676` | `assets/candidates/continuous-small-life-round16-20261018/batch-46/eiffelia/r001/attempt-02/eiffelia/{source,runtime}-contact-sheet.jpg` |
| `pseudofrenelopsis` | `ed99158237374b5bd33014c860faaeccadd8666fad915a42493949b90f91b9ec` | `assets/candidates/continuous-small-life-round16-20261018/batch-46/pseudofrenelopsis/r001/attempt-02/pseudofrenelopsis/{source,runtime}-contact-sheet.jpg` |
| `alluvial-fan` | `27221cfb01da7389ea6b140dc0f6204cf98375ebed8518f5eb7ab9bd253d0b02` | `assets/candidates/continuous-small-life-round16-20261018/batch-46/alluvial-fan/r001/attempt-01/alluvial-fan/{source,runtime}-contact-sheet.jpg` |
| `diplichnites-paired-trackway` | `f418499b0a67866f4e49edaea8deb021c6b3586db27029f56f82fccb01fa1593` | `assets/candidates/continuous-small-life-round16-20261018/batch-46/diplichnites-paired-trackway/r001/attempt-01/diplichnites-paired-trackway/{source,runtime}-contact-sheet.jpg` |

## 结论边界

判断依照已冻结的艺术化教学 brief，不要求严格科学复原，不推断具体生物学、地质年代或制造者身份。QA scope 中的素材 hash 与本报告所审查对象一致。原候选的 `approved_for_brief=false` 和未完成的正式阶段状态保持原样；本报告只记录这一轮独立 QA，不授予发布权。
