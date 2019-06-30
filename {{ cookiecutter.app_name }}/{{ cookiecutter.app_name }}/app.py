{% set app_class_name = cookiecutter.formal_name.title().replace(' ','').replace('-','').replace('!','').replace('.','').replace(',','') -%}
{% if cookiecutter.gui_framework == 'Toga' %}import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class {{ app_class_name }}(toga.App):
    def startup(self):
        # Create a main window with a name matching the app
        self.main_window = toga.MainWindow(title=self.name)

        # Create a main content box
        main_box = toga.Box()

        # Add the content on the main window
        self.main_window.content = main_box

        # Show the main window
        self.main_window.show()


def main():
    return {{ app_class_name }}('{{ cookiecutter.formal_name }}', '{{ cookiecutter.bundle }}.{{ cookiecutter.app_name }}')
{% elif cookiecutter.gui_framework == 'PySide2' %}import sys
from PySide2 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Hello World')
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
{% else -%}
def main():
    # This should start and launch your app!
    pass
{% endif -%}
