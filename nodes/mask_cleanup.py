"""ComfyUI-MaskCleanup

A small, dependency-free mask post-processor that implements the
"方案2" cleanup chain used by the matting workflows:

    1. optional hard threshold        (kills faint background haze)
    2. remove small isolated islands  (kills specks / dust)
    3. erode by N px                  (kills 1-2px fringe around the subject)
    4. feather by N px                (softens the final edge)

All steps are optional; set their parameter to 0 to disable.

Author: built for this workspace; MIT.
"""

import numpy as np
import torch
import cv2


class MaskCleanup:
    CATEGORY = "image/mask"
    FUNCTION = "run"
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "threshold": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01,
                    "tooltip": "0 = 保留软 alpha（人像/发丝用）；0.06~0.12 = 硬阈值，去除背景灰雾（商品图推荐）",
                }),
                "min_area_percent": ("FLOAT", {
                    "default": 0.05, "min": 0.0, "max": 20.0, "step": 0.01,
                    "tooltip": "丢弃面积小于整图该百分比的孤立小块（0 = 关闭）",
                }),
                "erode_px": ("INT", {
                    "default": 1, "min": 0, "max": 32, "step": 1,
                    "tooltip": "向内收缩 N 像素，去掉主体边缘 1~2px 的残留光晕（0 = 关闭）",
                }),
                "feather_px": ("INT", {
                    "default": 1, "min": 0, "max": 32, "step": 1,
                    "tooltip": "最终边缘羽化半径（0 = 关闭）",
                }),
            }
        }

    def run(self, mask, threshold, min_area_percent, erode_px, feather_px):
        out = []
        for i in range(mask.shape[0]):
            m = mask[i].detach().float().cpu().numpy().astype(np.float32)
            m = np.clip(m, 0.0, 1.0)

            # 1) hard threshold (optional)
            if threshold > 0.0:
                m = (m > threshold).astype(np.float32)

            # 2) remove small isolated islands
            if min_area_percent > 0.0:
                binary = (m > 0.05).astype(np.uint8)
                num, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
                if num > 1:
                    total = float(binary.size)
                    keep = np.zeros(num, dtype=np.uint8)
                    for lab in range(1, num):
                        area = float(stats[lab, cv2.CC_STAT_AREA])
                        if area * 100.0 / total >= min_area_percent:
                            keep[lab] = 1
                    m = m * keep[labels].astype(np.float32)

            # 3) erode the visible support by N px
            if erode_px > 0:
                k = 2 * int(erode_px) + 1
                kernel = np.ones((k, k), np.uint8)
                support = (m > 0.02).astype(np.uint8)
                support = cv2.erode(support, kernel, iterations=1)
                m = m * support.astype(np.float32)

            # 4) feather
            if feather_px > 0:
                k = 2 * int(feather_px) + 1
                m = cv2.GaussianBlur(m, (k, k), 0)

            out.append(torch.from_numpy(np.clip(m, 0.0, 1.0)))

        return (torch.stack(out, dim=0),)


NODE_CLASS_MAPPINGS = {"MaskCleanup": MaskCleanup}
NODE_DISPLAY_NAME_MAPPINGS = {"MaskCleanup": "Mask Cleanup (阈值/去孤岛/去边/羽化)"}
