from {{ cookiecutter.module_name }}.app import main

if __name__ == '__main__':
{%- if cookiecutter.gui_framework == 'Toga' %}
    main().main_loop()
{%- elif cookiecutter.gui_framework in ('PySide2', 'PySide6') %}
    main()
{%- else %}
    main()
{%- endif %}
