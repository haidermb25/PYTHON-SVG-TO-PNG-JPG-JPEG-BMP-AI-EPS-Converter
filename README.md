SVG Multi-Format Converter (Python)

This project converts SVG files into multiple formats such as PNG, JPG, JPEG, BMP, EPS, and AI using CairoSVG, Inkscape, and Ghostscript.

📖 About

A Python tool that converts SVG files into multiple image and design formats (PNG, JPG, EPS, AI) using Inkscape and CairoSVG.

🚀 Features
SVG to PNG conversion (with custom size support)
SVG to JPG / JPEG / BMP conversion
SVG to EPS conversion (via Inkscape)
SVG to AI conversion (via Ghostscript)
Automatic unique filename handling
Cross-tool integration (CairoSVG + Inkscape + Ghostscript)
⚙️ Requirements
Python 3.x
CairoSVG
Inkscape
Ghostscript
📦 Installation
pip install cairosvg

Also install:

Inkscape: https://inkscape.org
Ghostscript: https://www.ghostscript.com
▶️ Usage
convert_svg(
    input_svg="input.svg",
    output_file="output_path/filename",
    output_format="png",
    size=512
)
📌 Supported Formats
PNG
JPG
JPEG
BMP
EPS
AI
📂 Workflow
Load SVG file
Choose output format
Convert using appropriate tool
Save file with unique name
Return final converted file
