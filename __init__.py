"""ComfyUI Node Toolkit

Two small, dependency-light custom nodes:

1. Mask Cleanup  - threshold / despeckle / erode / feather for matting masks.
2. MiniMax H3 Image Aspect Selector - official MiniMax H3-Image aspect/size table.

Repository: https://github.com/LZM2023/comfyui-node-toolkit
License: MIT
"""

from .nodes.mask_cleanup import MaskCleanup
from .nodes.minimax_h3_aspect_selector import MiniMaxH3ImageAspectSelector

NODE_CLASS_MAPPINGS = {
    "MaskCleanup": MaskCleanup,
    "MiniMaxH3ImageAspectSelector": MiniMaxH3ImageAspectSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskCleanup": "Mask Cleanup (阈值/去孤岛/去边/羽化)",
    "MiniMaxH3ImageAspectSelector": "minimaxH3-image 比例选择器",
}

WEB_DIRECTORY = None
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
