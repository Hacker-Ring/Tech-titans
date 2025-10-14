import gradio as gr
import pytesseract
from PIL import Image
import requests
import os

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def ocr_interface(image):
    try:
        # Perform OCR
        text = pytesseract.image_to_string(Image.open(image))
    except Exception as e:
        return f"OCR Error: {str(e)}\nPlease ensure Tesseract is installed and the path is correct."
    # Debug: Show OCR text
    debug_info = f"OCR Text:\n{text}\n\n"
    # Search for books using recognized text
    params = {"q": text, "maxResults": 5}
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        if response.status_code != 200:
            return debug_info + f"Book API Error: HTTP {response.status_code} - {response.text}"
        books = response.json().get("items", [])
    except Exception as e:
        return debug_info + f"Book API Error: {str(e)}"
    if not books:
        return debug_info + "No book recommendations found for the recognized text."
    # Recommend books (simple: list top 5)
    recommendations = []
    for book in books:
        info = book.get("volumeInfo", {})
        title = info.get("title", "Unknown Title")
        authors = ", ".join(info.get("authors", ["Unknown Author"]))
        link = info.get("infoLink", "")
        recommendations.append(f"{title} by {authors}\n{link}")
    result = debug_info + "Book Recommendations:\n" + "\n\n".join(recommendations)
    return result

iface = gr.Interface(
    fn=ocr_interface,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="OCR Recognition & Book Finder",
    description="Upload an image to perform OCR and get book recommendations from Google Books."
)

if __name__ == "__main__":
    iface.launch()
import gradio as gr
import pytesseract
from PIL import Image
import requests
import os

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def ocr_interface(image):
    try:
        # Perform OCR
        text = pytesseract.image_to_string(Image.open(image))
    except Exception as e:
        return f"OCR Error: {str(e)}\nPlease ensure Tesseract is installed and the path is correct."
    # Debug: Show OCR text
    debug_info = f"OCR Text:\n{text}\n\n"
    # Search for books using recognized text
    params = {"q": text, "maxResults": 5}
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        if response.status_code != 200:
            return debug_info + f"Book API Error: HTTP {response.status_code} - {response.text}"
        books = response.json().get("items", [])
    except Exception as e:
        return debug_info + f"Book API Error: {str(e)}"
    if not books:
        return debug_info + "No book recommendations found for the recognized text."
    # Recommend books (simple: list top 5)
    recommendations = []
    for book in books:
        info = book.get("volumeInfo", {})
        title = info.get("title", "Unknown Title")
        authors = ", ".join(info.get("authors", ["Unknown Author"]))
        link = info.get("infoLink", "")
        recommendations.append(f"{title} by {authors}\n{link}")
    result = debug_info + "Book Recommendations:\n" + "\n\n".join(recommendations)
    return result

iface = gr.Interface(
    fn=ocr_interface,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="OCR Recognition & Book Finder",
    description="Upload an image to perform OCR and get book recommendations from Google Books."
)

if __name__ == "__main__":
    iface.launch()

import gradio as gr
import pytesseract
from PIL import Image
import requests
import os

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def ocr_interface(image):
    try:
        # Perform OCR
        text = pytesseract.image_to_string(Image.open(image))
    except Exception as e:
        return f"OCR Error: {str(e)}\nPlease ensure Tesseract is installed and the path is correct."
    # Debug: Show OCR text
    debug_info = f"OCR Text:\n{text}\n\n"
    # Search for books using recognized text
    params = {"q": text, "maxResults": 5}
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        if response.status_code != 200:
            return debug_info + f"Book API Error: HTTP {response.status_code} - {response.text}"
        books = response.json().get("items", [])
    except Exception as e:
        return debug_info + f"Book API Error: {str(e)}"
    if not books:
        return debug_info + "No book recommendations found for the recognized text."
    # Recommend books (simple: list top 5)
    recommendations = []
    for book in books:
        info = book.get("volumeInfo", {})
        title = info.get("title", "Unknown Title")
        authors = ", ".join(info.get("authors", ["Unknown Author"]))
        link = info.get("infoLink", "")
        recommendations.append(f"{title} by {authors}\n{link}")
    result = debug_info + "Book Recommendations:\n" + "\n\n".join(recommendations)
    return result

iface = gr.Interface(
    fn=ocr_interface,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="OCR Recognition & Book Finder",
    description="Upload an image to perform OCR and get book recommendations from Google Books."
)

if __name__ == "__main__":
    iface.launch()
