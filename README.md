# Auto Layout Etichette

Python CLI per creare layout di etichette ottimizzati su fogli A4/A3 con linee di taglio.

A Python script to arrange images onto A4 or A3 sheets efficiently, minimizing wasted space, and generate a high-resolution PDF with cut lines for labels.

## Requirements

- Python 3.x
- Pillow (PIL)
- ReportLab

Install dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the script from the command line:
```
python label_arranger.py
```

The script will interactively prompt for:
- Input folder path containing images (JPEG, PNG)
- Output folder path for the PDF
- Sheet format (A4 or A3)
- Units (mm or inch)
- Label dimensions (width, height)
- Margins (top, bottom, left, right)
- Gaps between labels (horizontal, vertical)
- Option to allow rotation (currently not implemented for same-size labels)
- PDF filename (default: arranged_labels.pdf)
- Sorting option (by name, size, or none)

## Features

- Resizes images to fit label dimensions while maintaining aspect ratio
- Arranges labels in a grid layout to minimize waste
- Handles multiple pages if needed
- Generates PDF with 300 DPI resolution
- Adds dashed cut lines around each label
- Supports sorting images before arrangement
- Error handling for invalid inputs and missing files

## Notes

- Images are fitted to the label size without cropping (centered on white background if needed)
- Rotation option is included but not fully implemented as it's not necessary for same-size labels
- For best results, ensure images are high quality