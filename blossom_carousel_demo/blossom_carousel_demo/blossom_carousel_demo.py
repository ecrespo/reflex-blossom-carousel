"""Welcome to Reflex! This file showcases the custom component in a basic app."""

import reflex as rx

from reflex_blossom_carousel import blossom_carousel


class State(rx.State):
    """The app state."""

    pass


def index() -> rx.Component:
    carousel = blossom_carousel(
        *[rx.el.li(str(i + 1), class_name="slide") for i in range(12)],
        id="demo-carousel",
        as_="ul",
        class_name="carousel",
        repeat=False,
        load="conditional",
    )
    return rx.center(
        rx.theme_panel(),
        rx.vstack(
            rx.heading("Blossom Carousel", size="9"),
            rx.text(
                "Native-scroll-first carousel with physics-based drag on pointer devices.",
                size="4",
                color_scheme="gray",
            ),
            carousel,
            rx.hstack(
                rx.button("Previous", on_click=carousel.prev(align="center")),
                rx.button("Next", on_click=carousel.next(align="center")),
                spacing="3",
            ),
            align="center",
            spacing="6",
            width="100%",
        ),
        height="100vh",
    )


# Add state and page to the app.
app = rx.App(stylesheets=["/carousel.css"])
app.add_page(index)