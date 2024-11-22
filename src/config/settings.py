from PyQt6.QtGui import QFontDatabase, QFont

class Settings:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    FONT_FAMILY = "Be Vietnam Pro"
    PRIMARY_COLOR = "#1A1A1A"
    SECONDARY_COLOR = "#666666"
    BACKGROUND_COLOR = "#FFFFFF"
    
    FONT_WEIGHTS = {
        "thin": 100,
        "light": 300,
        "regular": 400,
        "medium": 500,
        'semi-bold': 600,
        "bold": 700,
        "black": 800
    }

class FontLoader:
    @staticmethod
    def load_fonts():
        font_files = {
            "BeVietnamPro-Thin.ttf": QFont.Weight.Thin,
            "BeVietnamPro-Light.ttf": QFont.Weight.Light,
            "BeVietnamPro-Regular.ttf": QFont.Weight.Normal,
            "BeVietnamPro-Medium.ttf": QFont.Weight.Medium,
            "BeVietnamPro-SemiBold.ttf": QFont.Weight.DemiBold,
            "BeVietnamPro-Bold.ttf": QFont.Weight.Bold,
            "BeVietnamPro-Black.ttf": QFont.Weight.Black,
        }
        
        for font_file, weight in font_files.items():
            try:
                font_id = QFontDatabase.addApplicationFont(f"./src/assets/fonts/{font_file}")
                if font_id < 0:
                    print(f"Failed to load font: {font_file}")
            except Exception as e:
                print(f"Error loading font {font_file}: {e}")