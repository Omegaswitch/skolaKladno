#!/usr/bin/env python3
"""Recompresses migrated photos in static/media: JPEG quality 80 progressive, max 1600 px on the long side,
EXIF (camera location) removed, orientation applied. A file is replaced only if the result is smaller.

    pip install pillow && python3 tools/optimize_media.py
"""
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

MEDIA = Path(__file__).resolve().parent.parent / "static" / "media"
MAX = 1600


def one(f):
    try:
        im = ImageOps.exif_transpose(Image.open(f))
        if max(im.size) > MAX:
            im.thumbnail((MAX, MAX), Image.LANCZOS)
        buf = BytesIO()
        if f.suffix.lower() == ".png":
            if im.mode not in ("RGB", "RGBA", "L", "LA", "P"):
                im = im.convert("RGBA")
            im.save(buf, "PNG", optimize=True)
        else:
            im.convert("RGB").save(buf, "JPEG", quality=80, optimize=True, progressive=True)
        old = f.stat().st_size
        if buf.tell() < old * 0.95:
            f.write_bytes(buf.getvalue())
            return old - buf.tell()
    except Exception as e:  # a damaged file stays as it is
        print("skip", f, e)
    return 0


if __name__ == "__main__":
    files = [f for f in MEDIA.rglob("*") if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
    with ProcessPoolExecutor() as ex:
        saved = sum(ex.map(one, files, chunksize=16))
    print(f"{len(files)} images, saved {saved / 1e6:.0f} MB")
