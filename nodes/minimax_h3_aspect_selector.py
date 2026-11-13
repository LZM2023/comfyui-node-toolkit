"""MiniMax H3 Image 比例选择器 —— ComfyUI 自定义节点

把 MiniMax H3-Image 官方支持的分辨率表做成一个下拉选择节点：
  · 宽高比：横屏/竖屏分开列（1:1 不分）
  · 百万像素：只有 4MP 和 16MP 两档
  · 不要「倍数」控件（所有尺寸都已经对齐到 16 的倍数）

输出 width / height 两个 INT，直接接到
`MiniMax H3 Image Conditioning` 的 width / height 输入即可。
"""


# 官方文档 16MP 尺寸（宽 x 高），4MP = 各边减半（全部仍为 16 的倍数）
SIZES_16MP = {
    "1:1 (Square)": (4096, 4096),
    "4:3 (横屏)": (4736, 3552),
    "3:4 (竖屏)": (3552, 4736),
    "3:2 (横屏)": (5024, 3360),
    "2:3 (竖屏)": (3360, 5024),
    "16:9 (横屏)": (5472, 3072),
    "9:16 (竖屏)": (3072, 5472),
    "21:9 (横屏)": (6272, 2688),
}

SIZES_4MP = {
    "1:1 (Square)": (2048, 2048),
    "4:3 (横屏)": (2368, 1776),
    "3:4 (竖屏)": (1776, 2368),
    "3:2 (横屏)": (2512, 1680),
    "2:3 (竖屏)": (1680, 2512),
    "16:9 (横屏)": (2736, 1536),
    "9:16 (竖屏)": (1536, 2736),
    "21:9 (横屏)": (3136, 1344),
}

RATIOS = list(SIZES_16MP.keys())
MEGAPIXELS = ["4MP", "16MP"]


class MiniMaxH3ImageAspectSelector:
    """minimaxH3-image 比例选择器"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (list(RATIOS), {"default": "1:1 (Square)"}),
                "megapixels": (list(MEGAPIXELS), {"default": "16MP"}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "pick"
    CATEGORY = "MiniMax H3 Image"

    def pick(self, aspect_ratio, megapixels):
        table = SIZES_4MP if megapixels == "4MP" else SIZES_16MP
        w, h = table[aspect_ratio]
        return (int(w), int(h))


NODE_CLASS_MAPPINGS = {
    "MiniMaxH3ImageAspectSelector": MiniMaxH3ImageAspectSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MiniMaxH3ImageAspectSelector": "minimaxH3-image 比例选择器",
}
