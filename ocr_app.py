import gradio as gr
import pytesseract
from PIL import Image
import requests

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def ocr_interface(image):
    # Perform OCR
    text = pytesseract.image_to_string(Image.open(image))
    # Search for books using recognized text
    params = {"q": text, "maxResults": 5}
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    books = response.json().get("items", [])
    # Recommend books (simple: list top 5)
    recommendations = []
    for book in books:
        info = book.get("volumeInfo", {})
        title = info.get("title", "Unknown Title")
        authors = ", ".join(info.get("authors", ["Unknown Author"]))
        link = info.get("infoLink", "")
        recommendations.append(f"{title} by {authors}\n{link}")
    result = f"OCR Text:\n{text}\n\nBook Recommendations:\n" + "\n\n".join(recommendations)
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
