# Batch85 独立 QA：1 PASS / 3 REVISE

固定提交：`b727e577737d5108f5316ab898e8d7cbc4948f9f`。四个 GLB hash 与 maker handoff 一致。

## 可用结论

- namacalathus r002：PASS，限 static candidate 阶段。馆藏照片未显露的柄明确为有文献支撑的重建，不是照片观察事实。
- piedmont-glacier r004：REVISE。肩峰394.483612m，超过原冻结 max390m。原 r002 后盖共面穿插和 r003 15/25采样失败保留；r004 的25section与后盖修复已验证。
- lava-channel r002：REVISE。右堤峰14.580974m，超过原冻结上限13m。
- karst-polje r002：REVISE。56方位局部围缘峰最低128.678604m，12方位低于冻结下限170m。不是把坡脚或谷底误认作围缘。

以上修复须改实际几何，不可改原 freeze 或用材质/镜头掩盖。保留旧revision；新revision重新固定 source/GLB/derived brief/references、两次队列重建、八视图，再按本报告做定向差异验收。

## 已验证

- 亲自检查32张最终individual512、4张genuine concept、原Oxford/NPS/USGS/Gams实际pixels及参考正文。四资产视觉/事实范围通过；数值规格不因此豁免。
- 四个保存源独立重开及重导出都与原GLB逐字节相同。project有效；Khronos四个0error/0warning；Three0.180.0四个解析通过。
- 原freeze、selected inventory、依赖闭包、源/候选、616个raw文件共52,948,655bytes全部核hash；合计757个唯一输入核hash无错。
- 每资产两个真实独立queued rebuild的PID/时序/request/result/output和最终GLB一致。所有final triplet均在真实最终render request前固定。
- 每张512图与render manifest匹配；联系表带32px标签行，图像tile逐像素无损匹配。

## 阶段与授权

| 资产 | technical | visual | factual | specification | runtime_parse | gpu | scene |
|---|---|---|---|---|---|---|---|
| namacalathus | pass | pass | pass | pass | pass | not_run | not_run |
| piedmont-glacier | pass | pass | pass | fail | pass | not_run | not_run |
| lava-channel | pass | pass | pass | fail | pass | not_run | not_run |
| karst-polje | pass | pass | pass | fail | pass | not_run | not_run |

formal/user/website/release approval 全为 false。没有 push、PR、合并、发布，也未使用用户电脑或saved环境。

完整criterion、逐视图观察、测量坐标、闭包时序和独立验证证据见 independent-qa.report.json、parameter-measurements.json、immutable-input-audit.json 及各资产目录。
