import os
import sys
import webbrowser
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QCheckBox, QScrollArea, QFrame, QLineEdit,
    QMessageBox, QFileDialog, QColorDialog, QTabWidget, QTextEdit,
    QDialog, QDialogButtonBox, QComboBox, QGroupBox, QSizePolicy,
    QSpacerItem, QGridLayout, QMenu, QMenuBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon, QPainter, QAction, QPainterPath
from PyQt6.QtSvg import QSvgRenderer

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def load_pixmap(filename):
    try:
        path = resource_path(filename)
        if os.path.exists(path):
            return QPixmap(path)
        else:
            return QPixmap(filename)
    except Exception:
        return QPixmap()

def load_icon(filename):
    try:
        path = resource_path(filename)
        if os.path.exists(path):
            return QIcon(path)
        else:
            return QIcon(filename)
    except Exception:
        return QIcon()

class ModernButton(QPushButton):
    def __init__(self, text, color="#2196F3", icon=None, height=40):
        super().__init__(text)
        self.setFixedHeight(height)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {self._darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color, 30)};
            }}
        """)
        if icon:
            self.setIcon(QIcon(icon))

    def _darken_color(self, color, percent=15):
        try:
            color = QColor(color)
            r = max(0, color.red() - percent)
            g = max(0, color.green() - percent)
            b = max(0, color.blue() - percent)
            return f"rgb({r}, {g}, {b})"
        except:
            return color

class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            ModernCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                margin: 8px 8px 8px 8px;
                padding: 0px;
            }
        """)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)

class TaskCard(ModernCard):
    def __init__(self, task_data, index, font_size=11, strikethrough=True):
        super().__init__()
        self.task_data = task_data
        self.index = index
        self.font_size = font_size
        self.strikethrough = strikethrough
        self.subtask_vars = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: transparent;")
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_color = self.task_data.get('base_color', '#2E86AB')
        if title_color == 'default':
            title_color = '#2E86AB' if self.task_data.get('link') else '#1a1a1a'

        title_font_size = self.font_size + 3

        self.title_label = QLabel(self.task_data['name'])
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {title_color};
                font-size: {title_font_size}px;
                font-weight: bold;
                background-color: transparent;
                padding: 4px 0px;
            }}
        """)
        self.title_label.setWordWrap(True)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        if self.task_data.get('link'):
            self.title_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.title_label.mousePressEvent = lambda e: self.open_task()

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        layout.addWidget(title_frame)

        for i, subtask in enumerate(self.task_data['sub_tasks']):
            self.create_subtask(layout, subtask, i)

    def create_subtask(self, layout, text, index):
        subtask_frame = QFrame()
        subtask_frame.setStyleSheet("background-color: transparent;")
        subtask_layout = QHBoxLayout(subtask_frame)
        subtask_layout.setContentsMargins(0, 0, 0, 0)
        subtask_layout.setSpacing(10)

        checkbox = QCheckBox()
        checkbox.setFixedSize(20, 20)
        color = self.task_data.get('selected_color', '#4CAF50')
        if color == 'default':
            color = '#4CAF50'
            
        checkbox.setStyleSheet(f"""
            QCheckBox {{
                background-color: transparent;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
                border: 2px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                background-color: {color};
                border: 2px solid {color};
                image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='white' d='M10.28 2.28L4.5 8.06 1.72 5.28a1 1 0 00-1.41 1.41l3.35 3.36a1 1 0 001.41 0l6.36-6.36a1 1 0 10-1.41-1.41z'/></svg>");
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: {self._darken_color(color)};
                border: 2px solid {self._darken_color(color)};
            }}
        """)
        
        subtask_label = QLabel(text)
        subtask_label.setStyleSheet(f"""
            QLabel {{
                color: #333333;
                font-size: {self.font_size}px;
                background-color: transparent;
                padding: 2px 0px;
            }}
        """)
        subtask_label.setWordWrap(True)
        subtask_label.setCursor(Qt.CursorShape.PointingHandCursor)
        subtask_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        subtask_widget = {
            'checkbox': checkbox,
            'label': subtask_label,
            'original_text': text
        }
        self.subtask_vars.append(subtask_widget)

        checkbox.stateChanged.connect(
            lambda state, widget=subtask_widget: self.update_subtask_style(widget)
        )

        subtask_label.mousePressEvent = lambda e, cb=checkbox: cb.setChecked(not cb.isChecked())

        subtask_layout.addWidget(checkbox)
        subtask_layout.addWidget(subtask_label, 1)
        layout.addWidget(subtask_frame)

    def _darken_color(self, color, percent=15):
        try:
            color = QColor(color)
            r = max(0, color.red() - percent)
            g = max(0, color.green() - percent)
            b = max(0, color.blue() - percent)
            return f"rgb({r}, {g}, {b})"
        except:
            return color

    def update_subtask_style(self, widget):
        checked = widget['checkbox'].isChecked()
        color = self.task_data.get('selected_color', '#4CAF50')
        if color == 'default':
            color = '#4CAF50'

        if checked and self.strikethrough:
            widget['label'].setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: {self.font_size}px;
                    text-decoration: line-through;
                    background-color: transparent;
                    padding: 2px 0px;
                }}
            """)
        else:
            widget['label'].setStyleSheet(f"""
                QLabel {{
                    color: {'#333333' if not checked else color};
                    font-size: {self.font_size}px;
                    background-color: transparent;
                    padding: 2px 0px;
                }}
            """)

    def open_task(self):
        link = self.task_data.get('link', '')
        if link:
            try:
                if os.path.exists(link):
                    os.startfile(link)
                else:
                    webbrowser.open(link)
            except Exception as e:
                print(f"Error opening {link}: {e}")

