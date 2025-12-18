#!/usr/bin/env python3
"""
Auto Layout Etichette - Image Label Arranger

This script processes a folder of images, arranges them efficiently onto A4 or A3 sheets
to minimize wasted space, and outputs the result as a high-resolution PDF with cut lines.

Requirements:
- Pillow (PIL)
- ReportLab

Install with: pip install pillow reportlab
"""

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3
from reportlab.lib.units import mm, inch
import os
import sys
import tempfile
import json

def get_user_inputs():
    """
    Interactively prompt the user for all required inputs, or load from config.json if available.
    """
    print("Auto Layout Etichette - Image to PDF Arranger")
    print("=" * 50)

    input_folder = input("Enter input folder path containing images: ").strip()
    config_path = os.path.join(input_folder, 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            params = json.load(f)
        print(f"Loaded configuration from {config_path}")
        return params
    else:
        output_folder = input("Enter output folder path for PDF: ").strip()

        sheet_format = input("Sheet format (A4 or A3): ").strip().upper()
        while sheet_format not in ['A4', 'A3']:
            sheet_format = input("Invalid. Sheet format (A4 or A3): ").strip().upper()

        unit = input("Units for dimensions (mm or inch): ").strip().lower()
        while unit not in ['mm', 'inch']:
            unit = input("Invalid. Units (mm or inch): ").strip().lower()

        try:
            label_width = float(input("Label width: ").strip())
            label_height = float(input("Label height: ").strip())
            margins_top = float(input("Top margin: ").strip())
            margins_bottom = float(input("Bottom margin: ").strip())
            margins_left = float(input("Left margin: ").strip())
            margins_right = float(input("Right margin: ").strip())
            gap_h = float(input("Horizontal gap between labels: ").strip())
            gap_v = float(input("Vertical gap between labels: ").strip())
        except ValueError:
            print("Invalid numeric input. Exiting.")
            sys.exit(1)

        rotate = input("Allow rotation for better fit? (y/n): ").strip().lower() == 'y'

        pdf_name = input("PDF filename (default 'arranged_labels.pdf'): ").strip()
        if not pdf_name:
            pdf_name = "arranged_labels.pdf"

        sort_option = input("Sort images by (name/size/none): ").strip().lower()
        while sort_option not in ['name', 'size', 'none']:
            sort_option = input("Invalid. Sort by (name/size/none): ").strip().lower()

        return {
            'input_folder': input_folder,
            'output_folder': output_folder,
            'sheet_format': sheet_format,
            'unit': unit,
            'label_width': label_width,
            'label_height': label_height,
            'margins': {'top': margins_top, 'bottom': margins_bottom, 'left': margins_left, 'right': margins_right},
            'gaps': {'h': gap_h, 'v': gap_v},
            'rotate': rotate,
            'pdf_name': pdf_name,
            'sort_option': sort_option
        }

def load_images(folder_path):
    """
    Load all supported images from the input folder.
    Supports JPEG and PNG formats.
    """
    supported_ext = ('.jpg', '.jpeg', '.png')
    images = []
    if not os.path.isdir(folder_path):
        print(f"Error: Input folder '{folder_path}' does not exist.")
        return images

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_ext):
            filepath = os.path.join(folder_path, filename)
            try:
                img = Image.open(filepath)
                images.append((filename, img))
            except Exception as e:
                print(f"Error loading image '{filename}': {e}")
    return images

def sort_images(images, sort_option):
    """
    Sort the list of images based on the specified option.
    """
    if sort_option == 'name':
        images.sort(key=lambda x: x[0])
    elif sort_option == 'size':
        images.sort(key=lambda x: x[1].size[0] * x[1].size[1], reverse=True)
    # 'none': no sorting

def process_image(img, label_width, label_height, unit, allow_rotate, temp_dir, img_name):
    """
    Resize the image to fit within the label dimensions while maintaining aspect ratio.
    Save to temp file and return path.
    Optionally allow rotation for better fit (not implemented for same-size labels).
    """
    # Convert dimensions to pixels (assuming 300 DPI)
    dpi = 300
    if unit == 'mm':
        factor = dpi / 25.4  # mm to pixels
    else:
        factor = dpi  # inches to pixels

    label_w_px = int(label_width * factor)
    label_h_px = int(label_height * factor)

    # Calculate resize to fit
    img_ratio = img.width / img.height
    label_ratio = label_w_px / label_h_px

    if img_ratio > label_ratio:
        # Image is wider, fit to width
        new_width = label_w_px
        new_height = int(label_w_px / img_ratio)
    else:
        # Image is taller, fit to height
        new_height = label_h_px
        new_width = int(label_h_px * img_ratio)

    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

    # Create a new image with label size, paste resized in center
    final_img = Image.new('RGB', (label_w_px, label_h_px), (255, 255, 255))
    x_offset = (label_w_px - new_width) // 2
    y_offset = (label_h_px - new_height) // 2
    final_img.paste(resized_img, (x_offset, y_offset))

    # Save to temp file
    temp_path = os.path.join(temp_dir, img_name)
    final_img.save(temp_path, 'PNG')

    return temp_path

