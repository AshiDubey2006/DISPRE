"""
Convert SVG diagram to JPG using cairosvg + Pillow
Run: python convert_svg_to_jpg.py
"""
import os
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
except Exception:
    # If libraries are missing, the script will be run after installing them
    pass

BASE = Path(__file__).resolve().parent
INPUT_SVG = BASE / 'output' / 'architecture_diagram.svg'
OUTPUT_PNG = BASE / 'output' / 'architecture_diagram_tmp.png'
OUTPUT_JPG = BASE / 'output' / 'architecture_diagram.jpg'

if not INPUT_SVG.exists():
    print(f"Input SVG not found: {INPUT_SVG}")
    raise SystemExit(1)

print(f"Converting SVG -> PNG -> JPG:\n  {INPUT_SVG}\n  -> {OUTPUT_JPG}")

# Convert SVG to PNG using cairosvg
cairosvg.svg2png(url=str(INPUT_SVG), write_to=str(OUTPUT_PNG))

# Open PNG and save as JPG using Pillow
img = Image.open(str(OUTPUT_PNG)).convert('RGB')
img.save(str(OUTPUT_JPG), quality=90)

# Clean up temporary PNG
try:
    OUTPUT_PNG.unlink()
except Exception:
    pass

print(f"Saved JPG: {OUTPUT_JPG}")