class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)

        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        logo_label = QLabel()
        logo_pixmap = load_pixmap("todo1.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("📝")
            logo_label.setStyleSheet("font-size: 48px; color: #2E86AB;")
        
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(logo_label)

        title_label = QLabel("✔️ Simply TodoTask")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #2E86AB;
                background-color: transparent;
                padding: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        welcome_text = QLabel(
            "Welcome to Simply TodoTask!\n\n"
            "To get started, load an existing list\n"
            "or create a new one by clicking on Customize"
        )
        welcome_text.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #555555;
                background-color: transparent;
                text-align: center;
                line-height: 1.4;
            }
        """)
        welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_text)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        load_btn = ModernButton("📂 Load TodoTask List", "#2196F3", height=50)
        personalize_btn = ModernButton("🎯 Create / Customize Todo", "#4CAF50", height=50)

        button_layout.addWidget(load_btn)
        button_layout.addWidget(personalize_btn)

        layout.addLayout(button_layout)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version_label = QLabel("Simply TodoTask v0.1")
        version_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #333333;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        author_label = QLabel("Created with ♥ by Daniele Borghi")
        author_label.setStyleSheet("font-size: 11px; color: #2E86AB;")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        github_label = QLabel("Visit my GITHUB repository for more information!")
        github_label.setStyleSheet("font-size: 11px; color: #666666;")
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github_label.setCursor(Qt.CursorShape.PointingHandCursor)
        github_label.mousePressEvent = lambda e: webbrowser.open("https://github.com/danjiss/Simply-TodoTask-Checklist")

        date_label = QLabel(f"Update: Nov. 2025")
        date_label.setStyleSheet("font-size: 10px; color: #888888;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(version_label)
        info_layout.addWidget(author_label)
        info_layout.addWidget(github_label)
        info_layout.addWidget(date_label)

        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addLayout(info_layout)

        self.load_btn = load_btn
        self.personalize_btn = personalize_btn

class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save List")
        self.setFixedSize(400, 180)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 12px;
            }
        """)
        self.setWindowIcon(load_icon("todo.ico"))
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(25, 25, 25, 25)

        message = QLabel("How do you want to save the list?")
        message.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                text-align: center;
            }
        """)
        layout.addWidget(message)

        button_layout = QHBoxLayout()
        
        save_btn = ModernButton("💾 Save", "#2196F3", height=45)
        save_as_btn = ModernButton("📁 Save as new", "#4CAF50", height=45)
        cancel_btn = ModernButton("❌ Cancel", "#757575", height=45)

        save_btn.clicked.connect(lambda: self.done(1))
        save_as_btn.clicked.connect(lambda: self.done(2))
        cancel_btn.clicked.connect(lambda: self.done(0))

        button_layout.addWidget(save_btn)
        button_layout.addWidget(save_as_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

class ResetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reset Task")
        self.setFixedSize(400, 180)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 12px;
            }
        """)
        self.setWindowIcon(load_icon("todo.ico"))
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        message = QLabel("What do you want to reset?")
        message.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                text-align: center;
            }
        """)
        layout.addWidget(message)

        button_layout = QHBoxLayout()
        
        reset_checks_btn = ModernButton("🔄 Reset Checks", "#2196F3", height=45)
        reset_tasks_btn = ModernButton("🗑 Reset To-Do", "#f44336", height=45)
        cancel_btn = ModernButton("❌ Cancel", "#757575", height=45)

        reset_checks_btn.clicked.connect(lambda: self.done(1))
        reset_tasks_btn.clicked.connect(lambda: self.done(2))
        cancel_btn.clicked.connect(lambda: self.done(0))

        button_layout.addWidget(reset_checks_btn)
        button_layout.addWidget(reset_tasks_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

class CustomizeDialog(QDialog):
    def __init__(self, parent, tasks, current_file_path, settings):
        super().__init__(parent)
        self.parent = parent
        self.tasks = tasks.copy()
        self.current_file_path = current_file_path
        self.settings = settings.copy()
        self.task_widgets = []
        self.setup_ui()
        self.setWindowIcon(load_icon("todo.ico"))

    def setup_ui(self):
        self.setWindowTitle("Customize To-Do")
        self.setMinimumSize(950, 750)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("🎯 Customize To-Do List")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2E86AB;
                padding: 10px 0px;
                background-color: transparent;
            }
        """)
        layout.addWidget(title_label)

        if self.current_file_path:
            file_info = QLabel(f"📄 Current file: {self.current_file_path}")
            file_info.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #666666;
                    background-color: #e3f2fd;
                    padding: 8px 12px;
                    border-radius: 6px;
                    border: 1px solid #bbdefb;
                }
            """)
            file_info.setWordWrap(True)
            layout.addWidget(file_info)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                border-radius: 8px;
                background-color: white;
                margin-top: 5px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                margin-right: 3px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                color: #555555;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2E86AB;
                border-bottom: 2px solid #2E86AB;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
        """)

        self.setup_general_tab()
        self.setup_tasks_tab()
        self.setup_file_tab()

        layout.addWidget(self.tab_widget, 1)

        button_layout = QHBoxLayout()

        load_btn = ModernButton("📂 Load List", "#FF9800", height=45)
        reset_btn = ModernButton("🔄 Reset To-Do", "#f44336", height=45)
        cancel_btn = ModernButton("❌ Cancel", "#757575", height=45)
        save_btn = ModernButton("💾 Save Changes", "#2196F3", height=45)

        button_layout.addWidget(load_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

        load_btn.clicked.connect(self.load_configuration)
        reset_btn.clicked.connect(self.show_reset_dialog)
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self.show_save_dialog)

    def setup_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        group = ModernCard()
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(12)
        group_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("⚙️ List Settings")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E86AB;
                padding-bottom: 5px;
                border-bottom: 2px solid #e0e0e0;
            }
        """)
        group_layout.addWidget(title_label)

        title_row = QHBoxLayout()
        title_label = QLabel("Title:")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.title_edit = QLineEdit(self.settings.get('title', 'Simply TodoTask'))
        self.title_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #cccccc;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
        title_row.addWidget(title_label)
        title_row.addWidget(self.title_edit, 1)
        group_layout.addLayout(title_row)

        font_row = QHBoxLayout()
        font_label = QLabel("Font size:")
        font_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.font_combo = QComboBox()
        self.font_combo.addItems(["small", "medium", "large"])
        current_font = self.settings.get('font_size', 'medium')
        current_font = 'small' if current_font == 'piccolo' else 'medium' if current_font == 'medio' else 'large'
        self.font_combo.setCurrentText(current_font)
        self.font_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #cccccc;
                border-radius: 6px;
                font-size: 12px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #2196F3;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 6px;
                outline: none;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border: none;
                color: #333333;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #2196F3;
                color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #e3f2fd;
                color: #333333;
            }
        """)
        font_row.addWidget(font_label)
        font_row.addWidget(self.font_combo)
        font_row.addStretch()
        group_layout.addLayout(font_row)

        self.strikethrough_check = QCheckBox("Show strikethrough for completed tasks")
        self.strikethrough_check.setChecked(self.settings.get('strikethrough', True))
        self.strikethrough_check.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                font-weight: bold;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
                image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='white' d='M10.28 2.28L4.5 8.06 1.72 5.28a1 1 0 00-1.41 1.41l3.35 3.36a1 1 0 001.41 0l6.36-6.36a1 1 0 10-1.41-1.41z'/></svg>");
            }
        """)
        group_layout.addWidget(self.strikethrough_check)

        layout.addWidget(group)
        layout.addStretch()

        self.tab_widget.addTab(tab, "⚙️ Settings")

    def setup_tasks_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.scroll_widget = QWidget()
        self.tasks_layout = QVBoxLayout(self.scroll_widget)
        self.tasks_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tasks_layout.setSpacing(0)

        self.refresh_tasks_layout()

        scroll.setWidget(self.scroll_widget)
        layout.addWidget(scroll, 1)

        add_btn = ModernButton("➕ Add New To-Do", "#4CAF50", height=45)
        add_btn.clicked.connect(self.add_new_task)
        layout.addWidget(add_btn)

        self.tab_widget.addTab(tab, "📋 Manage To-Do")

    def refresh_tasks_layout(self):
        for i in reversed(range(self.tasks_layout.count())):
            item = self.tasks_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        self.task_widgets = []
        
        for i, task in enumerate(self.tasks):
            self.add_task_widget(i, task)

        if not self.tasks:
            no_tasks_label = QLabel("No To-Do present. Click 'Add New To-Do' to get started!")
            no_tasks_label.setStyleSheet("""
                QLabel {
                    font-size: 14px; 
                    color: #666666; 
                    text-align: center;
                    padding: 40px;
                    background-color: white;
                    border-radius: 8px;
                    border: 2px dashed #cccccc;
                }
            """)
            no_tasks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tasks_layout.addWidget(no_tasks_label)

    def setup_file_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        group = ModernCard()
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(15)
        group_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("💾 File Management")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2E86AB;
                padding-bottom: 5px;
                border-bottom: 2px solid #e0e0e0;
            }
        """)
        group_layout.addWidget(title_label)

        file_layout = QVBoxLayout()
        file_label = QLabel("Current file:")
        file_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #333333;")
        
        file_text = self.current_file_path if self.current_file_path else "No file loaded"
        self.file_label = QLabel(file_text)
        self.file_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #666666;
                background-color: #f5f5f5;
                padding: 10px 12px;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
            }
        """)
        self.file_label.setWordWrap(True)
        
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_label)
        group_layout.addLayout(file_layout)

        if self.current_file_path:
            unload_btn = ModernButton("🗑️ Remove Current File", "#ff6b6b", height=45)
            unload_btn.clicked.connect(self.unload_file)
            group_layout.addWidget(unload_btn)

        layout.addWidget(group)
        layout.addStretch()

        self.tab_widget.addTab(tab, "💾 File")

    def add_task_widget(self, index, task_data):
        task_card = ModernCard()
        task_layout = QVBoxLayout(task_card)
        task_layout.setSpacing(0)
        task_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        
        task_number = QLabel(f"📝 To-Do #{index + 1}")
        task_number.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2E86AB;
            }
        """)
        
        header_layout.addWidget(task_number)
        header_layout.addStretch()
        
        delete_btn = QPushButton("🗑 Delete")
        delete_btn.setFixedSize(80, 30)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_task(index))
        header_layout.addWidget(delete_btn)

        task_layout.addLayout(header_layout)

        details_card = ModernCard()
        details_card.setStyleSheet("ModernCard { background-color: #f8f9fa; }")
        details_layout = QVBoxLayout(details_card)
        details_layout.setContentsMargins(15, 15, 15, 15)
        details_layout.setSpacing(10)

        title_row = QHBoxLayout()
        title_label = QLabel("Title:")
        title_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #555555;")
        name_edit = QLineEdit(task_data['name'])
        name_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #cccccc;
                border-radius: 6px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
        title_row.addWidget(title_label)
        title_row.addWidget(name_edit, 1)
        details_layout.addLayout(title_row)

        link_row = QHBoxLayout()
        link_label = QLabel("Link (optional):")
        link_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #555555;")
        
        link_edit = QLineEdit(task_data.get('link', ''))
        link_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #cccccc;
                border-radius: 6px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
        browse_btn = ModernButton("Browse", "#E0E0E0", height=35)
        browse_btn.setStyleSheet(browse_btn.styleSheet() + "color: #333333;")
        browse_btn.clicked.connect(lambda: self.browse_file(link_edit))
        
        link_row.addWidget(link_label)
        link_row.addWidget(link_edit, 1)
        link_row.addWidget(browse_btn)
        details_layout.addLayout(link_row)

        task_layout.addWidget(details_card)

        subtasks_card = ModernCard()
        subtasks_card.setStyleSheet("ModernCard { background-color: #f8f9fa; }")
        subtasks_layout = QVBoxLayout(subtasks_card)
        subtasks_layout.setContentsMargins(15, 15, 15, 15)

        subtasks_title = QLabel("📋 Tasks:")
        subtasks_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #555555; margin-bottom: 8px;")
        subtasks_layout.addWidget(subtasks_title)

        subtasks_container = QWidget()
        subtasks_container_layout = QVBoxLayout(subtasks_container)
        subtasks_container_layout.setSpacing(8)
        subtasks_container_layout.setContentsMargins(0, 0, 0, 0)

        task_entries = []
        for subtask in task_data['sub_tasks']:
            self.add_subtask_entry(subtasks_container_layout, task_entries, subtask)

        subtasks_layout.addWidget(subtasks_container)

        add_subtask_btn = ModernButton("➕ Add Task", "#E0E0E0", height=35)
        add_subtask_btn.setStyleSheet(add_subtask_btn.styleSheet() + "color: #333333;")
        add_subtask_btn.clicked.connect(lambda: self.add_subtask_entry(subtasks_container_layout, task_entries))
        subtasks_layout.addWidget(add_subtask_btn)

        task_layout.addWidget(subtasks_card)

        colors_card = ModernCard()
        colors_card.setStyleSheet("ModernCard { background-color: #f8f9fa; }")
        colors_layout = QVBoxLayout(colors_card)
        colors_layout.setContentsMargins(15, 15, 15, 15)
        
        colors_title = QLabel("🎨 Color Customization")
        colors_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #555555; margin-bottom: 8px;")
        colors_layout.addWidget(colors_title)

        colors_row = QHBoxLayout()
        colors_row.setSpacing(20)

        base_color_layout = QHBoxLayout()
        base_color_label = QLabel("Title color:")
        base_color_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #666666;")
        base_color_btn = QPushButton()
        base_color_btn.setFixedSize(30, 30)
        base_color = task_data.get('base_color', 'default')
        base_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#1a1a1a' if base_color == 'default' else base_color};
                border: 2px solid #cccccc;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                border-color: #2196F3;
            }}
        """)
        base_color_btn.clicked.connect(lambda: self.choose_color(index, 'base', base_color_btn))
        base_color_layout.addWidget(base_color_label)
        base_color_layout.addWidget(base_color_btn)
        base_color_layout.addStretch()
        colors_row.addLayout(base_color_layout)

        selected_color_layout = QHBoxLayout()
        selected_color_label = QLabel("Completed color:")
        selected_color_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #666666;")
        selected_color_btn = QPushButton()
        selected_color_btn.setFixedSize(30, 30)
        selected_color = task_data.get('selected_color', 'default')
        selected_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#4CAF50' if selected_color == 'default' else selected_color};
                border: 2px solid #cccccc;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                border-color: #2196F3;
            }}
        """)
        selected_color_btn.clicked.connect(lambda: self.choose_color(index, 'selected', selected_color_btn))
        selected_color_layout.addWidget(selected_color_label)
        selected_color_layout.addWidget(selected_color_btn)
        selected_color_layout.addStretch()
        colors_row.addLayout(selected_color_layout)

        colors_row.addStretch()
        colors_layout.addLayout(colors_row)
        task_layout.addWidget(colors_card)

        widget_data = {
            'widget': task_card,
            'name_edit': name_edit,
            'link_edit': link_edit,
            'base_color_btn': base_color_btn,
            'selected_color_btn': selected_color_btn,
            'task_entries': task_entries,
            'subtasks_container': subtasks_container,
            'subtasks_container_layout': subtasks_container_layout
        }
        self.task_widgets.append(widget_data)

        self.tasks_layout.addWidget(task_card)

    def add_subtask_entry(self, layout, task_entries, text=""):
        entry_widget = QWidget()
        entry_layout = QHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(0, 0, 0, 0)
        entry_layout.setSpacing(8)
        
        entry = QLineEdit(text)
        entry.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #cccccc;
                border-radius: 6px;
                font-size: 11px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
        
        delete_btn = QPushButton("❌")
        delete_btn.setFixedSize(25, 25)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        entry_layout.addWidget(entry, 1)
        entry_layout.addWidget(delete_btn)
        
        layout.addWidget(entry_widget)
        
        task_entries.append((entry_widget, entry))
        delete_btn.clicked.connect(lambda: self.delete_subtask_entry(entry_widget, entry, task_entries))

    def delete_subtask_entry(self, container, entry, task_entries):
        container.setParent(None)
        if (container, entry) in task_entries:
            task_entries.remove((container, entry))

    def add_new_task(self):
        new_task = {
            "name": "New To-Do",
            "sub_tasks": ["New task"],
            "base_color": "default",
            "selected_color": "default",
            "link": ""
        }
        self.tasks.append(new_task)
        self.refresh_tasks_layout()

    def delete_task(self, index):
        reply = QMessageBox.question(
            self, "Delete To-Do",
            f"Are you sure you want to delete To-Do #{index + 1}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.tasks.pop(index)
            self.refresh_tasks_layout()

    def choose_color(self, index, color_type, button):
        current_color = self.tasks[index].get(f"{color_type}_color", "default")
        if current_color != "default":
            initial = QColor(current_color)
        else:
            initial = QColor("#1a1a1a" if color_type == "base" else "#4CAF50")
            
        color = QColorDialog.getColor(initial, self, f"Choose {color_type} color")
        if color.isValid():
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color.name()};
                    border: 2px solid #cccccc;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    border-color: #2196F3;
                }}
            """)
            self.tasks[index][f"{color_type}_color"] = color.name()

    def browse_file(self, link_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file")
        if file_path:
            link_edit.setText(file_path)

    def unload_file(self):
        reply = QMessageBox.question(
            self, "Remove File", 
            "Do you want to remove the current file from memory?\n\nThe current list will be cleared.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.current_file_path = None
            self.tasks = []
            self.task_widgets = []
            
            self.parent.current_file_path = None
            self.parent.tasks = []
            self.parent.settings = {
                "title": "Simply TodoTask",
                "font_size": "medium",
                "strikethrough": True
            }
            self.parent.show_welcome_screen()
            self.accept()

    def show_reset_dialog(self):
        dialog = ResetDialog(self)
        result = dialog.exec()
        
        if result == 1:
            self.reset_checks()
        elif result == 2:
            self.reset_tasks()

    def reset_checks(self):
        QMessageBox.information(self, "Reset Checks", "Checks will be reset when you save the changes.")

    def reset_tasks(self):
        self.tasks = []
        self.refresh_tasks_layout()

    def load_configuration(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load list", "", "Text files (*.txt);;All files (*.*)"
        )
        if file_path:
            try:
                tasks = []
                settings = {
                    "title": "Simply TodoTask",
                    "font_size": "medium",
                    "strikethrough": True
                }
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    current_task = None
                    i = 0
                    while i < len(lines):
                        line = lines[i].strip()
                        if line.startswith("[SETTINGS]"):
                            i += 1
                            while i < len(lines) and not lines[i].startswith("[TASK]") and lines[i].strip() != "":
                                line = lines[i].strip()
                                if line.startswith("title="):
                                    settings["title"] = line.split('=', 1)[1]
                                elif line.startswith("font_size="):
                                    font_size = line.split('=', 1)[1]
                                    if font_size in ['piccolo', 'medio', 'grande']:
                                        font_size = 'small' if font_size == 'piccolo' else 'medium' if font_size == 'medio' else 'large'
                                    settings["font_size"] = font_size
                                elif line.startswith("strikethrough="):
                                    settings["strikethrough"] = line.split('=', 1)[1].lower() == "true"
                                i += 1
                            continue
                        elif line.startswith("[TASK]"):
                            if current_task:
                                tasks.append(current_task)
                            current_task = {
                                "name": "",
                                "sub_tasks": [],
                                "base_color": "default",
                                "selected_color": "default",
                                "link": ""
                            }
                        elif line.startswith("name=") and current_task is not None:
                            current_task["name"] = line[5:]
                        elif line.startswith("base_color=") and current_task is not None:
                            current_task["base_color"] = line[11:]
                        elif line.startswith("selected_color=") and current_task is not None:
                            current_task["selected_color"] = line[15:]
                        elif line.startswith("link=") and current_task is not None:
                            current_task["link"] = line[5:]
                        elif line.startswith("sub_task=") and current_task is not None:
                            current_task["sub_tasks"].append(line[9:])
                        i += 1
                    
                    if current_task:
                        tasks.append(current_task)
                
                self.tasks = tasks
                self.current_file_path = file_path
                self.settings = settings
                
                self.file_label.setText(file_path)
                self.title_edit.setText(settings["title"])
                self.font_combo.setCurrentText(settings["font_size"])
                self.strikethrough_check.setChecked(settings["strikethrough"])
                
                self.refresh_tasks_layout()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot load the list: {e}")

    def show_save_dialog(self):
        if not self.current_file_path:
            self.save_as_configuration()
            return
            
        dialog = SaveDialog(self)
        result = dialog.exec()
        
        if result == 1:
            self._save_to_file(self.current_file_path)
        elif result == 2:
            self.save_as_configuration()

    def save_as_configuration(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save list", "", "Text files (*.txt);;All files (*.*)"
        )
        if file_path:
            self._save_to_file(file_path)

    def _save_to_file(self, file_path):
        try:
            tasks_to_save = []
            for i in range(len(self.tasks)):
                widgets = self.task_widgets[i]
                
                name = widgets['name_edit'].text().strip() or f"To-Do {i+1}"
                link = widgets['link_edit'].text().strip()
                
                base_color = self.tasks[i].get('base_color', 'default')
                selected_color = self.tasks[i].get('selected_color', 'default')
                
                sub_tasks = []
                for container, entry in widgets['task_entries']:
                    task_text = entry.text().strip()
                    if task_text:
                        sub_tasks.append(task_text)
                
                if not sub_tasks:
                    sub_tasks = ["New task"]
                
                task_to_save = {
                    "name": name,
                    "sub_tasks": sub_tasks,
                    "base_color": base_color,
                    "selected_color": selected_color,
                    "link": link
                }
                tasks_to_save.append(task_to_save)
            
            settings_to_save = {
                "title": self.title_edit.text(),
                "font_size": self.font_combo.currentText(),
                "strikethrough": self.strikethrough_check.isChecked()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("[SETTINGS]\n")
                f.write(f"title={settings_to_save['title']}\n")
                f.write(f"font_size={settings_to_save['font_size']}\n")
                f.write(f"strikethrough={settings_to_save['strikethrough']}\n")
                f.write("\n")
                
                for task in tasks_to_save:
                    f.write("[TASK]\n")
                    f.write(f"name={task['name']}\n")
                    f.write(f"base_color={task.get('base_color', 'default')}\n")
                    f.write(f"selected_color={task.get('selected_color', 'default')}\n")
                    f.write(f"link={task.get('link', '')}\n")
                    for sub_task in task['sub_tasks']:
                        f.write(f"sub_task={sub_task}\n")
                    f.write("\n")
            
            self.current_file_path = file_path
            self.file_label.setText(file_path)
            
            self.parent.tasks = tasks_to_save
            self.parent.settings = settings_to_save
            self.parent.current_file_path = file_path
            self.parent.refresh_tasks()
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot save the list: {e}")

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Information")
        self.setFixedSize(500, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
            }
        """)
        self.setWindowIcon(load_icon("todo.ico"))
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("✔️ Simply TodoTask")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2E86AB;
                text-align: center;
                padding: 10px 0px;
            }
        """)
        layout.addWidget(title_label)

        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(15)
        info_layout.setContentsMargins(20, 20, 20, 20)

        desc_label = QLabel(
            "This application helps you manage your tasks:\n\n"
            "• Create and customize your activity lists\n"
            "• Organize To-Dos with tasks and links\n"
            "• Save and load your lists in text format"

        )
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #333333;
                line-height: 1;
                background-color: transparent;
            }
        """)
        desc_label.setWordWrap(False)
        info_layout.addWidget(desc_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e0e0e0; margin: 10px 0px;")
        info_layout.addWidget(separator)

        dev_info = QLabel("👨‍💻 Developed by Daniele Borghi")
        dev_info.setStyleSheet("font-size: 12px; font-weight: bold; color: #2E86AB;")
        info_layout.addWidget(dev_info)

        version_info = QLabel("📦 Version: 0.1 (November 2025)")
        version_info.setStyleSheet("font-size: 11px; color: #666666;")
        info_layout.addWidget(version_info)

        layout.addWidget(info_card)

        github_btn = ModernButton("🐙 Visit repository on GitHub", "#333333", height=45)
        github_btn.clicked.connect(lambda: webbrowser.open("https://github.com/danjiss/Simply-TodoTask-Checklist"))
        layout.addWidget(github_btn)

        close_btn = ModernButton("Close", "#757575", height=45)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.current_file_path = None
        self.settings = {
            "title": "Simply TodoTask",
            "font_size": "medium",
            "strikethrough": True
        }
        self.setup_ui()
        self.show_welcome_screen()
        self.setWindowIcon(load_icon("todo.ico"))

    def setup_ui(self):
        self.setWindowTitle("Simply TodoTask")
        self.setGeometry(100, 100, 600, 850)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)

        self.setup_menu()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
                padding: 4px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #e3f2fd;
            }
            QMenu {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 24px 6px 12px;
            }
            QMenu::item:selected {
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
            }
        """)

        actions_menu = menubar.addMenu("Actions")
        
        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.show_reset_dialog)
        actions_menu.addAction(reset_action)
        
        personalize_action = QAction("Create To-Do", self)
        personalize_action.triggered.connect(self.customize_tasks)
        actions_menu.addAction(personalize_action)

        list_menu = menubar.addMenu("List")
        
        save_action = QAction("Save list", self)
        save_action.triggered.connect(self.save_configuration)
        list_menu.addAction(save_action)
        
        load_action = QAction("Load list", self)
        load_action.triggered.connect(self.load_configuration)
        list_menu.addAction(load_action)
        
        info_menu = menubar.addMenu("?")
        
        about_action = QAction("Information", self)
        about_action.triggered.connect(self.show_info_dialog)
        info_menu.addAction(about_action)
        
    def show_info_dialog(self):
        dialog = InfoDialog(self)
        dialog.exec()

    def show_welcome_screen(self):
        self.clear_layout(self.main_layout)

        welcome_screen = WelcomeScreen()
        welcome_screen.load_btn.clicked.connect(self.load_configuration)
        welcome_screen.personalize_btn.clicked.connect(self.customize_tasks)
        
        self.main_layout.addWidget(welcome_screen)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

    def refresh_tasks(self):
        self.clear_layout(self.main_layout)

        if not self.tasks:
            self.show_welcome_screen()
            return

        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2E86AB;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        header.setFixedHeight(90)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(15)
        
        icon_label = QLabel()
        icon_pixmap = load_pixmap("todo1.png")
        if not icon_pixmap.isNull():
            icon_pixmap = icon_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
        else:
            icon_label.setText("📝")
            icon_label.setStyleSheet("font-size: 24px; color: white;")
        icon_label.setStyleSheet("background-color: transparent;")
        icon_label.setFixedSize(32, 32)
        
        title_label = QLabel(self.settings.get('title', 'Simply TodoTask'))
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 5px 0px;
                background-color: transparent;
            }
        """)
        title_label.setWordWrap(True)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        buttons_layout = QHBoxLayout()
        personalize_btn = ModernButton("Customize", "#2196F3", height=40)
        reset_btn = ModernButton("Reset", "#757575", height=40)
        
        personalize_btn.clicked.connect(self.customize_tasks)
        reset_btn.clicked.connect(self.show_reset_dialog)
        
        buttons_layout.addWidget(personalize_btn)
        buttons_layout.addWidget(reset_btn)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label, 1)
        header_layout.addLayout(buttons_layout)
        
        self.main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_layout.setSpacing(0)
        scroll_layout.setContentsMargins(2, 2, 2, 2)

        font_sizes = {
            "small": 12,
            "medium": 14,
            "large": 16
        }
        font_size = font_sizes.get(self.settings.get('font_size', 'medium'), 14)

        for i, task in enumerate(self.tasks):
            task_card = TaskCard(task, i, font_size, self.settings.get('strikethrough', True))
            scroll_layout.addWidget(task_card)

        scroll.setWidget(scroll_widget)
        self.main_layout.addWidget(scroll, 1)

    def load_configuration(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load list", "", "Text files (*.txt);;All files (*.*)"
        )
        if file_path:
            try:
                tasks = []
                settings = {
                    "title": "Simply TodoTask",
                    "font_size": "medium",
                    "strikethrough": True
                }
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    current_task = None
                    i = 0
                    while i < len(lines):
                        line = lines[i].strip()
                        if line.startswith("[SETTINGS]"):
                            i += 1
                            while i < len(lines) and not lines[i].startswith("[TASK]") and lines[i].strip() != "":
                                line = lines[i].strip()
                                if line.startswith("title="):
                                    settings["title"] = line.split('=', 1)[1]
                                elif line.startswith("font_size="):
                                    font_size = line.split('=', 1)[1]
                                    if font_size in ['piccolo', 'medio', 'grande']:
                                        font_size = 'small' if font_size == 'piccolo' else 'medium' if font_size == 'medio' else 'large'
                                    settings["font_size"] = font_size
                                elif line.startswith("strikethrough="):
                                    settings["strikethrough"] = line.split('=', 1)[1].lower() == "true"
                                i += 1
                            continue
                        elif line.startswith("[TASK]"):
                            if current_task:
                                tasks.append(current_task)
                            current_task = {
                                "name": "",
                                "sub_tasks": [],
                                "base_color": "default",
                                "selected_color": "default",
                                "link": ""
                            }
                        elif line.startswith("name=") and current_task is not None:
                            current_task["name"] = line[5:]
                        elif line.startswith("base_color=") and current_task is not None:
                            current_task["base_color"] = line[11:]
                        elif line.startswith("selected_color=") and current_task is not None:
                            current_task["selected_color"] = line[15:]
                        elif line.startswith("link=") and current_task is not None:
                            current_task["link"] = line[5:]
                        elif line.startswith("sub_task=") and current_task is not None:
                            current_task["sub_tasks"].append(line[9:])
                        i += 1
                    
                    if current_task:
                        tasks.append(current_task)
                
                self.tasks = tasks
                self.settings = settings
                self.current_file_path = file_path
                self.refresh_tasks()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot load the list: {e}")

    def save_configuration(self):
        if not self.current_file_path:
            self.save_as_configuration()
            return
            
        dialog = SaveDialog(self)
        result = dialog.exec()
        
        if result == 1:
            self._save_to_file(self.current_file_path)
        elif result == 2:
            self.save_as_configuration()

    def save_as_configuration(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save list", "", "Text files (*.txt);;All files (*.*)"
        )
        if file_path:
            self._save_to_file(file_path)

    def _save_to_file(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("[SETTINGS]\n")
                f.write(f"title={self.settings['title']}\n")
                f.write(f"font_size={self.settings['font_size']}\n")
                f.write(f"strikethrough={self.settings['strikethrough']}\n")
                f.write("\n")
                
                for task in self.tasks:
                    f.write("[TASK]\n")
                    f.write(f"name={task['name']}\n")
                    f.write(f"base_color={task.get('base_color', 'default')}\n")
                    f.write(f"selected_color={task.get('selected_color', 'default')}\n")
                    f.write(f"link={task.get('link', '')}\n")
                    for sub_task in task['sub_tasks']:
                        f.write(f"sub_task={sub_task}\n")
                    f.write("\n")
            
            self.current_file_path = file_path
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot save the list: {e}")

    def customize_tasks(self):
        dialog = CustomizeDialog(self, self.tasks, self.current_file_path, self.settings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_tasks()

    def show_reset_dialog(self):
        dialog = ResetDialog(self)
        result = dialog.exec()
        
        if result == 1:
            self.reset_checks()
        elif result == 2:
            self.reset_tasks()

    def reset_checks(self):
        self.refresh_tasks()

    def reset_tasks(self):
        self.tasks = []
        self.refresh_tasks()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    
    window = TodoApp()
    window.show()
    
    sys.exit(app.exec())
