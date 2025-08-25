import os

import flet as ft

import constants as const


def main(page: ft.Page):
    page.title = const.PAGE_TITLE
    page.theme_mode = const.THEME_DARK
    page.window.resizable = False
    page.window.maximizable = False

    if not os.path.exists(const.PATH_TO_TODO_LISTS_FOLDER):
        os.makedirs(const.PATH_TO_TODO_LISTS_FOLDER)

    horizontal_divider = ft.Divider(height=5, thickness=3, color=const.ON_PRIMARY)
    vertical_divider = ft.VerticalDivider(width=5, thickness=3, color=const.ON_PRIMARY)

    todo_lists_column = ft.Column(height=const.PAGE_HEIGHT, scroll=ft.ScrollMode.AUTO, width=250)

    def add_new_todo_list(e):
        list_name = todo_lists_new_name_field.value
        if list_name != "" and list_name != " ":
            list_name = f"{list_name}.txt"
            with open(os.path.join(const.PATH_TO_TODO_LISTS_FOLDER, list_name), "w") as f:
                f.write("")
            todo_lists_new_name_field.value = ""
            todo_lists_new_name_field.update()
            generate_todo_lists_ui()

    def remove_todo_list(e, name):
        os.remove(os.path.join(const.PATH_TO_TODO_LISTS_FOLDER, f"{name}.txt"))
        generate_todo_lists_ui()

    def generate_todo_lists_ui():
        todo_lists_names = [f for f in os.scandir(const.PATH_TO_TODO_LISTS_FOLDER) if f.is_file()]
        todo_lists_column_controls = [ft.Container(ft.Text(value=const.TODO_LISTS_LABEL, size=20), padding=5),
                                      horizontal_divider]
        for l in todo_lists_names:
            filename = os.path.basename(l).split(".")
            filename.pop(-1)
            tmp = ""
            for part in filename:
                tmp = tmp.join(part)
            filename = tmp
            todo_lists_column_controls.append(ft.Container(ft.Row([ft.Container(ft.Text(value=filename, size=20),
                                                                                on_click=lambda
                                                                                    e: generate_todo_list_content(e,
                                                                                                                  filename)),
                                                                   ft.IconButton(const.ICON_REMOVE,
                                                                                 on_click=lambda e: remove_todo_list(e,
                                                                                                                     filename))]),
                                                           padding=5))
            todo_lists_column_controls.append(horizontal_divider)

        todo_lists_column_controls.append(todo_lists_add_new_row)

        todo_lists_column.controls = todo_lists_column_controls
        try:
            todo_lists_column.update()
        except Exception:
            pass
        page.update()

    def new_todo_list_line(e, todo_list_name):
        with open(os.path.join(const.PATH_TO_TODO_LISTS_FOLDER, f"{todo_list_name}.txt"), "a") as f:
            f.write("task\n")
        generate_todo_list_content(e, todo_list_name)

    def save_todo_list(e, todo_list_name):
        content = list()
        for row in todo_list_content.content.controls:
            if type(row.controls[-1]) is ft.TextField:
                check_box_value = row.controls[0].value
                if check_box_value:
                    content.append(f"{row.controls[-1].value}:True\n")
                else:
                    content.append(f"{row.controls[-1].value}:Flse\n")

        with open(os.path.join(const.PATH_TO_TODO_LISTS_FOLDER, f"{todo_list_name}.txt"), "w") as f:
            f.writelines(content)

    def generate_todo_list_content(e, todo_list_name):
        todo_list_controls = list()
        todo_list_controls.append(ft.Row([ft.Text(todo_list_name, size=30),
            ft.IconButton(const.ICON_ADD, on_click=lambda e: new_todo_list_line(e, todo_list_name))],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True))
        with open(os.path.join(const.PATH_TO_TODO_LISTS_FOLDER, f"{todo_list_name}.txt"), "r") as f:
            lines = f.readlines()
            for line in lines:
                check_box_value = True if line.split(":")[-1] == "True" else False
                todo_list_controls.append(ft.Row(
                    [ft.Checkbox(value=check_box_value, on_change=lambda e: save_todo_list(e, todo_list_name)),
                        ft.TextField(value=line[:len(line) - 6],
                                     on_submit=lambda e: save_todo_list(e, todo_list_name))]))
        todo_list_content.content = ft.Column(todo_list_controls, scroll=ft.ScrollMode.AUTO,
                                              alignment=ft.MainAxisAlignment.START,
                                              horizontal_alignment=ft.CrossAxisAlignment.START)

    todo_lists_add_new_button = ft.IconButton(const.ICON_ADD, on_click=add_new_todo_list)
    todo_lists_new_name_field = ft.TextField(label=const.TODO_LISTS_FIELD_LABEL, width=200, max_length=18)
    todo_lists_add_new_row = ft.Row([todo_lists_new_name_field, todo_lists_add_new_button])
    todo_list_content = ft.Container()
    todo_lists_container = ft.Container(todo_lists_column, padding=10,
                                        border=ft.border.all(width=3, color=const.ON_PRIMARY))

    main_row = ft.Row([todo_lists_container, vertical_divider, todo_list_content])
    generate_todo_lists_ui()
    page.add(main_row)
    page.update()


ft.run(main)