def calculate_grid(sheet_size, margins, gaps, label_width, label_height, unit):
    unit_conv = mm if unit == 'mm' else inch

    usable_w = sheet_size[0] - margins['left']*unit_conv - margins['right']*unit_conv
    usable_h = sheet_size[1] - margins['top']*unit_conv - margins['bottom']*unit_conv

    label_w = label_width * unit_conv
    label_h = label_height * unit_conv

    gap_h = gaps['h'] * unit_conv
    gap_v = gaps['v'] * unit_conv

    cols = max(1, int((usable_w + gap_h) / (label_w + gap_h)))
    rows = max(1, int((usable_h + gap_v) / (label_h + gap_v)))

    return cols, rows

def generate_pdf(images, params, output_path):
    """
    Generate the PDF with arranged images and cut lines.
    """
    sheet_size = A4 if params['sheet_format'] == 'A4' else A3
    cols, rows = calculate_grid(sheet_size, params['margins'], params['gaps'],
                                params['label_width'], params['label_height'], params['unit'])

    c = canvas.Canvas(output_path, pagesize=sheet_size)

    # Unit conversion for ReportLab

    unit_conv = mm if params['unit'] == 'mm' else inch

    x_start = params['margins']['left'] * unit_conv
    y_start = sheet_size[1] - params['margins']['top'] * unit_conv
    gap_h = params['gaps']['h'] * unit_conv
    gap_v = params['gaps']['v'] * unit_conv
    label_w = params['label_width'] * unit_conv
    label_h = params['label_height'] * unit_conv

    print(f"DEBUG: unit_conv={unit_conv}, x_start={x_start:.2f}, y_start={y_start:.2f}, label_w={label_w:.2f}, label_h={label_h:.2f}")

    idx = 0
    page_count = 1
    for img_name, img_path in images:
        if idx >= cols * rows:
            c.showPage()
            idx = 0
            page_count += 1

        col = idx // rows
        row = idx % rows

        x = x_start + col * (label_w + gap_h)
        y = y_start - row * (label_h + gap_v) - label_h

        # Draw image
        c.drawImage(img_path, x, y, label_w, label_h)

        # Draw cut lines (dashed)
        c.setLineWidth(0.5)
        c.setDash(2, 2)  # Dashed line
        c.rect(x, y, label_w, label_h)
        c.setDash()  # Reset to solid

        idx += 1

    try:
        c.save()
        print(f"PDF generated with {page_count} page(s): {output_path}")
    except PermissionError:
        print(f"Error saving PDF: permission denied. The file may be open in another program. Close it and try again.")
        print(f"Output path: {output_path}")

def main():
    """
    Main function to orchestrate the script.
    """
    params = get_user_inputs()

    # Validate output folder
    if not os.path.isdir(params['output_folder']):
        try:
            os.makedirs(params['output_folder'])
        except Exception as e:
            print(f"Error creating output folder: {e}")
            return

    # Validate label size fits on sheet
    unit_conv = mm if params['unit'] == 'mm' else inch
    sheet_size = A4 if params['sheet_format'] == 'A4' else A3
    usable_w = sheet_size[0] - params['margins']['left']*unit_conv - params['margins']['right']*unit_conv
    usable_h = sheet_size[1] - params['margins']['top']*unit_conv - params['margins']['bottom']*unit_conv

    label_w = params['label_width'] * unit_conv
    label_h = params['label_height'] * unit_conv

    if label_w > usable_w or label_h > usable_h:
        print("Error: Label dimensions are too large for the sheet with given margins.")
        return

    # Load and process images
    images = load_images(params['input_folder'])
    if not images:
        print("No valid images found in the input folder.")
        return

    sort_images(images, params['sort_option'])

    # Optimize orientation if rotation allowed and labels not square
    if params['rotate'] and params['label_width'] != params['label_height']:
        # Calculate per page for normal
        sheet_size = A4 if params['sheet_format'] == 'A4' else A3
        cols_n, rows_n = calculate_grid(sheet_size, params['margins'], params['gaps'],
                                        params['label_width'], params['label_height'], params['unit'])
        per_page_n = cols_n * rows_n
        # For rotated
        cols_r, rows_r = calculate_grid(sheet_size, params['margins'], params['gaps'],
                                        params['label_height'], params['label_width'], params['unit'])
        per_page_r = cols_r * rows_r
        if per_page_r > per_page_n:
            params['label_width'], params['label_height'] = params['label_height'], params['label_width']
            print("Using rotated label orientation for better packing density.")

    # Create temp directory for processed images
    temp_dir = tempfile.mkdtemp()

    processed_images = []
    for name, img in images:
        processed_path = process_image(img, params['label_width'], params['label_height'],
                                       params['unit'], params['rotate'], temp_dir, name)
        processed_images.append((name, processed_path))

    # Generate PDF
    output_path = os.path.join(params['output_folder'], params['pdf_name'])
    generate_pdf(processed_images, params, output_path)

    # Clean up temp dir
    import shutil
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()