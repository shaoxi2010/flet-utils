import os
from itertools import islice
import flet
from flet import (
    Page,
    UserControl,
    colors,
    TextField,
    Text,
    IconButton,
    icons,
    Icon,
    GridView,
    Row,
    Column,
    Container,
    TextButton,
    alignment,
    SnackBar
)

class ColorsBrowser(UserControl):
    def __init__(self, expand=False, height=500):
        super().__init__()
        if expand:
            self.expand = expand
        else:
            self.height = height

    def build(self):
        def batches(iterable, batch_size):
            iterator = iter(iterable)
            while batch := list(islice(iterator, batch_size)):
                yield batch

        # fetch all icon constants from colors.py module
        colors_list = []
        list_started = False
        for key, value in vars(colors).items():
            if key == "PRIMARY":
                list_started = True
            if list_started:
                colors_list.append(value)

        search_txt = TextField(
            expand=1,
            hint_text="Enter keyword and press search button",
            autofocus=True,
            on_submit=lambda e: display_colors(e.control.value),
        )

        def search_click(e):
            display_colors(search_txt.value)

        search_query = Row(
            [search_txt, IconButton(icon=icons.SEARCH, on_click=search_click)]
        )
        search_results = GridView(
            expand=1,
            runs_count=10,
            max_extent=150,
            spacing=5,
            run_spacing=5,
            child_aspect_ratio=1,
        )
        status_bar = Text()
        def copy_to_clipboard(e):
            color_name = e.control.data
            print("Copy to clipboard:", color_name)
            self.page.set_clipboard(e.control.data)
            self.page.show_snack_bar(
                SnackBar(Text(f"Copied {color_name}"), open=True))

        def search_color(search_term: str):
            for color_name in colors_list:
                if search_term in color_name:
                    yield color_name

        def display_colors(search_term: str):

            # clean search results
            search_query.disabled = True
            self.update()

            search_results.clean()

            for batch in batches(search_color(search_term.lower()), 200):
                for color_name in batch:
                    search_results.controls.append(
                        TextButton(
                            content=Container(
                                content=Column(
                                    [
                                        Icon(name=icons.RECTANGLE, size=55, color=color_name),
                                        Text(
                                            value=f"{color_name}",
                                            size=12,
                                            width=100,
                                            no_wrap=True,
                                            text_align="center",
                                            color=colors.ON_SURFACE_VARIANT,
                                        ),
                                    ],
                                    spacing=5,
                                    alignment="center",
                                    horizontal_alignment="center",
                                ),
                                alignment=alignment.center,
                            ),
                            tooltip=f"{color_name}\nClick to copy to a clipboard",
                            on_click=copy_to_clipboard,
                            data=color_name,
                        )
                    )
                status_bar.value = f"Colors found: {len(search_results.controls)}"
                self.update()

            if len(search_results.controls) == 0:
                self.page.show_snack_bar(
                    SnackBar(Text("No colors found"), open=True))
            search_query.disabled = False
            self.update()

        return Column(
            [
                search_query,
                search_results,
                status_bar,
            ],
            expand=True,
        )


def main(page: Page):
    page.title = "Flet colors browser"
    page.add(ColorsBrowser(expand=True))


flet.app(target=main)
