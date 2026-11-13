# ComfyUI Node Toolkit

两个轻量 ComfyUI 自定义节点，零额外依赖：

1. **Mask Cleanup（阈值 / 去孤岛 / 去边 / 羽化）** —— 抠图 mask 后处理，专治「背景灰雾、细小碎块、边缘光晕」。
2. **minimaxH3-image 比例选择器** —— 把 MiniMax H3-Image 官方分辨率表做成下拉节点，直接输出 width / height。

> 配套的 5 个抠图工作流见姊妹项目：[ComfyUI Matting Workflows](https://github.com/LZM2023/comfyui-matting-workflows)

---

## 安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/LZM2023/comfyui-node-toolkit.git
```

重启 ComfyUI。无需 `pip install`（只用 torch / numpy / opencv，ComfyUI 已自带）。

---

## 节点 1：Mask Cleanup（阈值/去孤岛/去边/羽化）

分类：`image/mask`

| 输入 | 说明 |
|---|---|
| `mask` | 待清理的 MASK（白=主体） |
| `threshold` | `0` = 保留软 alpha（人像/发丝）；`0.06~0.12` = 硬阈值，去背景灰雾（商品图推荐） |
| `min_area_percent` | 丢弃面积小于整图该百分比的孤立小块（0 = 关闭） |
| `erode_px` | 向内收缩 N 像素，去掉主体边缘 1~2px 光晕（0 = 关闭） |
| `feather_px` | 最终边缘羽化半径（0 = 关闭） |

输出：`mask`（清理后的 MASK）

典型接法（配合 ComfyUI-RMBG / BiRefNet / InSPyReNet / SDMatte）：

```
抠图模型 MASK ──► Mask Cleanup ──► Invert Mask ──► Join Image with Alpha ──► Save Image
```

> 注意：ComfyUI 的 `Join Image with Alpha` 把 MASK 当透明度用，所以合成前要先 `Invert Mask`。

---

## 节点 2：minimaxH3-image 比例选择器

分类：`MiniMax H3 Image`

- 输入：`aspect_ratio`（1:1 / 4:3 / 3:4 / 3:2 / 2:3 / 16:9 / 9:16 / 21:9，横竖屏分列）、`megapixels`（`4MP` / `16MP`，默认 16MP）
- 输出：`width`、`height`（INT），直接接 `MiniMax H3 Image Conditioning` 的宽/高

| 宽高比 | 16MP | 4MP |
|---|---|---|
| 1:1 | 4096×4096 | 2048×2048 |
| 4:3 横屏 | 4736×3552 | 2368×1776 |
| 3:4 竖屏 | 3552×4736 | 1776×2368 |
| 3:2 横屏 | 5024×3360 | 2512×1680 |
| 2:3 竖屏 | 3360×5024 | 1680×2512 |
| 16:9 横屏 | 5472×3072 | 2736×1536 |
| 9:16 竖屏 | 3072×5472 | 1536×2736 |
| 21:9 横屏 | 6272×2688 | 3136×1344 |

所有尺寸都已对齐到 16 的倍数，4MP = 16MP 各边减半。

---

## 兼容性

- ComfyUI 0.45+（Mask Cleanup 使用标准 MASK 类型）
- 不引入 transformers / diffusers 依赖，不会触发版本升级
- MIT License
