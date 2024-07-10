# Japanify

Japanify is a web application that converts Indonesian names into meaningful Japanese names, providing translations in kanji, hiragana, and romaji, along with their meanings in English.

## Features

- Converts Indonesian names to Japanese names.
- Provides translations in kanji, hiragana, and romaji.
- Displays the meaning of the name in English.
- Plays the pronunciation of the Japanese name using an audio feature.

## Technology Stack

- Flask
- HTML
- CSS
- JavaScript
- Google Generative AI
- Axios

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/stefanus-ai-tech/Japanify-Local
   cd Japanify-Local
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Google Generative AI API key and desired port:
   ```env
   GEMINI_API_KEY=your_google_generative_ai_api_key
   PORT=3000
   ```

5. Run the Flask app:
   ```bash
   python app.py
   ```

6. Open your browser and go to `http://127.0.0.1:3000` to see the application.

## File Structure

```plaintext
japanify/
├── static/
│   ├── styles2.css
│   ├── script2.js
│   └── index.html
├── app.py
├── requirements.txt
└── .env
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
