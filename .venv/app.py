import json
import os
import sys
from datetime import datetime

from PyQt6.QtCore import Qt, QDateTime, QTimer, QTime, QDate
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCalendarWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QComboBox,
    QLabel,
    QDialog,
    QGridLayout,
    QDateEdit,
    QTimeEdit,
    QCheckBox
)


class ReminderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Установить напоминание")

        self.label_date = QLabel("Дата:", self)
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(datetime.today())

        self.label_time = QLabel("Время:", self)
        self.time_edit = QTimeEdit(self)
        self.time_edit.setTime(QTime(9, 0))

        self.checkbox_recurring = QCheckBox("Повторяющееся", self)

        button_box = QHBoxLayout()
        self.button_ok = QPushButton("OK", self)
        self.button_cancel = QPushButton("Cancel", self)
        button_box.addWidget(self.button_ok)
        button_box.addWidget(self.button_cancel)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.label_date, 0, 0)
        grid_layout.addWidget(self.date_edit, 0, 1)
        grid_layout.addWidget(self.label_time, 1, 0)
        grid_layout.addWidget(self.time_edit, 1, 1)
        grid_layout.addWidget(self.checkbox_recurring, 2, 0, 1, 2)
        grid_layout.addLayout(button_box, 3, 0, 1, 2)

        self.setLayout(grid_layout)

        self.button_ok.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Менеджер задач")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Calendar
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet("QCalendarWidget QWidget { color: black; background-color: #f9f9f9; }")
        self.layout.addWidget(self.calendar)

        # Category ComboBox
        self.category_combo = QComboBox(self)
        self.category_combo.addItem("Без категории")
        self.category_combo.addItem("Работа")
        self.category_combo.addItem("Домашние дела")
        self.category_combo.addItem("Личное")
        self.category_combo.setStyleSheet("color: white; background-color: #333;")
        self.layout.addWidget(self.category_combo)

        # Task Tree
        self.task_tree = QTreeWidget(self)
        self.task_tree.setHeaderLabels(["Дата", "Задача"])
        self.task_tree.setStyleSheet("color: white; background-color: #333;")
        self.layout.addWidget(self.task_tree)

        # Buttons
        self.button_layout = QHBoxLayout()

        self.add_task_button = QPushButton("Добавить задачу", self)
        self.add_task_button.setIcon(QIcon("add_icon.png"))
        self.add_task_button.clicked.connect(self.add_task)
        self.add_task_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button_layout.addWidget(self.add_task_button)

        self.add_subtask_button = QPushButton("Добавить подзадачу", self)
        self.add_subtask_button.setIcon(QIcon("add_subtask_icon.png"))
        self.add_subtask_button.clicked.connect(self.add_subtask)
        self.add_subtask_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_layout.addWidget(self.add_subtask_button)

        self.set_reminder_button = QPushButton("Установить напоминание", self)
        self.set_reminder_button.setIcon(QIcon("reminder_icon.png"))
        self.set_reminder_button.clicked.connect(self.set_reminder)
        self.set_reminder_button.setStyleSheet("background-color: #FF9800; color: white;")
        self.button_layout.addWidget(self.set_reminder_button)

        self.save_tasks_button = QPushButton("Сохранить задачи", self)
        self.save_tasks_button.setIcon(QIcon("save_icon.png"))
        self.save_tasks_button.clicked.connect(self.save_tasks)
        self.save_tasks_button.setStyleSheet("background-color: #E91E63; color: white;")
        self.button_layout.addWidget(self.save_tasks_button)

        self.load_tasks_button = QPushButton("Загрузить задачи", self)
        self.load_tasks_button.setIcon(QIcon("load_icon.png"))
        self.load_tasks_button.clicked.connect(self.load_tasks)
        self.load_tasks_button.setStyleSheet("background-color: #9C27B0; color: white;")
        self.button_layout.addWidget(self.load_tasks_button)

        self.filter_button = QPushButton("Фильтровать", self)
        self.filter_button.setIcon(QIcon("filter_icon.png"))
        self.filter_button.clicked.connect(self.filter_tasks)
        self.filter_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button_layout.addWidget(self.filter_button)

        self.edit_task_button = QPushButton("Изменить задачу", self)
        self.edit_task_button.setIcon(QIcon("edit_icon.png"))
        self.edit_task_button.clicked.connect(self.edit_task)
        self.edit_task_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_layout.addWidget(self.edit_task_button)

        self.remove_task_button = QPushButton("Удалить задачу", self)
        self.remove_task_button.setIcon(QIcon("delete_icon.png"))
        self.remove_task_button.clicked.connect(self.remove_task)
        self.remove_task_button.setStyleSheet("background-color: #F44336; color: white;")
        self.button_layout.addWidget(self.remove_task_button)

        self.button_layout.addWidget(QLabel('', self))
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.layout.addLayout(self.button_layout)

        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9f9f9;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #e0e0e0;
                selection-background-color: #c0c0c0;
            }
            QTreeWidget::item:selected {
                background-color: #b0b0b0;
            }
            QPushButton {
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            }
            .central-widget {
                background-image: url('original.png');
                background-repeat: no-repeat;
                background-position: center center;
                background-size: cover;
            }
        """)

        # Reminders
        self.reminders = {}

        # Load tasks from file if exists
        self.load_tasks()

    def add_task(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        task_name, ok = QInputDialog.getText(self, 'Добавить задачу', 'Введите название задачи:')
        if ok and task_name:
            category = self.category_combo.currentText()
            parent_item = QTreeWidgetItem(self.task_tree)
            parent_item.setText(0, date)
            parent_item.setText(1, task_name)
            parent_item.setForeground(1, QColor("white"))
            parent_item.setFlags(parent_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            parent_item.setCheckState(1, Qt.CheckState.Unchecked)
            parent_item.setData(1, Qt.ItemDataRole.UserRole, {"category": category})

    def add_subtask(self):
        selected_items = self.task_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Выберите родительскую задачу.")
            return

        parent_item = selected_items[0]
        subtask_name, ok = QInputDialog.getText(self, 'Добавить подзадачу', 'Введите название подзадачи:')
        if ok and subtask_name:
            child_item = QTreeWidgetItem(parent_item)
            child_item.setText(1, subtask_name)
            child_item.setForeground(1, QColor("white"))
            child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            child_item.setCheckState(1, Qt.CheckState.Unchecked)
            child_item.setData(1, Qt.ItemDataRole.UserRole, {
                "category": parent_item.data(1, Qt.ItemDataRole.UserRole).get("category", "Без категории")})

    def set_reminder(self):
        selected_items = self.task_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Выберите задачу для установки напоминания.")
            return

        item = selected_items[0]
        date_str = item.text(0)
        task_name = item.text(1)

        dialog = ReminderDialog(self)
        if dialog.exec():
            reminder_date = dialog.date_edit.date()
            reminder_time = dialog.time_edit.time()
            reminder_datetime = QDateTime(reminder_date.year(), reminder_date.month(), reminder_date.day(),
                                          reminder_time.hour(), reminder_time.minute(), reminder_time.second())
            reminder_time = reminder_datetime.toPyDateTime()
            self.reminders[task_name] = reminder_time

            timer = QTimer(self)
            delay_ms = int((reminder_time - datetime.now()).total_seconds() * 1000)
            timer.start(delay_ms)
            timer.timeout.connect(self.show_reminder)

            QMessageBox.information(self, "Напоминание установлено",
                                    f"Напоминание для '{task_name}' установлено на {reminder_time}")

    def show_reminder(self):
        QMessageBox.information(self, "Менеджер задач", f"Напоминание")

    def save_tasks(self):
        self.tasks_data = []
        for i in range(self.task_tree.topLevelItemCount()):
            top_item = self.task_tree.topLevelItem(i)
            task_data = {
                "date": top_item.text(0),
                "task": top_item.text(1),
                "checked": top_item.checkState(1) == Qt.CheckState.Checked,
                "category": top_item.data(1, Qt.ItemDataRole.UserRole).get("category", "Без категории"),
                "subtasks": []
            }
            for j in range(top_item.childCount()):
                child_item = top_item.child(j)
                task_data["subtasks"].append({
                    "task": child_item.text(1),
                    "checked": child_item.checkState(1) == Qt.CheckState.Checked,
                    "category": child_item.data(1, Qt.ItemDataRole.UserRole).get("category", "Без категории")
                })
            self.tasks_data.append(task_data)

        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(self.tasks_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить задачи: {str(e)}")

        QMessageBox.information(self, "Сохранение", "Задачи успешно сохранены.")

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r", encoding="utf-8") as f:
                    self.tasks_data = json.load(f)

                self.task_tree.clear()
                for task_data in self.tasks_data:
                    top_item = QTreeWidgetItem(self.task_tree)
                    top_item.setText(0, task_data["date"])
                    top_item.setText(1, task_data["task"])
                    top_item.setForeground(1, QColor("white"))
                    top_item.setFlags(top_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    top_item.setCheckState(1,
                                           Qt.CheckState.Checked if task_data["checked"] else Qt.CheckState.Unchecked)
                    top_item.setData(1, Qt.ItemDataRole.UserRole, {"category": task_data["category"]})

                    for subtask_data in task_data["subtasks"]:
                        child_item = QTreeWidgetItem(top_item)
                        child_item.setText(1, subtask_data["task"])
                        child_item.setForeground(1, QColor("white"))
                        child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                        child_item.setCheckState(1, Qt.CheckState.Checked if subtask_data[
                            "checked"] else Qt.CheckState.Unchecked)
                        child_item.setData(1, Qt.ItemDataRole.UserRole, {"category": subtask_data["category"]})

                QMessageBox.information(self, "Загрузка", "Задачи успешно загружены.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить задачи: {str(e)}")
        else:
            QMessageBox.warning(self, "Предупреждение", "Файл задач не найден.")

    def filter_tasks(self):
        category = self.category_combo.currentText()
        self.task_tree.clear()

        for task_data in self.tasks_data:
            if category == "Без категории" or task_data.get("category", "") == category:
                top_item = QTreeWidgetItem(self.task_tree)
                top_item.setText(0, task_data["date"])
                top_item.setText(1, task_data["task"])
                top_item.setForeground(1, QColor("white"))
                top_item.setFlags(top_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                top_item.setCheckState(1, Qt.CheckState.Checked if task_data["checked"] else Qt.CheckState.Unchecked)

                for subtask_data in task_data["subtasks"]:
                    child_item = QTreeWidgetItem(top_item)
                    child_item.setText(1, subtask_data["task"])
                    child_item.setForeground(1, QColor("white"))
                    child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    child_item.setCheckState(1, Qt.CheckState.Checked if subtask_data[
                        "checked"] else Qt.CheckState.Unchecked)

    def edit_task(self):
        selected_items = self.task_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Выберите задачу для редактирования.")
            return

        item = selected_items[0]
        new_task_name, ok = QInputDialog.getText(self, 'Изменить задачу', 'Введите новое название задачи:',
                                                 text=item.text(1))
        if ok and new_task_name:
            item.setText(1, new_task_name)

    def remove_task(self):
        selected_items = self.task_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Выберите задачу для удаления.")
            return

        item = selected_items[0]
        if item.parent():
            item.parent().removeChild(item)
        else:
            self.task_tree.takeTopLevelItem(self.task_tree.indexOfTopLevelItem(item))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
