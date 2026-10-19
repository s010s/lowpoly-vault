# 砂岩：两种世界摆放的验证图

范围：只导入冻结的Before生产GLB与现有After校准GLB渲染；没有改GLB/Blend、没有新模型版本、没有导出地形资产、没有运行完整QA、没有merge或上线。地形是临时中性验证载体。两件既有模型和图片保持原字节。原有参考图像素访问限制保持不变；不以摆放图补充实物参考通过。

- `half-buried-slope-comparison.jpg`：底部下移0.135m，约下部0.15m与土坡相交。顶面、主要层理侧面及右侧保持暴露。
- `embedded-bank-comparison.jpg`：模型向坡壁移动+0.06m，背部嵌入；坡脚、两侧与周围土体接合，主要层理面仍外露。没有草、碎石、雾或装饰遮盖边界。

每组Before/After使用相同原尺度、位置、透视相机、55mm镜头、地形、灯光和颜色管理。镜头在模型地面原点上方1.15m／1.25m，朝向露面；属于普通人／儿童观看高度范围，不是俯视正交陈列镜头。四张原始PNG、相机和GLB哈希见render-manifest.json。Cycles CPU 64 samples，Standard/None，曝光0。

## 用途结论

砂岩可作为约80cm宽的局部露头碎块，部分埋在土坡中，或将背部嵌入坡壁、让层理面朝向步行路径。普通视线能同时看到顶面和层理侧面。若把它埋到只剩水平顶面，主要层理信息反而会丢失；这件不是只能从顶面看的地表瓦片。

候选取消了原版整块矩形外框和周期台阶，但每组层理仍主要由直线、单一倾率的条带组成，顶面与侧边仍是概括的大平面。用户指出的平行／程序化观感仍有依据。两种摆放只改变露出范围，无法修复层理生成逻辑。候选侧面仍偏光滑色带，不能据此声称已经符合砂岩的结构质感。局部平行层理本身不是错误，条带也不必全部做成凸起或沟槽；本补充未重新核验实物照片，不新增事实通过。局部碎块用途可继续A/B比较；大面积自然坡壁或可直接连续铺设的山体用途仍未成立。

两图的接缝与切块感按实际渲染记录在placement-observations.json。本补充不改变已有独立QA允许用户A/B比较、无生产批准的边界。用户风格反馈继续等待，不据此追加美学修模。

## 复现

仓库根：

```sh
blender -b -t 2 --python experiments/geology-calibration-20261019/sandstone-use-validation/render.py
python experiments/geology-calibration-20261019/sandstone-use-validation/compose.py
```

原候选提交：34d8d3f3b46503a0f5d734cc200ebb2c4f2136e0。既有独立QA提交（父会话提供）：5f981d9e744932093ea058197abadf7a13b1beb5。此处仅补场景图，不重跑或改写旧QA。

作者：Leon Made This <8357465+s010s@users.noreply.github.com>。脚本MIT，渲染和文档CC-BY-4.0。
