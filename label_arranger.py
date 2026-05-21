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
import ui

def get_user_inputs():
    ui.clear_screen()
    ui.print_banner()
    ui.print_info("Trasforma le tue immagini in etichette PDF pronte da stampare")
    print()

    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        if os.path.isfile(config_path) and config_path.endswith('.json'):
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    params = json.load(f)
                params['input_folder'] = os.path.dirname(config_path)
                ui.print_success(f"Configurazione caricata da {config_path}")
                return params
            else:
                ui.print_error(f"File di configurazione non trovato: {config_path}")
                sys.exit(1)
        elif os.path.isdir(config_path):
            input_folder = config_path
            config_path_file = os.path.join(input_folder, 'config.json')
            if os.path.exists(config_path_file):
                with open(config_path_file, 'r') as f:
                    params = json.load(f)
                params['input_folder'] = input_folder
                ui.print_success("Configurazione caricata da config.json")
                return params
            else:
                ui.print_step("Scegli il tipo di etichetta")
                options = [
                    ('1', 'Grande (153 x 153 mm)'),
                    ('2', 'Stretta (108 x 147 mm)'),
                    ('3', 'Personalizzato'),
                ]
                ui.print_menu(options)
                choice = ui.get_menu_choice(options)

                if choice is None:
                    ui.print_info("Operazione annullata.")
                    sys.exit(0)

                if choice == "1":
                    label_width, label_height = 153, 153
                    ui.print_success("Etichette Grandi selezionate (153 x 153 mm)")
                elif choice == "2":
                    label_width, label_height = 108, 147
                    ui.print_success("Etichette Strette selezionate (108 x 147 mm)")
                else:
                    print()
                    ui.print_info("Inserisci le dimensioni personalizzate")
                    sheet_format = input("Formato foglio (A4/A3) [default A3]: ").strip().upper()
                    if not sheet_format:
                        sheet_format = "A3"
                    while sheet_format not in ("A4", "A3"):
                        sheet_format = input("Formato non valido. Usa A4 o A3 [default A3]: ").strip().upper()
                        if not sheet_format:
                            sheet_format = "A3"

                    label_width = input("Larghezza etichetta (mm) [default 153]: ").strip()
                    label_width = float(label_width) if label_width else 153

                    label_height = input("Altezza etichetta (mm) [default 153]: ").strip()
                    label_height = float(label_height) if label_height else 153

                    ui.print_success(f"Dimensioni personalizzate: {label_width}x{label_height} mm")

                params = {
                    'input_folder': input_folder,
                    'output_folder': 'out',
                    'sheet_format': 'A3',
                    'unit': 'mm',
                    'label_width': label_width,
                    'label_height': label_height,
                    'margins': {'top': 20, 'bottom': 20, 'left': 20, 'right': 20},
                    'gaps': {'h': 0, 'v': 0},
                    'rotate': True,
                    'sort_option': 'none'
                }
                return params
        else:
            ui.print_error(f"Percorso non valido: {config_path}")
            sys.exit(1)
    else:
        input_folder = input("Inserisci il nome della cartella con le immagini: ").strip()
        if not os.path.isdir(input_folder):
            ui.print_error(f"La cartella '{input_folder}' non esiste.")
            sys.exit(1)

        config_path = os.path.join(input_folder, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                params = json.load(f)
            params['input_folder'] = input_folder
            ui.print_success("Configurazione caricata da config.json")
            return params
        else:
            ui.print_step("Scegli il tipo di etichetta")
            options = [
                ('1', 'Grande (153 x 153 mm)'),
                ('2', 'Stretta (108 x 147 mm)'),
                ('3', 'Personalizzato'),
            ]
            ui.print_menu(options)
            choice = ui.get_menu_choice(options)

            if choice is None:
                ui.print_info("Operazione annullata.")
                sys.exit(0)

            if choice == "1":
                label_width, label_height = 153, 153
                ui.print_success("Etichette Grandi selezionate (153 x 153 mm)")
            elif choice == "2":
                label_width, label_height = 108, 147
                ui.print_success("Etichette Strette selezionate (108 x 147 mm)")
            else:
                print()
                ui.print_info("Inserisci le dimensioni personalizzate")
                sheet_format = input("Formato foglio (A4/A3) [default A3]: ").strip().upper()
                if not sheet_format:
                    sheet_format = "A3"
                while sheet_format not in ("A4", "A3"):
                    sheet_format = input("Formato non valido. Usa A4 o A3 [default A3]: ").strip().upper()
                    if not sheet_format:
                        sheet_format = "A3"

                label_width = input("Larghezza etichetta (mm) [default 153]: ").strip()
                label_width = float(label_width) if label_width else 153

                label_height = input("Altezza etichetta (mm) [default 153]: ").strip()
                label_height = float(label_height) if label_height else 153

                ui.print_success(f"Dimensioni personalizzate: {label_width}x{label_height} mm")

            params = {
                'input_folder': input_folder,
                'output_folder': 'out',
                'sheet_format': 'A3',
                'unit': 'mm',
                'label_width': label_width,
                'label_height': label_height,
                'margins': {'top': 20, 'bottom': 20, 'left': 20, 'right': 20},
                'gaps': {'h': 0, 'v': 0},
                'rotate': True,
                'sort_option': 'none'
            }
            return params

def load_images(folder_path):
    supported_ext = ('.jpg', '.jpeg', '.png')
    images = []
    if not os.path.isdir(folder_path):
        ui.print_error(f"La cartella '{folder_path}' non esiste.")
        return images

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(supported_ext):
                filepath = os.path.join(root, filename)
                try:
                    img = Image.open(filepath)
                    images.append((filename, img))
                except Exception as e:
                    ui.print_warning(f"Impossibile caricare '{filename}': {e}")
    return images

def sort_images(images, sort_option):
    if sort_option == 'name':
        images.sort(key=lambda x: x[0])
    elif sort_option == 'size':
        images.sort(key=lambda x: x[1].size[0] * x[1].size[1], reverse=True)

def process_image(img, label_width, label_height, unit, rotate_images, temp_dir, img_name):
    dpi = 300
    if unit == 'mm':
        factor = dpi / 25.4
    else:
        factor = dpi

    if rotate_images:
        img = img.rotate(-90)

    label_w_px = int(label_width * factor)
    label_h_px = int(label_height * factor)

    img_ratio = img.width / img.height
    label_ratio = label_w_px / label_h_px

    if img_ratio > label_ratio:
        new_width = label_w_px
        new_height = int(label_w_px / img_ratio)
    else:
        new_height = label_h_px
        new_width = int(label_h_px * img_ratio)

    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

    final_img = Image.new('RGB', (label_w_px, label_h_px), (255, 255, 255))
    x_offset = (label_w_px - new_width) // 2
    y_offset = (label_h_px - new_height) // 2
    final_img.paste(resized_img, (x_offset, y_offset))

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

def draw_grid(c, x_start, y_start, cols, rows, label_w, label_h, gap_h, gap_v, sheet_width, sheet_height):
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    for i in range(cols + 1):
        x = x_start + i * (label_w + gap_h)
        c.line(x, 0, x, sheet_height)
    for j in range(rows + 1):
        y = y_start - j * (label_h + gap_v)
        c.line(0, y, sheet_width, y)
    c.setDash()

def generate_pdf(images, params, output_path):
    sheet_size = A4 if params['sheet_format'] == 'A4' else A3
    cols, rows = calculate_grid(sheet_size, params['margins'], params['gaps'],
                                params['label_width'], params['label_height'], params['unit'])

    c = canvas.Canvas(output_path, pagesize=sheet_size)
    ui.print_info(f"Generazione PDF: {output_path}")

    unit_conv = mm if params['unit'] == 'mm' else inch

    x_start = params['margins']['left'] * unit_conv
    y_start = sheet_size[1] - params['margins']['top'] * unit_conv
    gap_h = params['gaps']['h'] * unit_conv
    gap_v = params['gaps']['v'] * unit_conv
    label_w = params['label_width'] * unit_conv
    label_h = params['label_height'] * unit_conv

    total_images = len(images)
    counter = 0
    idx = 0
    page_count = 1
    for img_name, img_path in images:
        counter += 1
        ui.print_progress(counter, total_images, f"Elaborazione immagini")
        if idx >= cols * rows:
            draw_grid(c, x_start, y_start, cols, rows, label_w, label_h, gap_h, gap_v, sheet_size[0], sheet_size[1])
            filename = os.path.basename(output_path)
            c.setFont("Helvetica", 8)
            c.drawString(10*unit_conv, 5*unit_conv, filename)
            c.showPage()
            idx = 0
            page_count += 1

        col = idx // rows
        row = idx % rows

        x = x_start + col * (label_w + gap_h)
        y = y_start - row * (label_h + gap_v) - label_h

        c.drawImage(img_path, x, y, label_w, label_h)

        idx += 1

    draw_grid(c, x_start, y_start, cols, rows, label_w, label_h, gap_h, gap_v, sheet_size[0], sheet_size[1])

    filename = os.path.basename(output_path)
    c.setFont("Helvetica", 8)
    c.drawString(10*unit_conv, 5*unit_conv, filename)

    try:
        c.save()
        ui.print_success(f"PDF generato con {page_count} pagina(e): {output_path}")
    except PermissionError:
        ui.print_error("Impossibile salvare il PDF. Il file potrebbe essere aperto in un altro programma.")
        ui.print_info(f"Percorso: {output_path}")

def process_batch(params):
    if 'pdf_name' not in params:
        params['pdf_name'] = os.path.basename(params['input_folder']) + ".pdf"

    output_folder = params['output_folder']
    if not os.path.isabs(output_folder):
        output_folder = os.path.join(os.getcwd(), output_folder)

    if not os.path.isdir(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            ui.print_error(f"Impossibile creare la cartella di output: {e}")
            return

    unit_conv = mm if params['unit'] == 'mm' else inch
    sheet_size = A4 if params['sheet_format'] == 'A4' else A3
    usable_w = sheet_size[0] - params['margins']['left']*unit_conv - params['margins']['right']*unit_conv
    usable_h = sheet_size[1] - params['margins']['top']*unit_conv - params['margins']['bottom']*unit_conv

    label_w = params['label_width'] * unit_conv
    label_h = params['label_height'] * unit_conv

    if label_w > usable_w or label_h > usable_h:
        ui.print_error("Le dimensioni dell'etichetta sono troppo grandi per il foglio.")
        return

    ui.print_step("Caricamento immagini")
    images = load_images(params['input_folder'])
    if not images:
        ui.print_error(f"Nessuna immagine trovata nella cartella: {params['input_folder']}")
        ui.print_info("Assicurati che i file siano in formato .jpg, .jpeg o .png")
        return

    ui.print_success(f"{len(images)} immagini caricate")

    sort_images(images, params['sort_option'])

    rotate_images = False
    if params['rotate'] and params['label_width'] != params['label_height']:
        sheet_size = A4 if params['sheet_format'] == 'A4' else A3
        cols_n, rows_n = calculate_grid(sheet_size, params['margins'], params['gaps'],
                                        params['label_width'], params['label_height'], params['unit'])
        per_page_n = cols_n * rows_n
        cols_r, rows_r = calculate_grid(sheet_size, params['margins'], params['gaps'],
                                        params['label_height'], params['label_width'], params['unit'])
        per_page_r = cols_r * rows_r
        if per_page_r > per_page_n:
            rotate_images = True
            ui.print_info("Ruotamento immagini per ottimizzare lo spazio")

    ui.print_step("Elaborazione immagini")
    temp_dir = tempfile.mkdtemp()

    processed_images = []
    for name, img in images:
        processed_path = process_image(img, params['label_width'], params['label_height'],
                                       params['unit'], rotate_images, temp_dir, name)
        processed_images.append((name, processed_path))

    ui.print_success(f"{len(processed_images)} immagini elaborate")

    ui.print_step("Generazione PDF")
    output_path = os.path.join(output_folder, params['pdf_name'])
    generate_pdf(processed_images, params, output_path)

    import shutil
    shutil.rmtree(temp_dir)

def main():
    params = get_user_inputs()

    input_folder = params['input_folder']
    if 'output_folder' in params:
        process_batch(params)
    else:
        subfolders = []
        for root, dirs, files in os.walk(input_folder):
            if 'config.json' in files:
                subfolders.append(root)

        if not subfolders:
            ui.print_step("Scegli il tipo di etichetta")
            options = [
                ('1', 'Grande (153 x 153 mm)'),
                ('2', 'Stretta (108 x 147 mm)'),
                ('3', 'Personalizzato'),
            ]
            ui.print_menu(options)
            choice = ui.get_menu_choice(options)

            if choice is None:
                ui.print_info("Operazione annullata.")
                return

            sheet_format = "A3"
            if choice == "1":
                label_width, label_height = 153, 153
                ui.print_success("Etichette Grandi selezionate (153 x 153 mm)")
            elif choice == "2":
                label_width, label_height = 108, 147
                ui.print_success("Etichette Strette selezionate (108 x 147 mm)")
            else:
                print()
                sheet_format = input("Formato foglio (A4/A3) [default A3]: ").strip().upper()
                if not sheet_format:
                    sheet_format = "A3"
                while sheet_format not in ("A4", "A3"):
                    sheet_format = input("Formato non valido. Usa A4 o A3 [default A3]: ").strip().upper()
                    if not sheet_format:
                        sheet_format = "A3"

                label_width = input("Larghezza etichetta (mm) [default 153]: ").strip()
                label_width = float(label_width) if label_width else 153

                label_height = input("Altezza etichetta (mm) [default 153]: ").strip()
                label_height = float(label_height) if label_height else 153

            sub_params = {
                'input_folder': input_folder,
                'output_folder': 'out',
                'sheet_format': sheet_format,
                'unit': 'mm',
                'label_width': label_width,
                'label_height': label_height,
                'margins': {'top': 20, 'bottom': 20, 'left': 20, 'right': 20},
                'gaps': {'h': 0, 'v': 0},
                'rotate': True,
                'sort_option': 'none'
            }
            ui.print_success(f"Dimensioni: foglio {sheet_format}, etichetta {label_width}x{label_height} mm")
            process_batch(sub_params)
            return

        ui.print_info(f"Trovate {len(subfolders)} cartelle con config.json")

        for sub in subfolders:
            batch_num = subfolders.index(sub) + 1
            print()
            ui.print_step(f"Elaborazione {batch_num}/{len(subfolders)}: {os.path.basename(sub)}")
            config_path = os.path.join(sub, 'config.json')
            with open(config_path, 'r') as f:
                sub_params = json.load(f)
            sub_params['input_folder'] = sub
            process_batch(sub_params)

    print()
    ui.print_success("Operazione completata!")

    while True:
        print()
        choice = input("Vuoi creare altre etichette? [S/N]: ").strip().upper()
        if choice in ('S', 'SI'):
            main()
            break
        elif choice in ('N', 'NO'):
            ui.print_info("Arrivederci! Grazie per aver usato Auto Layout Etichette.")
            break
        print("Rispondi S per continuare o N per uscire.")

if __name__ == "__main__":
    main()