import pytesseract

def get_text_elements(image):
    results = pytesseract.image_to_data(image, lang='eng', output_type=pytesseract.Output.DICT)

    text_elements = []
    for i in range(len(results['text'])):
        text = results['text'][i].strip()
        if text:
            x = results['left'][i]
            y = results['top'][i]
            w = results['width'][i]
            h = results['height'][i]
            text_elements.append({
                'text': text,
                'box': (x, y, w, h)
            })

    return text_elements
