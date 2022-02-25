"""
{{ cookiecutter.description }}
"""
{% if cookiecutter.gui_framework == 'Toga' -%}
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class {{ cookiecutter.class_name }}(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return {{ cookiecutter.class_name }}()
{% elif cookiecutter.gui_framework in ('PySide2', 'PySide6') -%}
import sys
from {{ cookiecutter.gui_framework }} import QtWidgets


class {{ cookiecutter.class_name }}(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('{{ cookiecutter.app_name }}')
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = {{ cookiecutter.class_name }}()
    {%- if cookiecutter.gui_framework == 'PySide2' %}
    sys.exit(app.exec_())
    {%- else %}
    sys.exit(app.exec())
    {%- endif %}
{% elif cookiecutter.gui_framework == 'PursuedPyBear' %}import ppb


class {{ cookiecutter.class_name }}(ppb.Scene):
    def __init__(self, **props):
        super().__init__(**props)

        self.add(ppb.Sprite(
            image=ppb.Image('{{ cookiecutter.module_name }}/resources/{{ cookiecutter.app_name }}.png'),
        ))


def main():
    ppb.run(
        starting_scene={{ cookiecutter.class_name }},
        title='{{ cookiecutter.formal_name }}',
    )
{% else -%}
def main():
    # This should start and launch your app!
    pass
{% endif -%}
