from typing import Any

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Menu(QWidget):
    itemActivated = Signal(Any)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(256)
        q_v_box_layout = QVBoxLayout(self)
        q_v_box_layout.setContentsMargins(0, 0, 0, 0)
        q_v_box_layout.setSpacing(0)

        q_line_edit = QLineEdit()
        # q_line_edit.setStyleSheet("QLineEdit{border:0}")
        q_line_edit.textChanged.connect(lambda q_string: self.text_changed(q_string))
        q_line_edit.setTextMargins(4, 0, 4, 0)
        q_line_edit.setFixedHeight(44)
        q_v_box_layout.addWidget(q_line_edit)

        self.q_list_widget = QListWidget()
        self.q_list_widget.setStyleSheet("QListWidget{border:0}")
        self.q_list_widget.itemActivated.connect(
            lambda q_list_widget_item: self.itemActivated.emit(
                q_list_widget_item.data(Qt.ItemDataRole.UserRole)
            )
        )
        self.q_list_widget.itemClicked.connect(
            lambda q_list_widget_item: self.itemActivated.emit(
                q_list_widget_item.data(Qt.ItemDataRole.UserRole)
            )
        )
        q_v_box_layout.addWidget(self.q_list_widget)

    def text_changed(self, q_string: str) -> None:
        for index in range(self.q_list_widget.count()):
            q_list_widget_item = self.q_list_widget.item(index)

            q_list_widget_item.setHidden(
                str(q_list_widget_item.data(Qt.ItemDataRole.AccessibleTextRole))
                .lower()
                .count(q_string.lower())
                < 1
            )

    def add(self, accessible_text_role: str, user_role: Any) -> None:
        q_list_widget_item = QListWidgetItem(self.q_list_widget)
        q_list_widget_item.setData(
            Qt.ItemDataRole.AccessibleTextRole, accessible_text_role
        )
        q_list_widget_item.setData(Qt.ItemDataRole.UserRole, user_role)
        q_label = QLabel(accessible_text_role)
        q_label.setContentsMargins(4, 0, 4, 0)
        self.q_list_widget.setItemWidget(q_list_widget_item, q_label)
        q_list_widget_item.setSizeHint(QSize(0, 44))
