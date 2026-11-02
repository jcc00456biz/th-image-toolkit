#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class ImageScale(Enum):
    """Definitions of image and video scales."""

    # 300 DPI reference (media cases)
    DVD_AMARAY_FULL = "dvd_amaray_full"
    DVD_AMARAY_SINGLE = "dvd_amaray_single"
    BD_AMARAY_FULL = "bd_amaray_full"
    BD_AMARAY_SINGLE = "bd_amaray_single"
    VHS_SLIPCOVER_FULL = "vhs_slipcover_full"
    VHS_SLIPCOVER_SINGLE = "vhs_slipcover_single"
    CD_JACKET = "cd_jacket"
    CD_BACK_INLAY = "cd_back_inlay"
    BETA_JACKET_FULL = "beta_jacket_full"
    BETA_JACKET_SINGLE = "beta_jacket_single"
    LD_JACKET = "ld_jacket"
    VHD_JACKET = "vhd_jacket"
    LP_JACKET = "lp_jacket"
    SINGLE_RECORD_JACKET = "single_record_jacket"

    # 72 DPI
    DVD_AMARAY_FULL_72DPI = "dvd_amaray_full_72dpi"
    DVD_AMARAY_SINGLE_72DPI = "dvd_amaray_single_72dpi"
    BD_AMARAY_FULL_72DPI = "bd_amaray_full_72dpi"
    BD_AMARAY_SINGLE_72DPI = "bd_amaray_single_72dpi"
    VHS_SLIPCOVER_FULL_72DPI = "vhs_slipcover_full_72dpi"
    VHS_SLIPCOVER_SINGLE_72DPI = "vhs_slipcover_single_72dpi"
    CD_JACKET_72DPI = "cd_jacket_72dpi"
    CD_BACK_INLAY_72DPI = "cd_back_inlay_72dpi"
    BETA_JACKET_FULL_72DPI = "beta_jacket_full_72dpi"
    BETA_JACKET_SINGLE_72DPI = "beta_jacket_single_72dpi"
    LD_JACKET_72DPI = "ld_jacket_72dpi"
    VHD_JACKET_72DPI = "vhd_jacket_72dpi"
    LP_JACKET_72DPI = "lp_jacket_72dpi"
    SINGLE_RECORD_JACKET_72DPI = "single_record_jacket_72dpi"

    # 96 DPI
    DVD_AMARAY_FULL_96DPI = "dvd_amaray_full_96dpi"
    DVD_AMARAY_SINGLE_96DPI = "dvd_amaray_single_96dpi"
    BD_AMARAY_FULL_96DPI = "bd_amaray_full_96dpi"
    BD_AMARAY_SINGLE_96DPI = "bd_amaray_single_96dpi"
    VHS_SLIPCOVER_FULL_96DPI = "vhs_slipcover_full_96dpi"
    VHS_SLIPCOVER_SINGLE_96DPI = "vhs_slipcover_single_96dpi"
    CD_JACKET_96DPI = "cd_jacket_96dpi"
    CD_BACK_INLAY_96DPI = "cd_back_inlay_96dpi"
    BETA_JACKET_FULL_96DPI = "beta_jacket_full_96dpi"
    BETA_JACKET_SINGLE_96DPI = "beta_jacket_single_96dpi"
    LD_JACKET_96DPI = "ld_jacket_96dpi"
    VHD_JACKET_96DPI = "vhd_jacket_96dpi"
    LP_JACKET_96DPI = "lp_jacket_96dpi"
    SINGLE_RECORD_JACKET_96DPI = "single_record_jacket_96dpi"

    # 150 DPI
    DVD_AMARAY_FULL_150DPI = "dvd_amaray_full_150dpi"
    DVD_AMARAY_SINGLE_150DPI = "dvd_amaray_single_150dpi"
    BD_AMARAY_FULL_150DPI = "bd_amaray_full_150dpi"
    BD_AMARAY_SINGLE_150DPI = "bd_amaray_single_150dpi"
    VHS_SLIPCOVER_FULL_150DPI = "vhs_slipcover_full_150dpi"
    VHS_SLIPCOVER_SINGLE_150DPI = "vhs_slipcover_single_150dpi"
    CD_JACKET_150DPI = "cd_jacket_150dpi"
    CD_BACK_INLAY_150DPI = "cd_back_inlay_150dpi"
    BETA_JACKET_FULL_150DPI = "beta_jacket_full_150dpi"
    BETA_JACKET_SINGLE_150DPI = "beta_jacket_single_150dpi"
    LD_JACKET_150DPI = "ld_jacket_150dpi"
    VHD_JACKET_150DPI = "vhd_jacket_150dpi"
    LP_JACKET_150DPI = "lp_jacket_150dpi"
    SINGLE_RECORD_JACKET_150DPI = "single_record_jacket_150dpi"

    # 200 DPI
    DVD_AMARAY_FULL_200DPI = "dvd_amaray_full_200dpi"
    DVD_AMARAY_SINGLE_200DPI = "dvd_amaray_single_200dpi"
    BD_AMARAY_FULL_200DPI = "bd_amaray_full_200dpi"
    BD_AMARAY_SINGLE_200DPI = "bd_amaray_single_200dpi"
    VHS_SLIPCOVER_FULL_200DPI = "vhs_slipcover_full_200dpi"
    VHS_SLIPCOVER_SINGLE_200DPI = "vhs_slipcover_single_200dpi"
    CD_JACKET_200DPI = "cd_jacket_200dpi"
    CD_BACK_INLAY_200DPI = "cd_back_inlay_200dpi"
    BETA_JACKET_FULL_200DPI = "beta_jacket_full_200dpi"
    BETA_JACKET_SINGLE_200DPI = "beta_jacket_single_200dpi"
    LD_JACKET_200DPI = "ld_jacket_200dpi"
    VHD_JACKET_200DPI = "vhd_jacket_200dpi"
    LP_JACKET_200DPI = "lp_jacket_200dpi"
    SINGLE_RECORD_JACKET_200DPI = "single_record_jacket_200dpi"

    # STD (fixed size)
    DVD_AMARAY_FULL_STD = "dvd_amaray_full_std"
    DVD_AMARAY_SINGLE_STD = "dvd_amaray_single_std"
    BD_AMARAY_FULL_STD = "bd_amaray_full_std"
    BD_AMARAY_SINGLE_STD = "bd_amaray_single_std"
    VHS_SLIPCOVER_FULL_STD = "vhs_slipcover_full_std"
    VHS_SLIPCOVER_SINGLE_STD = "vhs_slipcover_single_std"
    CD_JACKET_STD = "cd_jacket_std"
    CD_BACK_INLAY_STD = "cd_back_inlay_std"
    BETA_JACKET_FULL_STD = "beta_jacket_full_std"
    BETA_JACKET_SINGLE_STD = "beta_jacket_single_std"
    LD_JACKET_STD = "ld_jacket_std"
    VHD_JACKET_STD = "vhd_jacket_std"
    LP_JACKET_STD = "lp_jacket_std"
    SINGLE_RECORD_JACKET_STD = "single_record_jacket_std"

    # Video resolutions
    VIDEO_VGA = "video_vga"  # 640 x 480 (4:3)
    VIDEO_SD_NTSC = "video_sd_ntsc"  # 720 x 480 (4:3 / 16:9)
    VIDEO_HD = "video_hd"  # 1280 x 720 (16:9)
    VIDEO_1440X1080 = "video_1440_1080"  # 1440 x 1080 (4:3 / e.g. HDV)
    VIDEO_FHD = "video_fhd"  # 1920 x 1080 (16:9)
    VIDEO_WQHD = "video_wqhd"  # 2560 x 1440 (16:9)
    VIDEO_UWQHD = "video_uwqhd"  # 3440 x 1440 (21:9)
    VIDEO_4K_UHD = "video_4k_uhd"  # 3840 x 2160 (16:9)
    VIDEO_8K_UHD = "video_8k_uhd"  # 7680 x 4320 (16:9)


