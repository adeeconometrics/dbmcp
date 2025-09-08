from enum import StrEnum


class Categiories(StrEnum):
    """Enumeration for product categories."""
    LAPTOP = "Laptop"
    SMARTPHONE = "Smartphone"
    HEADPHONES = "Headphones"
    MONITOR = "Monitor"
    KEYBOARD = "Keyboard"
    MOUSE = "Mouse"
    PRINTER = "Printer"
    TABLET = "Tablet"
    SMARTWATCH = "Smartwatch"
    CAMERA = "Camera"


class LaptopModels(StrEnum):
    """Enumeration for laptop models."""
    DELL_XPS_13 = "Dell XPS 13"
    MACBOOK_PRO = "MacBook Pro"
    HP_SPECTRE_X360 = "HP Spectre x360"
    LENOVO_THINKPAD_X1 = "Lenovo ThinkPad X1 Carbon"
    ASUS_ZENBOOK_14 = "ASUS ZenBook 14"
    ACER_SWIFT_3 = "Acer Swift 3"
    RAZER_BLADE_15 = "Razer Blade 15"
    MICROSOFT_SURFACE_LAPTOP_4 = "Microsoft Surface Laptop 4"
    LG_GRAM_17 = "LG Gram 17"
    SAMSUNG_GALAXY_BOOK_PRO = "Samsung Galaxy Book Pro"


class SmartphoneModels(StrEnum):
    """Enumeration for smartphone models."""
    IPHONE_13 = "iPhone 13"
    SAMSUNG_GALAXY_S21 = "Samsung Galaxy S21"
    GOOGLE_PIXEL_6 = "Google Pixel 6"
    ONEPLUS_9 = "OnePlus 9"
    XIAOMI_MI_11 = "Xiaomi Mi 11"
    OPPO_FIND_X3_PRO = "Oppo Find X3 Pro"
    MOTOROLA_EDGE_20 = "Motorola Edge 20"
    SONY_XPERIA_1_III = "Sony Xperia 1 III"
    ASUS_ROG_PHONE_5 = "ASUS ROG Phone 5"
    REALME_GT = "Realme GT"


class HeadphoneModels(StrEnum):
    """Enumeration for headphone models."""
    SONY_WH_1000XM4 = "Sony WH-1000XM4"
    BOSE_700 = "Bose 700"
    APPLE_AIRPODS_MAX = "Apple AirPods Max"
    SENNHEISER_MOMENTUM_3 = "Sennheiser Momentum 3"
    JABRA_ELITE_85H = "Jabra Elite 85h"
    BANG_OLUFSEN_BEOPLAY_H9 = "Bang & Olufsen Beoplay H9"
    AKG_N700NC_M2 = "AKG N700NC M2"
    SHURE_AONIC_50 = "Shure AONIC 50"
    PHILIPS_FIDELIO_L3 = "Philips Fidelio L3"
    JBL_LIVE_650BTNC = "JBL Live 650BTNC"


class MonitorModels(StrEnum):
    """Enumeration for monitor models."""
    DELL_ULTRASHARP_U2721DE = "Dell UltraSharp U2721DE"
    LG_27UK850_W = "LG 27UK850-W"
    ASUS_PROART_PA278QV = "ASUS ProArt PA278QV"
    SAMSUNG_S32A800N = "Samsung S32A800N"
    BENQ_PD3220U = "BenQ PD3220U"
    ACER_PREDATOR_X34 = "Acer Predator X34"
    VIEWSONIC_VP3268A_4K = "ViewSonic VP3268a-4K"
    EIZO_COLOREDGE_CG319X = "Eizo ColorEdge CG319X"
    HP_Z27 = "HP Z27"
    PHILIPS_328P6VJEB = "Philips 328P6VJEB"


class KeyboardModels(StrEnum):
    """Keyboard models enumeration."""
    LOGITECH_MX_KEYS = "Logitech MX Keys"
    APPLE_MAGIC_KEYBOARD = "Apple Magic Keyboard"
    DAS_KEYBOARD_4C = "Das Keyboard 4C"
    RAZER_BLACKWIDOW_V3 = "Razer BlackWidow V3"
    CORSAIR_K95_RGB_PLATINUM = "Corsair K95 RGB Platinum"
    DREVO_CALIBER_V2 = "Drevo Caliber V2"
    FILCO_MAJESTOUCH_2 = "Filco Majestouch 2"
    ANNE_PRO_2 = "Anne Pro 2"
    KEYCHRON_K6 = "Keychron K6"
    VORTEX_POK3R = "Vortex Pok3r"


