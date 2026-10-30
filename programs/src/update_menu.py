from src.data_service import get_layer

def update_menu(canvas):
    canvas.delete("layer_status")

    if get_layer() is not None:
        canvas.create_text(
            180,
            350,
            text="Plik załadowany poprawnie",
            fill="#76A2D7",
            tags="layer_status"
        )