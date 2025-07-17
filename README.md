# 🤖 Aeiden AI

A modern, interactive AI chatbot web application powered by Google's Gemini AI, featuring a stunning 3D animated background and responsive design.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow)
![CSS3](https://img.shields.io/badge/CSS3-Animations-orange)
![HTML5](https://img.shields.io/badge/HTML5-Semantic-red)

## ✨ Features

- 🎨 **Modern UI/UX**: Futuristic glassmorphism design with 3D animations
- 🤖 **AI-Powered**: Integrated with Google's advanced Gemini AI model
- 📱 **Responsive**: Works seamlessly on desktop and mobile devices
- 🌐 **Real-time Chat**: Interactive chat interface with typing indicators
- 🔒 **Secure**: Environment-based API key management
- 🎭 **3D Background**: Floating sphere animations with perspective projection
- ⚡ **Fast & Lightweight**: Optimized for performance

## 🚀 Live Demo

Visit the [live demo](https://github.com/Tayyab-Hussayn/tayyab-ai-chatbot) to see the chatbot in action!

## 🛠️ Technology Stack

### Backend
- **Python 3.7+** - Core programming language
- **Flask** - Web framework
- **Google Generative AI** - Gemini API integration
- **Flask-CORS** - Cross-origin resource sharing
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Advanced styling with animations
- **JavaScript (ES6+)** - Interactive functionality
- **Canvas API** - 3D background animations
- **Fetch API** - HTTP requests to backend

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Google Gemini API key

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Tayyab-Hussayn/tayyab-ai-chatbot.git
cd tayyab-ai-chatbot
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env
```

Edit the `.env` file and add your configuration:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=1000

# Flask Configuration
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here

# Environment
FLASK_ENV=development
```

### 5. Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new project or select an existing one
3. Generate an API key
4. Replace `your_actual_gemini_api_key_here` in your `.env` file

### 6. Run the Application

```bash
python app.py
```

### 7. Access the Chatbot

Open your web browser and visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📁 Project Structure

```
Aeiden AI/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore patterns
├── README.md             # Project documentation
├── docs/
│   └── PROJECT_STRUCTURE.md
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # Main JavaScript file
│   └── images/           # Static images
├── templates/
│   └── index.html        # Main HTML template
└── utils/                # Utility functions
```

## 🎯 Usage

1. **Start a Conversation**: Type your message in the input field
2. **Send Messages**: Click the "Send" button or press Enter
3. **View Responses**: The AI will respond in real-time
4. **Enjoy the Experience**: Watch the 3D background animation while chatting

## 🔒 Security

- API keys are stored in environment variables
- No sensitive data is committed to the repository
- CORS is properly configured for security
- Input validation and error handling implemented

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google for the Gemini AI API
- Flask community for the excellent framework
- Inter font family for typography
- All contributors and users

## 📧 Contact

Tayyab Hussayn - [GitHub Profile](https://github.com/Tayyab-Hussayn)

Tayyab Hussayn - [Linkedin Profile](https://linkedin/in/tayyabhussayn)

Project Link: [https://github.com/Tayyab-Hussayn/tayyab-ai-chatbot](https://github.com/Tayyab-Hussayn/tayyab-ai-chatbot)

---

⭐ **If you found this project helpful, please give it a star!** ⭐
