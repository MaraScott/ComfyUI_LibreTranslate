import torch
from io import BytesIO
import numpy as np
import requests

names = ['English','Albanian','Arabic','Azerbaijani','Bengali','Bulgarian','Catalan','Chinese','Chinese (traditional)',
        'Czech','Danish','Dutch','Esperanto','Estonian','Finnish','French','German','Greek','Hindi','Hungarian','Indonesian',
        'Irish','Italian','Japanese','Korean','Latvian','Lithuanian','Malay','Norwegian','Persian','Polish','Portuguese','Romanian',
        'Russian','Slovak','Slovenian','Spanish','Swedish','Tagalog','Thai','Turkish','Ukranian','Urdu']

codes = ['en', 'sq', 'ar', 'az', 'bn', 'bg', 'ca', 'zh', 'zt', 'cs', 'da', 'nl', 'eo', 'et', 'fi', 'fr', 'de', 'el', 'hi', 'hu', 'id', 'ga', 'it',
         'ja', 'ko', 'lv', 'lt', 'ms', 'nb', 'fa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'es', 'sv', 'tl', 'th', 'tr', 'uk', 'ur']
 
# Mapping language names to codes
name_to_code = dict(zip(names, codes)) 

# Helper function to translate text
def translate_text(text, source_code, target_code):
    url = "http://127.0.0.1:5000/translate"
    data = {
        "q": text,
        "source": source_code,  # Use language code
        "target": target_code,  # Use language code
        "format": "text",
		"alternatives": 3,
		"api_key": ""
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Check if the response status is not an error
        translated_text = response.json().get('translatedText')
        return translated_text
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the translation server. Is the server running?"
    except requests.exceptions.Timeout:
        return "Error: The request to the translation server timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: An error occurred while trying to connect to the translation server: {e}"



# Define LibreTranslate class
class LibreTranslate:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Hello", "multiline": True}),
                "source": (names, ),
                "target": (names, ),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Translation"

    def execute(self, text, source, target):
        # Convert names to codes using the mapping
        source_code = name_to_code.get(source)
        target_code = name_to_code.get(target)
        if source_code and target_code:
            translated_text = translate_text(text, source_code, target_code)
        else:
            translated_text = "Error: Invalid language selection."
        return (translated_text,)

# Define node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "LibreTranslate": LibreTranslate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LibreTranslate": "Libre Translate",
}
