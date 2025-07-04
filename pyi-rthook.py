import sys

if getattr(sys, "frozen", False):
    sys.path.append(sys._MEIPASS)  # type: ignore
