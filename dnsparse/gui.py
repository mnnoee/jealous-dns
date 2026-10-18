"""Графический интерфейс (Qt5/Qt6)."""

QT = None
try:
    from PyQt6.QtCore import Qt as _Qt
    from PyQt6.QtCore import QTimer
    from PyQt6.QtGui import QFont, QTextCursor
    from PyQt6.QtWidgets import (
        QApplication,
        QCheckBox,
        QHBoxLayout,
        QLabel,
        QMainWindow,
        QPushButton,
        QSplitter,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
    QT = "PyQt6"
    _VERTICAL = _Qt.Orientation.Vertical
except Exception:
    from PyQt5.QtCore import Qt as _Qt
    from PyQt5.QtCore import QTimer
    from PyQt5.QtGui import QFont, QTextCursor
    from PyQt5.QtWidgets import (
        QApplication,
        QCheckBox,
        QHBoxLayout,
        QLabel,
        QMainWindow,
        QPushButton,
        QSplitter,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
    QT = "PyQt5"
    _VERTICAL = _Qt.Vertical


def run_gui():
    import os
    import signal
    import sys

    from .core import DNSParser
    from .formatter import DNSFormatter

    os.environ.pop("QT_QPA_PLATFORM", None)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    class Window(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("jealous-dns")
            self.setGeometry(100, 100, 1300, 800)
            central = QWidget()
            self.setCentralWidget(central)
            layout = QVBoxLayout(central)
            splitter = QSplitter(_VERTICAL)

            input_area = QWidget()
            input_layout = QVBoxLayout(input_area)
            self.input_text = QTextEdit()
            self.input_text.setPlaceholderText("Сюда вставляй DNS-выгрузку")
            self.input_text.setFont(QFont("Monospace", 10))
            input_layout.addWidget(self.input_text)

            self.format_btn = QPushButton("Форматировать")
            self.clear_btn = QPushButton("Очистить")
            self.pretty_checkbox = QCheckBox("Выравнивать")
            self.pretty_checkbox.setChecked(True)

            self.format_btn.clicked.connect(self.format_dns)
            self.clear_btn.clicked.connect(self.clear_input)

            button_row = QHBoxLayout()
            button_row.addWidget(self.format_btn)
            button_row.addWidget(self.clear_btn)
            button_row.addStretch()
            button_row.addWidget(self.pretty_checkbox)
            input_layout.addLayout(button_row)

            output_area = QWidget()
            output_layout = QVBoxLayout(output_area)
            output_layout.addWidget(QLabel("Результат:"))
            self.output_text = QTextEdit()
            self.output_text.setReadOnly(True)
            self.output_text.setFont(QFont("Monospace", 10))
            output_layout.addWidget(self.output_text)

            splitter.addWidget(input_area)
            splitter.addWidget(output_area)
            splitter.setSizes([400, 400])
            layout.addWidget(splitter)

        def format_dns(self):
            raw_text = self.input_text.toPlainText()
            if not raw_text.strip():
                return
            try:
                records = DNSParser.parse(raw_text)
                if not records:
                    self.output_text.setText("Не распознано. Проверь формат.")
                    return
                is_pretty = self.pretty_checkbox.isChecked()
                formatted = DNSFormatter(is_pretty=is_pretty).format(records)
                self.output_text.setText(formatted)
                _start = getattr(QTextCursor, "Start", None)
                if _start is None:
                    _start = QTextCursor.MoveOperation.Start
                self.output_text.moveCursor(_start)
            except Exception as e:
                self.output_text.setText(f"Ошибка: {str(e)}")

        def clear_input(self):
            self.input_text.clear()
            self.output_text.clear()

        def closeEvent(self, event):
            event.accept()
            sys.exit(0)

    signal.signal(signal.SIGINT, lambda s, f: app.quit())
    window = Window()
    window.show()
    sys.exit(app.exec() if hasattr(app, "exec") else app.exec_())
