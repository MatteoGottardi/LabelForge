import os
import sys

os.system('') if sys.platform == 'win32' else None

COLORS = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
}

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        ascii_text = text.encode('ascii', 'replace').decode('ascii')
        print(ascii_text)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title=None):
    if title is None:
        title = "AUTO LAYOUT ETICHETTE"
    width = 50
    safe_print("")
    safe_print(COLORS['bold'] + COLORS['blue'] + "=" * width + COLORS['reset'])
    safe_print(COLORS['bold'] + COLORS['blue'] + f"  {title}".center(width) + COLORS['reset'])
    safe_print(COLORS['bold'] + COLORS['blue'] + "=" * width + COLORS['reset'])
    safe_print("")

def print_success(msg):
    safe_print(f"{COLORS['green']}[OK] {msg}{COLORS['reset']}")

def print_error(msg):
    safe_print(f"{COLORS['red']}[ERRORE] {msg}{COLORS['reset']}")

def print_info(msg):
    safe_print(f"{COLORS['cyan']}[INFO] {msg}{COLORS['reset']}")

def print_warning(msg):
    safe_print(f"{COLORS['yellow']}[ATTENZIONE] {msg}{COLORS['reset']}")

def print_step(msg):
    safe_print(f"\n{COLORS['bold']}{COLORS['blue']}==> {msg}{COLORS['reset']}")

def print_progress(current, total, prefix='', bar_length=30):
    if total == 0:
        return
    percent = int((current / total) * 100)
    filled = int((current / total) * bar_length) if bar_length > 0 else bar_length
    bar = '=' * filled + '-' * (bar_length - filled)
    sys.stdout.write(f'\r{prefix}: |{bar}| {percent}% ({current}/{total})')
    sys.stdout.flush()
    if current == total:
        print()

def confirm(msg):
    while True:
        response = input(f"{COLORS['yellow']}{msg} [S/N]{COLORS['reset']} ").strip().upper()
        if response in ('S', 'SI', 'Y', 'YES'):
            return True
        elif response in ('N', 'NO'):
            return False
        safe_print(f"{COLORS['yellow']}Rispondi S per si o N per no.{COLORS['reset']}")

def print_menu(options, title="Seleziona un'opzione:", exit_option="Q"):
    safe_print(COLORS['bold'] + title + COLORS['reset'])
    safe_print("")
    for key, label in options:
        safe_print(f"  [{COLORS['cyan']}{key}{COLORS['reset']}] {label}")
    if exit_option:
        safe_print(f"  [{COLORS['red']}{exit_option}{COLORS['reset']}] Esci")
    safe_print("")

def get_menu_choice(options, exit_option="Q"):
    while True:
        choice = input(f"{COLORS['bold']}> {COLORS['reset']}").strip().upper()
        keys = [k for k, _ in options]
        if choice == exit_option:
            return None
        if choice in keys:
            return choice
        safe_print(f"{COLORS['red']}Scelta non valida. Riprova.{COLORS['reset']}")

def print_banner():
    safe_print("")
    safe_print(f"{COLORS['bold']}{COLORS['blue']}")
    safe_print("   ██████╗  █████╗ ██╗     ██╗██╗     ███████╗██╗")
    safe_print("  ██╔════╝ ██╔══██╗██║     ██║██║     ██╔════╝██║")
    safe_print("  ██║  ███╗███████║██║     ██║██║     █████╗  ██║")
    safe_print("  ██║   ██║██╔══██║██║     ██║██║     ██╔══╝  ██║")
    safe_print("  ╚██████╔╝██║  ██║███████╗██║███████╗███████╗██║")
    safe_print("   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚══════╝╚═╝")
    safe_print("")
    safe_print("        " + "-" * 31)
    safe_print("        |   SISTEMA ETICHETTE SCUOLA  |")
    safe_print("        |          GALILEI            |")
    safe_print("        " + "-" * 31)
    safe_print(f"{COLORS['reset']}")