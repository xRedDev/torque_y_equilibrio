import flet as ft
import fluentflet.utils
import pandas as pd  # Para exportar los datos (requiere instalar "pandas")
import io  # Manejo de buffers
from flet import FilePicker
import xlsxwriter

def determinar_equilibrio_extendido(masas, distancias, lados):
    """
    Determina el lado y calcula el valor faltante en un sistema de equilibrio estático.
    """
    momentos_izq = sum(m * d for m, d, lado in zip(masas, distancias, lados) if m is not None and d is not None and lado == "izq")
    momentos_der = sum(m * d for m, d, lado in zip(masas, distancias, lados) if m is not None and d is not None and lado == "der")

    indices_desconocidos = [(i, "masa") for i, m in enumerate(masas) if m is None] + \
                           [(i, "distancia") for i, d in enumerate(distancias) if d is None]

    if len(indices_desconocidos) != 1:
        return "Debe haber exactamente un valor desconocido."

    index, tipo = indices_desconocidos[0]

    if tipo == "masa":
        if distancias[index] is None:
            raise ValueError("La distancia asociada a la masa desconocida no puede ser None.")
        lado = lados[index]
        if lado == "izq":
            masas[index] = (momentos_der - momentos_izq) / distancias[index]
        elif lado == "der":
            masas[index] = (momentos_izq - momentos_der) / distancias[index]
        return f"Masa calculada: {masas[index]:.5f} kg en el lado {lado}."
    elif tipo == "distancia":
        if masas[index] is None:
            raise ValueError("La masa asociada a la distancia desconocida no puede ser None.")
        lado = lados[index]
        if lado == "izq":
            distancias[index] = (momentos_der - momentos_izq) / masas[index]
        elif lado == "der":
            distancias[index] = (momentos_izq - momentos_der) / masas[index]
        return f"Distancia calculada: {distancias[index]:.5f} m en el lado {lado}."


