# PySide6 Modern QSS Stylesheets matching Web Theme (Slate & Indigo)

DARK_STYLESHEET = """
QMainWindow, QDialog {
    background-color: #0F172A;
    color: #F8FAFC;
}

QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Vazirmatn", sans-serif;
    color: #F8FAFC;
}

/* Sidebar List Widget */
QListWidget#SidebarList {
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
    outline: none;
}

QListWidget#SidebarList::item {
    height: 48px;
    padding-left: 16px;
    padding-right: 16px;
    color: #94A3B8;
    border-radius: 8px;
    margin: 4px 8px;
    font-size: 13px;
    font-weight: 600;
}

QListWidget#SidebarList::item:hover {
    background-color: #1E293B;
    color: #F8FAFC;
}

QListWidget#SidebarList::item:selected {
    background-color: #4F46E5;
    color: #FFFFFF;
    font-weight: 700;
}

/* Cards & GroupBoxes */
QGroupBox {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    margin-top: 24px;
    padding-top: 16px;
    font-weight: 700;
    font-size: 13px;
    color: #CBD5E1;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 10px;
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #818CF8;
}

QFrame#StatsCard {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
}

QFrame#StatsCard QLabel#Title {
    font-size: 12px;
    color: #94A3B8;
    font-weight: 600;
}

QFrame#StatsCard QLabel#Value {
    font-size: 22px;
    color: #F8FAFC;
    font-weight: 800;
}

QFrame#StatsCard QLabel#Subtitle {
    font-size: 11px;
    color: #64748B;
}

/* DropZone Widget */
QFrame#DropZone {
    background-color: #0F172A;
    border: 2px dashed #4F46E5;
    border-radius: 12px;
    padding: 24px;
}

QFrame#DropZone:hover {
    background-color: #1E1B4B;
    border-color: #818CF8;
}

/* Buttons */
QPushButton {
    background-color: #334155;
    color: #F8FAFC;
    border: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #475569;
    border-color: #64748B;
}

QPushButton:pressed {
    background-color: #1E293B;
}

QPushButton#PrimaryButton {
    background-color: #4F46E5;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 8px;
}

QPushButton#PrimaryButton:hover {
    background-color: #4338CA;
}

QPushButton#PrimaryButton:disabled {
    background-color: #312E81;
    color: #6366F1;
}

QPushButton#DangerButton {
    background-color: #991B1B;
    color: #FEE2E2;
    border: none;
}

QPushButton#DangerButton:hover {
    background-color: #B91C1C;
}

/* Inputs & Selects */
QComboBox, QSpinBox, QLineEdit {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 6px 12px;
    color: #F8FAFC;
    font-size: 13px;
}

QComboBox:hover, QSpinBox:hover, QLineEdit:hover {
    border-color: #6366F1;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #1E293B;
    border: 1px solid #334155;
    color: #F8FAFC;
    selection-background-color: #4F46E5;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    font-size: 13px;
    color: #E2E8F0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #475569;
    background-color: #0F172A;
}

QCheckBox::indicator:checked {
    background-color: #4F46E5;
    border-color: #4F46E5;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
}

/* Tables */
QTableWidget {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 8px;
    gridline-color: #1E293B;
    color: #E2E8F0;
}

QHeaderView::section {
    background-color: #1E293B;
    color: #94A3B8;
    padding: 8px 12px;
    border: none;
    border-bottom: 1px solid #334155;
    font-weight: 700;
    font-size: 12px;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #312E81;
    color: #FFFFFF;
}

/* Progress Bar */
QProgressBar {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    height: 16px;
    text-align: center;
    color: #F8FAFC;
    font-size: 11px;
    font-weight: 700;
}

QProgressBar::chunk {
    background-color: #4F46E5;
    border-radius: 7px;
}

/* Status Bar */
QStatusBar {
    background-color: #0F172A;
    border-top: 1px solid #1E293B;
    color: #64748B;
    font-size: 12px;
}
"""

LIGHT_STYLESHEET = """
QMainWindow, QDialog {
    background-color: #F8FAFC;
    color: #0F172A;
}

QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Vazirmatn", sans-serif;
    color: #0F172A;
}

/* Sidebar List Widget */
QListWidget#SidebarList {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
    outline: none;
}

QListWidget#SidebarList::item {
    height: 48px;
    padding-left: 16px;
    padding-right: 16px;
    color: #64748B;
    border-radius: 8px;
    margin: 4px 8px;
    font-size: 13px;
    font-weight: 600;
}

QListWidget#SidebarList::item:hover {
    background-color: #F1F5F9;
    color: #0F172A;
}

QListWidget#SidebarList::item:selected {
    background-color: #4F46E5;
    color: #FFFFFF;
    font-weight: 700;
}

/* Cards & GroupBoxes */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    margin-top: 24px;
    padding-top: 16px;
    font-weight: 700;
    font-size: 13px;
    color: #334155;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 10px;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    color: #4F46E5;
}

QFrame#StatsCard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px;
}

QFrame#StatsCard QLabel#Title {
    font-size: 12px;
    color: #64748B;
    font-weight: 600;
}

QFrame#StatsCard QLabel#Value {
    font-size: 22px;
    color: #0F172A;
    font-weight: 800;
}

QFrame#StatsCard QLabel#Subtitle {
    font-size: 11px;
    color: #94A3B8;
}

/* DropZone Widget */
QFrame#DropZone {
    background-color: #FFFFFF;
    border: 2px dashed #818CF8;
    border-radius: 12px;
    padding: 24px;
}

QFrame#DropZone:hover {
    background-color: #EEF2FF;
    border-color: #4F46E5;
}

/* Buttons */
QPushButton {
    background-color: #F1F5F9;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #E2E8F0;
    border-color: #94A3B8;
}

QPushButton:pressed {
    background-color: #CBD5E1;
}

QPushButton#PrimaryButton {
    background-color: #4F46E5;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 8px;
}

QPushButton#PrimaryButton:hover {
    background-color: #4338CA;
}

QPushButton#PrimaryButton:disabled {
    background-color: #C7D2FE;
    color: #6366F1;
}

QPushButton#DangerButton {
    background-color: #FEE2E2;
    color: #991B1B;
    border: 1px solid #FCA5A5;
}

QPushButton#DangerButton:hover {
    background-color: #FCA5A5;
}

/* Inputs & Selects */
QComboBox, QSpinBox, QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 6px 12px;
    color: #0F172A;
    font-size: 13px;
}

QComboBox:hover, QSpinBox:hover, QLineEdit:hover {
    border-color: #4F46E5;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    color: #0F172A;
    selection-background-color: #4F46E5;
    selection-color: #FFFFFF;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    font-size: 13px;
    color: #1E293B;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #94A3B8;
    background-color: #FFFFFF;
}

QCheckBox::indicator:checked {
    background-color: #4F46E5;
    border-color: #4F46E5;
}

/* Tables */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    gridline-color: #F1F5F9;
    color: #0F172A;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #64748B;
    padding: 8px 12px;
    border: none;
    border-bottom: 1px solid #E2E8F0;
    font-weight: 700;
    font-size: 12px;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #EEF2FF;
    color: #4F46E5;
}

/* Progress Bar */
QProgressBar {
    background-color: #E2E8F0;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    height: 16px;
    text-align: center;
    color: #0F172A;
    font-size: 11px;
    font-weight: 700;
}

QProgressBar::chunk {
    background-color: #4F46E5;
    border-radius: 7px;
}

/* Status Bar */
QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E2E8F0;
    color: #64748B;
    font-size: 12px;
}
"""
