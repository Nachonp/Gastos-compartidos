import cv2
import pytesseract
import sys

# Configurar la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extraer_texto_de_imagen(ruta_imagen):
    """Extrae el texto de una imagen utilizando OCR."""
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("Error: No se pudo cargar la imagen. Verifique el archivo.")
        sys.exit(1)

    return pytesseract.image_to_string(imagen).strip()
