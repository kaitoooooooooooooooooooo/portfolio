"""Capture de la fenêtre de PDF to Markdown pendant une vraie conversion.

    python tools/capture-pdf-to-markdown.py

Lance le code de l'application (previews-src/build/convert.py, copie du dépôt GitHub) sur un
dossier de 3 PDF de démonstration, choisit ce dossier à la place de la boîte de dialogue,
lance « Convert », puis photographie la fenêtre quand la conversion est finie.
Sortie : previews-src/raw/pdf-to-markdown.png
"""
import ctypes
import os
import ctypes.wintypes
import tkinter.filedialog as filedialog
from pathlib import Path

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "previews-src" / "build" / "convert.py"
# Dossier court pour que le chemin affiché reste lisible ; PDF_DEMO pour en choisir un autre.
DEMO = Path(os.environ.get("PDF_DEMO", ROOT / "previews-src" / "build" / "pdf-demo"))
OUT = ROOT / "previews-src" / "raw" / "pdf-to-markdown.png"

ctypes.windll.shcore.SetProcessDpiAwareness(2)  # pixels réels : capture nette et coordonnées justes
filedialog.askdirectory = lambda **kw: str(DEMO)  # « Browse » choisit le dossier de démonstration


def window_rect(hwnd: int):
    """Bords visibles de la fenêtre, barre de titre comprise (sans l'ombre de Windows)."""
    r = ctypes.wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(hwnd, 9, ctypes.byref(r), ctypes.sizeof(r))  # DWMWA_EXTENDED_FRAME_BOUNDS
    return r.left, r.top, r.right, r.bottom


code = SRC.read_text(encoding="utf-8").replace("root.mainloop()", "")
ns: dict = {"__name__": "pdf_to_markdown"}
exec(compile(code, str(SRC), "exec"), ns)
root = ns["root"]
root.geometry("+160+160")
root.attributes("-topmost", True)


def shoot():
    root.update()
    hwnd = int(root.wm_frame(), 16)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ImageGrab.grab(bbox=window_rect(hwnd), all_screens=True).save(OUT)
    print("capture :", OUT, ns["status_label"].cget("text"))
    for md in DEMO.glob("*.md"):
        md.unlink()  # on ne garde que les PDF de démonstration
    root.destroy()


def wait_done(tries=0):
    if ns["status_label"].cget("text").startswith("Done") or tries > 60:
        root.after(400, shoot)
    else:
        root.after(200, wait_done, tries + 1)


root.after(600, ns["browse"])
root.after(1200, ns["convert"])
root.after(1500, wait_done)
root.mainloop()