def main(page: ft.Page):
    page.title = "Equitorque LAB"
    page.padding = 20
    page.scroll = "adaptive"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.blur_effect = True

    # Variables globales
    masas, distancias, lados = [], [], []
    modo_actual = "normal"
    exportar_btn = None

    # ---------------------- MENÚ PRINCIPAL ----------------------
    def menu_principal():
        page.controls.clear()
        page.appbar = None

        page.fonts = {
            "NunitoBase": "assets/fonts/NunitoBase.ttf",
            "NunitoBold": "assets/fonts/NunitoBold.ttf",
            "NunitoItalic": "assets/fonts/NunitoItalic.ttf",
        }

        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "EQUITORQUE LAB",
                            size=40,
                            weight="bold",
                            color=ft.colors.GREEN_900,
                            font_family="NunitoBold",
                        ),
                        padding=ft.padding.only(bottom=10),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Seleccione un Modo", size=28, weight="bold", color=ft.colors.BLUE_GREY_800),
                                ft.ElevatedButton(
                                    "Modo Normal",
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.BLUE_700,
                                        color=ft.colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                    on_click=lambda e: iniciar_app("normal"),
                                ),
                                ft.ElevatedButton(
                                    "Modo Custom",
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.GREEN_700,
                                        color=ft.colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                    on_click=lambda e: iniciar_app_custom("custom"),
                                ),
                                # ft.ElevatedButton(
                                #     "Teoría",
                                #     style=ft.ButtonStyle(
                                #         bgcolor=ft.colors.PURPLE_700,
                                #         color=ft.colors.WHITE,
                                #         shape=ft.RoundedRectangleBorder(radius=10),
                                #     ),
                                #     on_click=lambda e: iniciar_app_teoria("theory"),
                                # ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        alignment=ft.alignment.center,
                        width=500,
                        padding=30,
                        border_radius=15,
                        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.BLACK12),
                        bgcolor=ft.colors.WHITE,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Aprender Sobre...",
                                    size=28,
                                    weight="bold",
                                    color=ft.colors.BLUE_GREY_800,
                                    font_family="NunitoBold",
                                ),
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Teoría",
                                            icon=ft.Icon(ft.icons.INFO),
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.colors.BLACK12,
                                                color=ft.colors.WHITE,
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                            ),
                                            on_click=lambda e: iniciar_app_teoria("theory"),
                                        ),
                                        ft.ElevatedButton(
                                            "Este proyecto",
                                            icon=ft.Icon(ft.icons.INFO),
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.colors.PURPLE_700,
                                                color=ft.colors.WHITE,
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                            ),
                                            on_click=lambda e: iniciar_app_project("project"),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        alignment=ft.alignment.center,
                        width=500,
                        padding=30,
                        border_radius=15,
                        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.BLACK12),
                        bgcolor=ft.colors.WHITE,
                    ),
                    
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ), 
        )
        page.update()

    # ---------------------- MODO NORMAL ----------------------
    def iniciar_app(modo):
        nonlocal modo_actual, exportar_btn
        modo_actual = modo
        page.controls.clear()

        page.appbar = ft.AppBar(
            title=ft.Text("Cálculo de Equilibrio Estático", color=ft.colors.WHITE),
            bgcolor=ft.colors.BLUE_GREY_900,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: menu_principal()),
        )

        num_masas_input = ft.TextField(label="Número de masas", keyboard_type="number", width=300)
        entradas_container = ft.Column(
            spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        )
        resultado_label = ft.Text(value="El resultado aparecerá aquí.", size=18, weight="bold", color=ft.colors.TEAL_700)

        def generar_entradas(e):
            try:
                num_masas = int(num_masas_input.value)
                masas.clear()
                distancias.clear()
                lados.clear()
                entradas_container.controls.clear()

                for i in range(num_masas):
                    masa_field = ft.TextField(label=f"Masa {i+1} (kg, vaciar si es desconocida)", width=180)
                    distancia_field = ft.TextField(label=f"Distancia {i+1} (m, vaciar si es desconocida )", width=180)
                    lado_dropdown = ft.Dropdown(
                        options=[ft.dropdown.Option("izq"), ft.dropdown.Option("der")],
                        label=f"Lado Masa {i+1}",
                        width=100,
                    )
                    masas.append(masa_field)
                    distancias.append(distancia_field)
                    lados.append(lado_dropdown)
                    entradas_container.controls.append(
                        ft.Row([masa_field, distancia_field, lado_dropdown], alignment=ft.MainAxisAlignment.CENTER)
                    )
                entradas_container.update()
            except ValueError:
                resultado_label.value = "Por favor, ingrese un número válido."
                resultado_label.update()

        def calcular_equilibrio(e):
            try:
                masas_valores = [float(m.value) if m.value.strip() else None for m in masas]
                distancias_valores = [float(d.value) if d.value.strip() else None for d in distancias]
                lados_valores = [l.value for l in lados]

                resultado = determinar_equilibrio_extendido(masas_valores, distancias_valores, lados_valores)
                resultado_label.value = resultado
                exportar_btn.visible = True
                page.update()
            except Exception as ex:
                resultado_label.value = f"Error: {ex}"
                resultado_label.update()

        def exportar_tabla(e):
            data = {
                "Masa (kg)": [m.value for m in masas],
                "Distancia (m)": [d.value for d in distancias],
                "Lado": [l.value for l in lados],
            }
            df = pd.DataFrame(data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Equilibrio")
            output.seek(0)
            file_picker.save_file("equilibrio.xlsx", output.read())

        file_picker = FilePicker()
        page.overlay.append(file_picker)

        exportar_btn = ft.ElevatedButton("Exportar Tabla", visible=False, on_click=exportar_tabla)

        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        num_masas_input,
                        ft.ElevatedButton("Generar Entradas", on_click=generar_entradas),
                        entradas_container,
                        ft.ElevatedButton("Calcular Equilibrio", on_click=calcular_equilibrio),
                        resultado_label,
                        exportar_btn,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    expand=True,
                ),
                alignment=ft.alignment.center,
                border_radius=10,
                padding=20,
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.BLACK12),
                bgcolor=ft.colors.WHITE,
            )
        )
        page.update()

    # ---------------------- MODO CUSTOM ----------------------
    def iniciar_app_custom(modo):
        nonlocal modo_actual
        modo_actual = modo
        page.controls.clear()

        page.appbar = ft.AppBar(
            title=ft.Text("Modo Personalizad", color=ft.colors.WHITE),
            bgcolor=ft.colors.BLUE_GREY_900,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: menu_principal()),
        );


    # ---------------------- MODO TEORÍA ----------------------
    def iniciar_app_teoria(modo):
        nonlocal modo_actual
        modo_actual = modo
        page.controls.clear()

        page.appbar = ft.AppBar(
            title=ft.Text("Aprendiendo la Teoría", color=ft.colors.WHITE),
            bgcolor=ft.colors.BLUE_GREY_900,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: menu_principal()),
        );
    
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="Esta es la sección de teoría.", size=24, font_family="NunitoBold", weight="bold", color=ft.colors.TEAL_700),
                        ft.Text(value="Aquí encontrarás información sobre la teoría del equilibrio estático y sus aplicaciones.", size=16, font_family="NunitoBase"),
                        ft.Text(r"$E = mc^2$", size=30),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    expand=True,
                ),
                alignment=ft.alignment.center,
                padding=20,
                #shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.PURPLE_700),
                #bgcolor=ft.colors.WHITE,
            )
        );
    
    def iniciar_app_project(modo):
        nonlocal modo_actual
        modo_actual = modo
        page.controls.clear()

        page.appbar = ft.AppBar(
            title=ft.Text("Aprendiendo la Teoría", color=ft.colors.WHITE),
            bgcolor=ft.colors.BLUE_GREY_900,
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: menu_principal()),
        );
    
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="Esta es la sección de teoría.", size=24, font_family="NunitoBold", weight="bold", color=ft.colors.TEAL_700),
                        ft.Text(value="Aquí encontrarás información sobre la teoría del equilibrio estático y sus aplicaciones.", size=16, font_family="NunitoBase"),
                        ft.Text(r"$E = mc^2$", size=30),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    expand=True,
                ),
                alignment=ft.alignment.center,
                padding=20,
                #shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.PURPLE_700),
                #bgcolor=ft.colors.WHITE,
            )
        );

    # La primera pestaña será el menú principal
    menu_principal()


ft.app(target=main) # generar app