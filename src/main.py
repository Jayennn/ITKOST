import sys
from PyQt6.QtWidgets import QApplication
from config.settings import FontLoader, Settings
from pages.home_page import HomePage
from pages.owner.owner_dashboard_page import OwnerDashboardPage
class App(QApplication):
    def __init__(self, argv):
        """Initialize the application."""
        super().__init__(argv)
        self.load_fonts()
        self.apply_global_styles()

    def load_fonts(self):
        """Load custom fonts for the application."""
        FontLoader.load_fonts()

    def apply_global_styles(self):
        """Apply global styles from the CSS file."""
        try:
            with open('./src/styles/global.css', 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Error: Global stylesheet not found.")

def main():
    """Main entry point of the application."""
    app = App(sys.argv)

    # Launch the program        
    window = HomePage()
    window.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
    window.show()

    # Execute the application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
