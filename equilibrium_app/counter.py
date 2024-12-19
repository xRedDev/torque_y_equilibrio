import flet as ft

# gotten from https://ashki23.github.io/markdown-latex.html#latex-equations
md1 = """
# Markdown Errors

superscript^2^

Inline equation: $equation$
Display equation: $$equation$$
$$\mathbb{N} = \{ a \in \mathbb{Z} : a > 0 \}$$
$$\color{blue}{X \sim Normal \; (\mu,\sigma^2)}$$
$$f(X,n) = X_n + X_{n-1}$$
"""


def main(page: ft.Page):
    page.scroll = "auto"
    page.add(
        ft.Markdown(
            md1,
            selectable=True,
            extension_set="gitHubWeb",
            on_tap_link=lambda e: page.launch_url(e.data),
        )
    )


ft.app(target=main)