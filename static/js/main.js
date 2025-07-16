// --- Configuration for Flask Backend API ---
const FLASK_API_URL = 'http://127.0.0.1:5000/chat';

// Chat history to maintain context for the Gemini model
let chatHistory = [];

// --- 3D Background Animation Logic ---
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let w, h;

// Function to resize canvas on window resize
function resizeCanvas() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
    // Re-initialize sphere positions if needed, or just let them wrap
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas(); // Initial resize

// Generate floating 3D spheres
const spheres = [];
for (let i = 0; i < 30; i++) {
    spheres.push({
        x: Math.random() * w,
        y: Math.random() * h,
        z: Math.random() * 400 + 100, // Z-depth for perspective (100-500)
        r: Math.random() * 30 + 20, // Radius (20-50)
        dx: (Math.random() - 0.5) * 0.7, // X-direction speed (-0.35 to 0.35)
        dy: (Math.random() - 0.5) * 0.7, // Y-direction speed
        dz: (Math.random() - 0.5) * 0.3, // Z-direction speed
        color: `rgba(0,255,231,${Math.random() * 0.5 + 0.3})` // Cyan with varying opacity
    });
}

// Function to draw a single sphere with perspective
function drawSphere(s) {
    // Perspective projection calculation
    const scale = 200 / s.z; // Closer objects (smaller z) appear larger
    const x2d = s.x * scale + w / 2 - (w / 2) * scale;
    const y2d = s.y * scale + h / 2 - (h / 2) * scale;

    ctx.beginPath();
    ctx.arc(x2d, y2d, s.r * scale, 0, 2 * Math.PI);
    ctx.fillStyle = s.color;
    ctx.shadowColor = "#00ffe7"; // Cyan glow
    ctx.shadowBlur = 20 * scale; // Blur based on distance
    ctx.fill();
    ctx.shadowBlur = 0; // Reset shadow for next draw
}

// Animation loop for 3D background
function animateBackground() {
    ctx.clearRect(0, 0, w, h); // Clear canvas
    for (let s of spheres) {
        // Update sphere positions
        s.x += s.dx;
        s.y += s.dy;
        s.z += s.dz;

        // Wrap spheres around the screen or reverse direction
        if (s.x < -s.r * 2 || s.x > w + s.r * 2) s.dx *= -1;
        if (s.y < -s.r * 2 || s.y > h + s.r * 2) s.dy *= -1;
        if (s.z < 100 || s.z > 500) s.dz *= -1; // Keep Z within bounds

        drawSphere(s);
    }
    requestAnimationFrame(animateBackground); // Loop animation
}

// Start the background animation when the window loads
window.onload = animateBackground;

// --- Chatbot Logic ---
const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

// Function to append messages to the chat window
function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.innerHTML = `${text}`;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to bottom
}

// Function to display a loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot loading-message';
    loadingDiv.innerHTML = `<span>Tayyab's AI Assistant:</span> <span class="loading-dots"><div></div><div></div><div></div></span>`;
    chatWindow.appendChild(loadingDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    sendBtn.disabled = true; // Disable send button while loading
    chatInput.disabled = true; // Disable input while loading
}

// Function to remove the loading indicator
function hideLoading() {
    const loadingMessage = chatWindow.querySelector('.loading-message');
    if (loadingMessage) {
        loadingMessage.remove();
    }
    sendBtn.disabled = false; // Re-enable send button
    chatInput.disabled = false; // Re-enable input
    chatInput.focus(); // Focus input for next message
}

// Function to get response from Flask backend
async function getGeminiResponse(userText) {
    showLoading(); // Show loading dots
    try {
        const payload = {
            message: userText,
            history: chatHistory
        };

        const response = await fetch(FLASK_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`API error: ${response.status} - ${errorData.error || 'Unknown error'}`);
        }

        const result = await response.json();

        // Check if the response structure is as expected
        if (result.response) {
            const botResponseText = result.response;
            // Update chat history with the response from backend
            if (result.history) {
                chatHistory = result.history;
            }
            return botResponseText;
        } else {
            return "Sorry, I couldn't get a valid response from the AI.";
        }

    } catch (error) {
        console.error("Error calling Flask API:", error);
        return `Apologies, there was an issue connecting to the AI: ${error.message}. Please try again.`;
    } finally {
        hideLoading(); // Hide loading dots regardless of success or failure
    }
}

// Function to handle sending messages
async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return; // Don't send empty messages

    appendMessage('user', text); // Display user's message immediately
    chatInput.value = ''; // Clear input field

    // Get bot's reply from Gemini API
    const botResponse = await getGeminiResponse(text);
    appendMessage('bot', botResponse); // Display bot's response
}

// Event listeners for send button and Enter key
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initial welcome message from the bot
window.addEventListener('load', () => {
    appendMessage('bot', "Hello! I'm Tayyab's AI Assistant. How can I help you today?");
});
