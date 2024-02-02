from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from PIL import Image

except ImportError:
    import os

    CMD = ["python -m venv .venv", ".venv/Scripts/activate", "pip install pillow"]
    for cmd in CMD:
        os.system(cmd)

    from PIL import Image


def convert(file: Path):
    img = Image.open(file)
    img.save(
        str(file).replace(".png", ".webp"), format="webp", optimize=True, quality=100
    )
    file.unlink()


def loader(path: str = "."):
    with ThreadPoolExecutor() as thread:
        for file in Path(path).iterdir():
            print(str(file))

            if file.is_dir() and "venv" not in file.name.lower():
                loader(str(file))

            if file.is_file() and file.name.endswith(".png"):
                thread.submit(convert, file)


if __name__ == "__main__":
    loader()
