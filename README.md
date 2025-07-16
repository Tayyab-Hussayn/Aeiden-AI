# Tayyab's AI Chatbot

This project is a web-based AI chatbot powered by Gemini AI, featuring a futuristic 3D background animation.

## Features

- Interactive chat interface
- 3D animated background
- Powered by the advanced Gemini AI

## Setup and Configuration

### Prerequisites

- Python 3.7+
- Virtualenv

### Getting Started

1. **Clone the repository:**

    ```sh
    git clone <REPO_URL>
    cd terminal-genai
    ```

2. **Set up a virtual environment:**

    ```sh
    virtualenv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Configuration:**
   
    Copy the example environment file and set up your configuration.

    ```sh
    cp .env.example .env
    ```
    
    Edit `.env` to configure your API key and Flask settings:
    
    ```
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    FLASK_DEBUG=True
    FLASK_HOST=127.0.0.1
    FLASK_PORT=5000
    ```

5. **Run the application:**

    ```sh
    python app.py
    ```

6. **Access the chatbot webpage:**

    Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## Contribution

For contributions, please fork the repository and use a feature branch. Pull requests are welcomed.

## License

This project is licensed under the MIT License.

---

Thank you for using Tayyab's AI Chatbot. Enjoy your chatting experience!
