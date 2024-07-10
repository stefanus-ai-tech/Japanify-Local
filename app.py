from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Google Generative AI with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the model and generation config
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Add this line to enable CORS

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/convert-name', methods=['POST'])

def convert_name():
    data = request.get_json()
    print("Received data:", data)  # Debug print
    name = data.get('name')
    print("Received name:", name)  # Debug print

    if not name:
        return jsonify({"error": "Name is required"}), 400

    instructions = f"""
    **Task Description:**
    Given an Indonesian name, follow these steps:
    
    1. **Determine the Meaning:** Research and determine the meaning of the given Indonesian name, considering its etymology and cultural context.
    2. **Translate into Japanese:** Translate the identified meaning of the name into Japanese.
    3. **Japanese Translation:** Provide the Japanese translation in appropriate kanji, hiragana, or katakana.
    4. **Create a New Name:** Combine elements from the original Indonesian name, its meaning, and the Japanese translation to create a new, meaningful name.
    5. **Export Results:** Structure the results in the specified JSON format.

    **Input Name:** {name}

    **Output JSON Format:**
    ```json
    {{
      "original_name": "{name}",
      "name_meaning": "",
      "japanese_translation": "",
      "final_name": {{
        "romaji": "",
        "kanji": "",
        "hiragana": "",
        "meaning in english":""
      }}
    }}
    ```

    **Detailed Instructions:**

    1. **Determine the Meaning:**
        - Break down the name into its components.
        - Research the meaning of each component, focusing on Indonesian cultural and linguistic origins.
        - Provide a concise meaning for the full name.

    2. **Translate into Japanese:**
        - Translate the meaning derived from the previous step into Japanese.
        - Ensure the translation captures the essence and cultural context of the original meaning.

    3. **Japanese Translation:**
        - Choose the appropriate Japanese writing system (kanji, hiragana, or katakana) for the translation.
        - Provide the Japanese translation in the chosen writing system.

    4. **Create a New Name:**
        - Combine elements from the original name, its meaning, and the Japanese translation.
        - Form a new name that is meaningful and culturally coherent.
        - Present the new name in three forms: romaji, kanji, and hiragana.

    5. **Export Results:**
        - Format the results in the provided JSON structure.
        - Ensure each field is accurately filled out based on your research and translations.

    **Now, please process the input name and provide the results in the specified JSON format.** DON'T GENERATE ANYTHING BESIDE THE JSON
    """

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [instructions],
            },
        ],
    )

    try:
        response = chat_session.send_message("Please provide the translated name as per the above instructions.")
        print("API Response:", response)  # Log the full response for debugging
        result = response.text

        # Check for safety warnings
        warnings = []
        if hasattr(response, 'safety_ratings'):
            for rating in response.safety_ratings:
                if rating.probability == "HIGH":
                    warnings.append(f"Warning: High probability of {rating.category.replace('HARM_CATEGORY_', '').replace('_', ' ').lower()}")

        return jsonify({"result": result, "warnings": warnings})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error processing the name"}), 500

if __name__ == '__main__':
    app.run(port=int(os.getenv("PORT", 3000)), debug=True)
