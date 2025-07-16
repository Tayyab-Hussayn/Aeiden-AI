# Project Structure

```
tayyab-ai-chatbot/
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

## File Descriptions

### Core Files
- **app.py**: Main Flask application with API routes and server configuration
- **config.py**: Configuration management with environment-specific settings
- **requirements.txt**: Python package dependencies

### Frontend Assets
- **templates/index.html**: Main HTML template using Jinja2 templating
- **static/css/style.css**: Complete CSS styling for the chatbot interface
- **static/js/main.js**: JavaScript for chatbot functionality and 3D animations

### Configuration
- **.env.example**: Template for environment variables
- **.gitignore**: Git ignore patterns to exclude sensitive files

### Documentation
- **README.md**: Main project documentation
- **docs/PROJECT_STRUCTURE.md**: This file - project structure documentation

## Technology Stack

### Backend
- **Python 3.7+**: Core programming language
- **Flask**: Web framework
- **Google Generative AI**: Gemini API integration
- **Flask-CORS**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5**: Markup structure
- **CSS3**: Styling with animations and responsive design
- **JavaScript (ES6+)**: Interactive functionality
- **Canvas API**: 3D background animations
- **Fetch API**: HTTP requests to backend

### Development Tools
- **Git**: Version control
- **GitHub**: Remote repository hosting
- **Virtual Environment**: Python dependency isolation

## Key Features

1. **Responsive Design**: Works on desktop and mobile devices
2. **3D Animations**: Floating sphere background animation
3. **Real-time Chat**: Interactive chat interface
4. **AI Integration**: Powered by Google's Gemini AI
5. **Secure Configuration**: Environment-based API key management
6. **Professional Structure**: Organized codebase with separation of concerns
