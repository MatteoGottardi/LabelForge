from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.colors import HexColor
import os

def create_manual():
    output_path = os.path.join("docs", "Manuale_Utente_Auto_Layout_Etichette.pdf")
    os.makedirs("docs", exist_ok=True)
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    title_font = "Helvetica-Bold"
    body_font = "Helvetica"
    title_size = 24
    heading_size = 16
    body_size = 12
    
    def draw_page_number(page_num):
        c.setFont(body_font, 10)
        c.setFillColor(HexColor("#666666"))
        c.drawRightString(width - 20*mm, 15*mm, f"Pagina {page_num}")
        c.setFillColor(HexColor("#000000"))
    
    # ============ PAGINA 1 ============
    # Titolo principale
    c.setFont(title_font, title_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawCentredString(width/2, height - 40*mm, "Auto Layout Etichette")
    
    c.setFont(body_font, 16)
    c.setFillColor(HexColor("#333333"))
    c.drawCentredString(width/2, height - 55*mm, "Manuale per l'Utente")
    
    # Linea decorativa
    c.setStrokeColor(HexColor("#1a56db"))
    c.setLineWidth(2)
    c.line(50*mm, height - 65*mm, width - 50*mm, height - 65*mm)
    
    # Introduzione
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#000000"))
    intro_text = """Questo programma ti permette di creare etichette per la scuola in modo semplice e veloce. 
Trasforma le tue immagini in un PDF pronto da stampare, con le etichette già disposte sul foglio."""
    
    text_object = c.beginText(30*mm, height - 85*mm)
    text_object.setFont(body_font, body_size)
    text_object.setFillColor(HexColor("#333333"))
    for line in intro_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    # Cosa ti serve
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawString(20*mm, height - 110*mm, "Cosa ti serve:")
    
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#333333"))
    items = [
        "Un computer con Windows",
        "Le immagini delle etichette (create con Canva)",
        "Il programma Auto Layout Etichette"
    ]
    
    y_pos = height - 125*mm
    for item in items:
        c.setFillColor(HexColor("#1a56db"))
        c.circle(25*mm, y_pos + 3*mm, 3*mm, fill=1)
        c.setFillColor(HexColor("#333333"))
        c.drawString(32*mm, y_pos, item)
        y_pos -= 10*mm
    
    draw_page_number(1)
    c.showPage()
    
    # ============ PAGINA 2 ============
    # Passo 1
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawString(20*mm, height - 30*mm, "PASSO 1: Creare le immagini con Canva")
    
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#333333"))
    passo1_text = """Vai su canva.com e crea un nuovo design. Scegli le dimensioni dell'etichetta che ti serve:

• Grande (153 x 153 mm) - Quadrata
• Stretta (108 x 147 mm) - Rettangolare

IMPORTANTE: Crea l'immagine con le stesse proporzioni dell'etichetta che userai!"""
    
    text_object = c.beginText(20*mm, height - 50*mm)
    text_object.setFont(body_font, body_size)
    text_object.setFillColor(HexColor("#333333"))
    for line in passo1_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    # Passo 2
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawString(20*mm, height - 110*mm, "PASSO 2: Esportare da Canva")
    
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#333333"))
    passo2_text = """1. Fai clic su "Condividi" in alto a destra
2. Scegli "Scarica"
3. Seleziona formato PNG o JPG
4. Clicca su "Scarica il file"

Canva creerà un file ZIP. Estrai le immagini dalla cartella scaricata."""
    
    text_object = c.beginText(20*mm, height - 125*mm)
    text_object.setFont(body_font, body_size)
    text_object.setFillColor(HexColor("#333333"))
    for line in passo2_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    draw_page_number(2)
    c.showPage()
    
    # ============ PAGINA 3 ============
    # Passo 3
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawString(20*mm, height - 30*mm, "PASSO 3: Preparare la cartella")
    
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#333333"))
    passo3_text = """1. Apri la cartella dove si trova il file "Auto Layout Etichette.exe"
2. Crea una nuova cartella (clic destro > Nuovo > Cartella)
3. Dai alla cartella il nome che vuoi dare al tuo file PDF
   Esempio: se chiami la cartella "etichette2024", il PDF si chiamerà "etichette2024.pdf"
4. Metti tutte le immagini dentro questa cartella

La cartella deve stare nella stessa posizione del file .exe"""
    
    text_object = c.beginText(20*mm, height - 50*mm)
    text_object.setFont(body_font, body_size)
    text_object.setFillColor(HexColor("#333333"))
    for line in passo3_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    # Immagine示意
    c.setStrokeColor(HexColor("#cccccc"))
    c.setLineWidth(1)
    c.rect(50*mm, height - 170*mm, 100*mm, 50*mm)
    c.setFont(body_font, 10)
    c.setFillColor(HexColor("#666666"))
    c.drawCentredString(width/2, height - 145*mm, "Cartella vicino al file .exe")
    c.drawCentredString(width/2, height - 155*mm, "con le immagini dentro")
    
    draw_page_number(3)
    c.showPage()
    
    # ============ PAGINA 4 ============
    # Passo 4
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawString(20*mm, height - 30*mm, "PASSO 4: Eseguire il programma")
    
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#333333"))
    passo4_text = """1. Fai doppio clic su "Auto Layout Etichette.exe"
2. Il programma si aprirà in una finestra nera
3. Inserisci il nome della cartella che hai creato e premi INVIO
4. Scegli il tipo di etichetta:
   - Digita 1 e INVIO per etichette Grandi (153 x 153 mm)
   - Digita 2 e INVIO per etichette Strette (108 x 147 mm)
   - Digita 3 e INVIO per dimensioni personalizzate
5. Attendi che il programma finisca...
6. Alla fine, premi S e INVIO per creare altre etichette, oppure N e INVIO per uscire"""
    
    text_object = c.beginText(20*mm, height - 50*mm)
    text_object.setFont(body_font, body_size)
    text_object.setFillColor(HexColor("#333333"))
    for line in passo4_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    # Suggerimento
    c.setFillColor(HexColor("#f59e0b"))
    c.rect(20*mm, height - 190*mm, width - 40*mm, 25*mm, fill=1)
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#000000"))
    c.drawString(25*mm, height - 182*mm, "💡 Se hai dubbi, scegli sempre 1 (Grandi) - è la scelta più comune")
    
    draw_page_number(4)
    c.showPage()
    
    # ============ PAGINA 5 ============
    # Passo 5
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawString(20*mm, height - 30*mm, "PASSO 5: Trovare il tuo PDF")
    
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#333333"))
    passo5_text = """Il PDF è stato creato in una cartella chiamata "out".

Per trovarlo:
1. Torna nella cartella principale dove c'è il file .exe
2. Apri la cartella "out"
3. Qui trovi il tuo file PDF! Si chiama come la cartella che hai creato.

Ora puoi aprire il PDF e stamparlo."""
    
    text_object = c.beginText(20*mm, height - 50*mm)
    text_object.setFont(body_font, body_size)
    text_object.setFillColor(HexColor("#333333"))
    for line in passo5_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    # Risoluzione problemi
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#dc2626"))
    c.drawString(20*mm, height - 110*mm, "Problemi? Ecco le soluzioni:")
    
    c.setFont(body_font, body_size - 1)
    c.setFillColor(HexColor("#333333"))
    problemi_text = """• "Nessuna immagine trovata"
  - Controlla che le immagini siano nella cartella giusta
  - Devono essere file .jpg, .jpeg o .png

• Il PDF non si apre
  - Prova ad aprirlo con un altro programma (Chrome, Edge, Adobe Reader)

• Le etichette sono troppo grandi o piccole
  - Quando hai scelto il tipo, assicurati che le immagini Canva abbiano le stesse dimensioni

• Il programma si chiude subito
  - Probabilmente hai sbagliato nome cartella. Riprova."""
    
    text_object = c.beginText(20*mm, height - 125*mm)
    text_object.setFont(body_font, body_size - 1)
    text_object.setFillColor(HexColor("#333333"))
    for line in problemi_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    draw_page_number(5)
    c.showPage()
    
    # ============ PAGINA 6 (ULTIMA) ============
    # Consigli finali
    c.setFont(title_font, heading_size)
    c.setFillColor(HexColor("#1a56db"))
    c.drawString(20*mm, height - 30*mm, "Consigli utili")
    
    c.setFont(body_font, body_size)
    c.setFillColor(HexColor("#333333"))
    consigli_text = """• Usa immagini di buona qualità - il programma le ridimensiona, ma non può migliorarle

• Se hai molte etichette, organizzale in cartelle diverse - ogni cartella crea un PDF diverso

• Il foglio di stampa è A3 (formato grande) - controlla di avere una stampante compatibile

• Le linee tratteggiate sul PDF ti aiutano a tagliare dritto

• Stampa una pagina di prova prima di stampare tutto"""
    
    text_object = c.beginText(20*mm, height - 50*mm)
    text_object.setFont(body_font, body_size)
    text_object.setFillColor(HexColor("#333333"))
    for line in consigli_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    # Footer
    c.setStrokeColor(HexColor("#1a56db"))
    c.setLineWidth(2)
    c.line(20*mm, 40*mm, width - 20*mm, 40*mm)
    
    c.setFont(body_font, 10)
    c.setFillColor(HexColor("#666666"))
    c.drawCentredString(width/2, 25*mm, "Auto Layout Etichette - Manuale per l'Utente")
    c.drawCentredString(width/2, 18*mm, "Scuola Galilei")
    
    draw_page_number(6)
    c.save()
    
    print(f"Manuale creato: {output_path}")
    return output_path

if __name__ == "__main__":
    create_manual()