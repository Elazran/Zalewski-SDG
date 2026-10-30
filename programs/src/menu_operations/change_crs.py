from tkinter import messagebox, simpledialog
from pyproj import CRS
from pyproj.exceptions import CRSError, ProjError

from src.data_service import get_layer, set_layer


def change_crs():
    layer = get_layer()

    if layer is None:
        return

    crs_input = simpledialog.askstring(
        "Zmiana układu współrzędnych",
        "Podaj docelowy układ współrzędnych (np. EPSG:2180):"
    )

    if crs_input is None:
        return

    try:
        target_crs = CRS.from_user_input(crs_input.strip())
    except CRSError:
        messagebox.showwarning(
            "Nieprawidłowy układ współrzędnych",
            "Nie rozpoznano podanego układu. Podaj poprawny kod lub opis CRS, "
            "np. EPSG:2180."
        )
        return

    try:
        transformed_layer = layer.to_crs(target_crs)
    except (ValueError, ProjError) as error:
        messagebox.showwarning(
            "Błąd zmiany układu współrzędnych",
            f"Nie udało się zmienić układu współrzędnych: {error}"
        )
        return

    set_layer(transformed_layer)
    messagebox.showinfo(
        "Zmieniono układ współrzędnych",
        f"Warstwa została przeliczona do układu {target_crs.to_string()}."
    )