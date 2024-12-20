from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QLabel, 
    QStackedWidget, QGridLayout, 
    QTableWidget, QTableWidgetItem, QDialog,
    QComboBox
)
import psycopg2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database.conn import DatabaseConnection
from config.settings import FontLoader, Settings
from components.input import Input
from components.label import Label
from components.button import Button
from components.room_box_owner import RoomBoxOwner
from config import session
from dialog.dormitory_input_dialog import DormitoryInputDialog
from controller.index import (
    DormitoryController, 
    DormitoryTypeController,
    OwnerController
)
from utils.utils import formatCurrency

class OwnerDashboardPage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('mainWindow')

        # Load Fonts
        FontLoader.load_fonts()


        self.session = session.get_user_info()

        self.db = DatabaseConnection()
        self.dormitory_controller = DormitoryController()
        self.dormitory_type_controller = DormitoryTypeController()
        self.owner_controller = OwnerController()
        # Initialize UI
        self.init_ui()



    def switch_page(self, index):
        """Switch the main content page."""
        self.content_stack.setCurrentIndex(index)

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                color: white;
                min-width: 250px;
                max-width: 250px;
                border: 1px solid #E4E7EC;
            }
            QPushButton {
                background-color: #F5F5FF;
                color: #101928;
                padding: 10px 8px;
                text-align: left;
                font-weight: medium;
                font-size: 12px;
                border-radius: 5px;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)
        sidebar.setLayout(layout)

        # Add navigation buttons
        buttons = [
            ("Dashboard", 0),
            ("Dormitories", 1),
            ("Manage Dormitory", 2)
            # ("Properti Saya", 1),
            # ("Fitur Promosi", 2),
            # ("Laporan Statistik", 3),
            # ("Akun", 4),
        ]
        for text, index in buttons:
            button = QPushButton(f"  {text}")  # Add space for better alignment
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, idx=index: self.switch_page(idx))
            layout.addWidget(button)

        layout.addStretch()
        return sidebar

    def create_content_pages(self):
        """Create different pages for the content area."""
        self.content_stack = QStackedWidget()
        self.content_stack.setContentsMargins(20, 20, 20, 20)

        # Home Page
        home_page = self.create_home_page()
        self.content_stack.addWidget(home_page)

        # Property Management Page
        property_page = self.create_dormitories_page()
        self.content_stack.addWidget(property_page)

        # Promotion Features Page
        promo_page = self.create_manage_dormitory_page()
        self.content_stack.addWidget(promo_page)

        # Statistics Report Page
        stats_page = self.create_stats_page()
        self.content_stack.addWidget(stats_page)

        # Account Page
        account_page = self.create_account_page()
        self.content_stack.addWidget(account_page)

        return self.content_stack

    def create_home_page(self):
        """Create the Home page."""
        page = QFrame()
        layout = QVBoxLayout()

        page.setLayout(layout)
        heading = Label(
            f"Halo, {self.session.get("username")}",
            font_size=20,
            font_weights=Settings.FONT_WEIGHTS['bold']
        )

       
        layout.addWidget(heading)
        layout.addStretch()
        return page

    def create_dormitories_page(self):  
        """Create the Property Management page."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)

        heading = Label(
            "List Dormitories",
            font_size=20,
            font_weights=Settings.FONT_WEIGHTS['bold']
        )
        layout.setSpacing(25)
        layout.addWidget(heading)
        
        dormitories = self.dormitory_controller.index()
      
        for dormitory in dormitories:
            room_box = RoomBoxOwner(
                image_path=dormitory["image_path"],
                title=dormitory["dorm_name"],
                description="Kamar luas dengan fasilitas lengkap.",
                price=formatCurrency(dormitory["dorm_price"], True)
            )
            layout.addWidget(room_box)
        layout.addStretch()
        return page

    def create_manage_dormitory_page(self):
        """Create the page to manage dormitory data."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)

        # Heading
        heading = Label("Manage Dormitory Data")
        heading.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(heading)

        # Add Button
        add_button = Button("Add Dormitory")
        add_button.clicked.connect(self.add_dormitory)
        layout.addWidget(add_button)

        # Table for Dormitory Data
        self.dormitory_table = QTableWidget()
        self.dormitory_table.setColumnCount(8)
        self.dormitory_table.setHorizontalHeaderLabels(
            ["Dormitroy Name", "Dormitory Type", "Dormitory Address", "Total Room", "Empty Room"]
        )

        self.dormitory_table.setColumnWidth(0, 200)  
        self.dormitory_table.setColumnWidth(1, 180)  
        self.dormitory_table.setColumnWidth(2, 260) 
        self.dormitory_table.setColumnWidth(3, 170)  
        self.dormitory_table.setColumnWidth(4, 170)  
    

        self.dormitory_table.verticalHeader().setDefaultSectionSize(35)

        layout.addWidget(self.dormitory_table)

        self.load_dormitory_data()

        return page

    def load_dormitory_data(self):
  
        """Load dormitory data into the table."""
        dormitories = self.owner_controller.dormitories()
        self.dormitory_table.setRowCount(0)
        for row_num, dorm in enumerate(dormitories):
            self.dormitory_table.insertRow(row_num)
            for col_num, data in enumerate(dorm):
                self.dormitory_table.setItem(row_num, col_num, QTableWidgetItem(str(dorm[data])))

            # Add Edit and Delete buttons
            # edit_button = Button("Edit")
            # edit_button.clicked.connect(lambda _, d=dorm: self.open_edit_dialog(d))

            # delete_button = Button("Delete")
            # delete_button.clicked.connect(lambda _, d=dorm: self.delete_dormitory(d[0]))

            # action_layout = QHBoxLayout()
            # action_layout.addWidget(edit_button)
            # action_layout.addWidget(delete_button)

            # action_widget = QWidget()
            # action_widget.setLayout(action_layout)
            # self.dormitory_table.setCellWidget(row_num, 8, action_widget)

    def add_dormitory(self):
        """Open a dialog to add a new dormitory."""

        # Load dormitory types for the dialog

        dormitory_types = self.dormitory_type_controller.index()
        dialog = DormitoryInputDialog(dormitory_types, self)
        if dialog.exec():
            request = dialog.get_inputs()
            print(request)

            dormitories = self.dormitory_controller.store({
                "dorm_type_id": request["dorm_type_id"],
                "user_id": self.session.get("user_id"),
                "name": request["name"],
                "address": request["address"],
                "price": request["price"],
                "total_room": request["total_room"],
                "empty_room": request["empty_room"],
                "image_path": request["image_path"]
            })

            print("Successfully!")
            self.load_dormitory_data()
      

    def open_edit_dialog(self, dorm):
        """Open a dialog to edit dormitory data."""
        # Load dormitory types for the dialog
        self.conn.cursor.execute("SELECT id, name FROM public.dorm_type ORDER BY id ASC")
        dorm_types = self.conn.cursor.fetchall()

        dialog = DormitoryInputDialog(dorm_types, self)
        dialog.name_input.setText(dorm[1])  # Set current values
        dialog.address_input.setText(dorm[3])
        dialog.price_input.setText(str(dorm[2]))
        dialog.total_room_input.setText(str(dorm[4]))
        dialog.empty_room_input.setText(str(dorm[5]))
        dialog.type_selector.setCurrentIndex(dialog.type_selector.findData(dorm[6]))

        if dialog.exec():
            inputs = dialog.get_inputs()
            try:
                query = '''
                UPDATE dormitory
                SET dorm_type_id = %s, name = %s, address = %s, price = %s, total_room = %s, empty_room = %s, image_path = %s
                WHERE id = %s
                '''
                self.conn.cursor.execute(
                    query, (
                        inputs["dorm_type_id"], inputs["name"], inputs["address"],
                        inputs["price"], inputs["total_rooms"], inputs["empty_rooms"],
                        inputs["image_path"], dorm[0]
                    )
                )
                self.conn.connection.commit()
                print("Dormitory updated successfully!")
                self.load_dormitory_data()
            except psycopg2.Error as e:
                print("Database Error: ", e)

    def delete_dormitory(self, dorm_id):
        """Delete a dormitory record."""
        query = "DELETE FROM dormitory WHERE id = %s"
        self.conn.cursor.execute(query, (dorm_id,))
        self.conn.connection.commit()
        print("Dormitory deleted!")
        self.load_dormitory_data()

    def open_edit_dialog(self, dorm):
        """Open a dialog to edit dormitory data."""
        dialog = QDialog()
        dialog.setWindowTitle("Edit Dormitory")
        dialog.setModal(True)
        layout = QVBoxLayout()

        # Input Fields
        name_input = QLineEdit(dorm[1])
        owner_input = QLineEdit(dorm[2])
        phone_input = QLineEdit(dorm[3])

        save_button = Button("Save")
        save_button.clicked.connect(
            lambda: self.save_edited_data(dialog, dorm[0], name_input.text(), owner_input.text(), phone_input.text())
        )

        layout.addWidget(Label("Dormitory Name"))
        layout.addWidget(name_input)
        layout.addWidget(Label("Owner Name"))
        layout.addWidget(owner_input)
        layout.addWidget(Label("Phone Number"))
        layout.addWidget(phone_input)
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec()

    def save_edited_data(self, dialog, dorm_id, name, owner, phone):
        """Save edited dormitory data to the database."""
        query = '''
        UPDATE dormitory
        SET name = %s, user_id = (SELECT id FROM public."user" WHERE name = %s AND phone_number = %s)
        WHERE id = %s
        '''
        self.conn.cursor.execute(query, (name, owner, phone, dorm_id))
        self.conn.connection.commit()
        print("Dormitory updated successfully!")
        self.load_dormitory_data()
        dialog.close()

    def create_stats_page(self):
        """Create the Statistics Report page."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)
        layout.addWidget(Label("Statistics Report Page"))
        return page

    def create_account_page(self):
        """Create the Account page."""
        page = QFrame()
        layout = QVBoxLayout()
        page.setLayout(layout)
        layout.addWidget(Label("Account Management Page"))
        return page

    def init_ui(self):
        """Initialize the main UI layout."""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Main content area with stack
        content_stack = self.create_content_pages()
        main_layout.addWidget(content_stack)