# ==========================================
# Pixel dimensions (all statically defined)
# ==========================================
IMAGE_SCALE_PIXELS = {
    ImageScale.DVD_AMARAY_FULL: (3240, 2160),
    ImageScale.DVD_AMARAY_SINGLE: (1536, 2160),
    ImageScale.BD_AMARAY_FULL: (3168, 1752),
    ImageScale.BD_AMARAY_SINGLE: (1504, 1752),
    ImageScale.VHS_SLIPCOVER_FULL: (3220, 2752),
    ImageScale.VHS_SLIPCOVER_SINGLE: (1480, 2752),
    ImageScale.CD_JACKET: (1416, 1416),
    ImageScale.CD_BACK_INLAY: (1656, 1392),
    ImageScale.BETA_JACKET_FULL: (1912, 1228),
    ImageScale.BETA_JACKET_SINGLE: (904, 1228),
    ImageScale.LD_JACKET: (3896, 3896),
    ImageScale.VHD_JACKET: (3256, 3136),
    ImageScale.LP_JACKET: (3896, 3896),
    ImageScale.SINGLE_RECORD_JACKET: (2120, 2120),
    # 72dpi
    ImageScale.DVD_AMARAY_FULL_72DPI: (776, 512),
    ImageScale.DVD_AMARAY_SINGLE_72DPI: (368, 512),
    ImageScale.BD_AMARAY_FULL_72DPI: (760, 416),
    ImageScale.BD_AMARAY_SINGLE_72DPI: (360, 416),
    ImageScale.VHS_SLIPCOVER_FULL_72DPI: (768, 656),
    ImageScale.VHS_SLIPCOVER_SINGLE_72DPI: (352, 656),
    ImageScale.CD_JACKET_72DPI: (336, 336),
    ImageScale.CD_BACK_INLAY_72DPI: (392, 328),
    ImageScale.BETA_JACKET_FULL_72DPI: (456, 288),
    ImageScale.BETA_JACKET_SINGLE_72DPI: (216, 288),
    ImageScale.LD_JACKET_72DPI: (928, 928),
    ImageScale.VHD_JACKET_72DPI: (776, 752),
    ImageScale.LP_JACKET_72DPI: (928, 928),
    ImageScale.SINGLE_RECORD_JACKET_72DPI: (504, 504),
    # 96dpi
    ImageScale.DVD_AMARAY_FULL_96DPI: (1032, 688),
    ImageScale.DVD_AMARAY_SINGLE_96DPI: (488, 688),
    ImageScale.BD_AMARAY_FULL_96DPI: (1008, 560),
    ImageScale.BD_AMARAY_SINGLE_96DPI: (480, 560),
    ImageScale.VHS_SLIPCOVER_FULL_96DPI: (1024, 880),
    ImageScale.VHS_SLIPCOVER_SINGLE_96DPI: (472, 880),
    ImageScale.CD_JACKET_96DPI: (448, 448),
    ImageScale.CD_BACK_INLAY_96DPI: (528, 440),
    ImageScale.BETA_JACKET_FULL_96DPI: (608, 392),
    ImageScale.BETA_JACKET_SINGLE_96DPI: (288, 392),
    ImageScale.LD_JACKET_96DPI: (1240, 1240),
    ImageScale.VHD_JACKET_96DPI: (1040, 1000),
    ImageScale.LP_JACKET_96DPI: (1240, 1240),
    ImageScale.SINGLE_RECORD_JACKET_96DPI: (672, 672),
    # 150dpi
    ImageScale.DVD_AMARAY_FULL_150DPI: (1616, 1080),
    ImageScale.DVD_AMARAY_SINGLE_150DPI: (768, 1080),
    ImageScale.BD_AMARAY_FULL_150DPI: (1584, 872),
    ImageScale.BD_AMARAY_SINGLE_150DPI: (752, 872),
    ImageScale.VHS_SLIPCOVER_FULL_150DPI: (1608, 1376),
    ImageScale.VHS_SLIPCOVER_SINGLE_150DPI: (736, 1376),
    ImageScale.CD_JACKET_150DPI: (704, 704),
    ImageScale.CD_BACK_INLAY_150DPI: (824, 696),
    ImageScale.BETA_JACKET_FULL_150DPI: (952, 608),
    ImageScale.BETA_JACKET_SINGLE_150DPI: (448, 608),
    ImageScale.LD_JACKET_150DPI: (1944, 1944),
    ImageScale.VHD_JACKET_150DPI: (1624, 1568),
    ImageScale.LP_JACKET_150DPI: (1944, 1944),
    ImageScale.SINGLE_RECORD_JACKET_150DPI: (1056, 1056),
    # 200dpi
    ImageScale.DVD_AMARAY_FULL_200DPI: (2160, 1440),
    ImageScale.DVD_AMARAY_SINGLE_200DPI: (1024, 1440),
    ImageScale.BD_AMARAY_FULL_200DPI: (2112, 1168),
    ImageScale.BD_AMARAY_SINGLE_200DPI: (1000, 1168),
    ImageScale.VHS_SLIPCOVER_FULL_200DPI: (2144, 1832),
    ImageScale.VHS_SLIPCOVER_SINGLE_200DPI: (984, 1832),
    ImageScale.CD_JACKET_200DPI: (944, 944),
    ImageScale.CD_BACK_INLAY_200DPI: (1104, 928),
    ImageScale.BETA_JACKET_FULL_200DPI: (1272, 816),
    ImageScale.BETA_JACKET_SINGLE_200DPI: (600, 816),
    ImageScale.LD_JACKET_200DPI: (2592, 2592),
    ImageScale.VHD_JACKET_200DPI: (2168, 2088),
    ImageScale.LP_JACKET_200DPI: (2592, 2592),
    ImageScale.SINGLE_RECORD_JACKET_200DPI: (1408, 1408),
    # STD
    ImageScale.DVD_AMARAY_FULL_STD: (1280, 848),
    ImageScale.DVD_AMARAY_SINGLE_STD: (600, 848),
    ImageScale.BD_AMARAY_FULL_STD: (1248, 688),
    ImageScale.BD_AMARAY_SINGLE_STD: (592, 688),
    ImageScale.VHS_SLIPCOVER_FULL_STD: (1272, 1080),
    ImageScale.VHS_SLIPCOVER_SINGLE_STD: (584, 1080),
    ImageScale.CD_JACKET_STD: (552, 552),
    ImageScale.CD_BACK_INLAY_STD: (648, 544),
    ImageScale.BETA_JACKET_FULL_STD: (752, 480),
    ImageScale.BETA_JACKET_SINGLE_STD: (352, 480),
    ImageScale.LD_JACKET_STD: (1536, 1536),
    ImageScale.VHD_JACKET_STD: (1280, 1232),
    ImageScale.LP_JACKET_STD: (1536, 1536),
    ImageScale.SINGLE_RECORD_JACKET_STD: (832, 832),
    # Video
    ImageScale.VIDEO_VGA: (640, 480),
    ImageScale.VIDEO_SD_NTSC: (720, 480),
    ImageScale.VIDEO_HD: (1280, 720),
    ImageScale.VIDEO_1440X1080: (1440, 1080),
    ImageScale.VIDEO_FHD: (1920, 1080),
    ImageScale.VIDEO_WQHD: (2560, 1440),
    ImageScale.VIDEO_UWQHD: (3440, 1440),
    ImageScale.VIDEO_4K_UHD: (3840, 2160),
    ImageScale.VIDEO_8K_UHD: (7680, 4320),
}
