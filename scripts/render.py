# -*- coding: utf-8 -*-
"""Рендерит первый PDF из корня репозитория в pages/NN.webp + pages/pages.json."""
import glob, json, os, shutil, datetime
import pymupdf

TARGET_WIDTH = 1800   # ширина картинки в пикселях
QUALITY      = 80     # качество WebP
OUT_DIR      = "pages"

pdfs = sorted(glob.glob("*.pdf"))
if not pdfs:
    raise SystemExit("В корне репозитория нет ни одного PDF")
src = pdfs[0]
print("Исходник:", src)

shutil.rmtree(OUT_DIR, ignore_errors=True)
os.makedirs(OUT_DIR, exist_ok=True)

doc = pymupdf.open(src)
total = 0
for i, page in enumerate(doc):
    zoom = TARGET_WIDTH / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
    path = os.path.join(OUT_DIR, f"{i+1:02d}.webp")
    pix.pil_save(path, format="WEBP", quality=QUALITY, method=5)
    size = os.path.getsize(path)
    total += size
    print(f"  {i+1:02d}.webp  {pix.width}x{pix.height}  {size/1024:.0f} KB")

meta = {
    "count": len(doc),
    "pdf": src,
    "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
}
with open(os.path.join(OUT_DIR, "pages.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f"Готово: {len(doc)} стр., {total/1024/1024:.2f} МБ")