class MouseModels(StrEnum):
    """Mouse models enumeration."""
    LOGITECH_MX_MASTER_3 = "Logitech MX Master 3"
    RAZER_DEATHADDER_V2 = "Razer DeathAdder V2"
    STEELSERIES_RIVAL_600 = "SteelSeries Rival 600"
    CORSAIR_IRONCLAW_RGB = "Corsair Ironclaw RGB"
    BENQ_ZOWIE_EVO_FK2 = "BenQ Zowie Evo FK2"
    ASUS_ROG_GLADIUS_II = "ASUS ROG Gladius II"
    COOLER_MASTER_MM710 = "Cooler Master MM710"
    HYPERX_PULSEFIRE_SENSEI = "HyperX Pulsefire Sensei"
    LOGITECH_G_PRO_WIRELESS = "Logitech G Pro Wireless"
    FINALMOUSE_ULTRALIGHT_2 = "FinalMouse Ultralight 2"


class PrinterModels(StrEnum):
    """Models of printers enumeration."""
    HP_OFFICEJET_PRO_9015E = "HP OfficeJet Pro 9015e"
    CANON_PIXMA_TR4520 = "Canon PIXMA TR4520"
    BROTHER_HL_L2350DW = "Brother HL-L2350DW"
    EPSON_WORKFORCE_WF_2830 = "Epson WorkForce WF-2830"
    SAMSUNG_XPRESS_M2020W = "Samsung Xpress M2020W"
    LEXMARK_B2236DW = "Lexmark B2236dw"
    KYOCERA_ECOSYS_P2040DW = "Kyocera ECOSYS P2040dw"
    RICOH_SP_150SU = "Ricoh SP 150SU"
    XEROX_PHASER_3260 = "Xerox Phaser 3260"
    DELL_E310DW = "Dell E310dw"


class TabletModels(StrEnum):
    """Enumeration for tablet models."""
    IPAD_PRO_11 = "iPad Pro 11"
    SAMSUNG_GALAXY_TAB_S7 = "Samsung Galaxy Tab S7"
    AMAZON_FIRE_HD_10 = "Amazon Fire HD 10"
    MICROSOFT_SURFACE_PRO_7 = "Microsoft Surface Pro 7"
    LENOVO_TAB_P11_PRO = "Lenovo Tab P11 Pro"
    ASUS_ZENPAD_3S_10 = "ASUS ZenPad 3S 10"
    HUAWEI_MATEPAD_PRO = "Huawei MatePad Pro"
    DELL_VENUE_10_PRO = "Dell Venue 10 Pro"
    GOOGLE_PIXEL_SLATE = "Google Pixel Slate"
    CHUWI_HI10_X = "Chuwi Hi10 X"


class SmartwatchModels(StrEnum):
    """Enumeration for smartwatch models."""
    APPLE_WATCH_SERIES_7 = "Apple Watch Series 7"
    SAMSUNG_GALAXY_WATCH_4 = "Samsung Galaxy Watch 4"
    FITBIT_SENSE = "Fitbit Sense"
    GARMIN_VIVOACTIVE_4 = "Garmin Venu Sq"
    AMAZFIT_GTS_2 = "Amazfit GTS 2"
    SUUNTO_7 = "Suunto 7"
    TICWATCH_PRO_3 = "TicWatch Pro 3"
    WITHINGS_SCANWATCH = "Withings ScanWatch"
    FOSSIL_GEN_5 = "Fossil Gen 5"
    MOBVOI_TICWATCH_E3 = "Mobvoi TicWatch E3"


class CameraModels(StrEnum):
    """Enumeration for camera models."""
    CANON_EOS_R5 = "Canon EOS R5"
    NIKON_Z7_II = "Nikon Z7 II"
    SONY_A7R_IV = "Sony A7R IV"
    FUJIFILM_X_T4 = "Fujifilm X-T4"
    OLYMPUS_OM_D_E_M1_MARK_III = "Olympus OM-D E-M1 Mark III"
    PANASONIC_LUMIX_S5 = "Panasonic Lumix S5"
    LEICA_SL2 = "Leica SL2"
    PENTAX_K1_MARK_II = "Pentax K-1 Mark II"
    SIGMA_FP = "Sigma fp"
    RICOH_GR_III = "Ricoh GR III"
