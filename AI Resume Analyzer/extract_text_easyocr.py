import easyocr
import os

def extract_text_easyocr(image_path):
    print(f"Opening image: {image_path}")
    if not os.path.exists(image_path):
        print("Image file not found!")
        return ""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path, detail=0)
    print(f"Detected {len(result)} text elements")
    return "\n".join(result)

if __name__ == "__main__":
    image_path = "resume.png"
    extracted_text = extract_text_easyocr(image_path)

    if extracted_text.strip() == "":
        print("No text extracted from the image.")
    else:
        with open("resume_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print("Text extracted and saved to resume_text.txt")
        print(f"Extracted text length: {len(extracted_text)} characters")
