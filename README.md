# 🌌 Quantum Chat AI

A beautifully designed desktop chat application that brings the power of local AI models to your fingertips with a stunning cyberpunk-inspired interface. Built for privacy-conscious users who want full control over their AI conversations.

## ✨ Features

### 🎨 **Stunning Visual Design**
- **Cyberpunk Aesthetic**: Rich purple gradients, neon accents, and futuristic UI elements
- **Custom SVG Icons**: Hand-crafted vector graphics for every interface element
- **Smooth Animations**: Polished interactions that feel responsive and alive
- **Rounded Corners & Modern Layout**: Contemporary design language throughout

### 🧠 **Powerful AI Integration**
- **Local LLM Support**: Full integration with Ollama for complete privacy
- **Multiple Model Support**: Optimized for Qwen2.5 14B, with support for other models
- **Advanced Parameters**: Fine-tune temperature, top-p, penalties, and token limits
- **Streaming Responses**: Real-time message generation with visual feedback

### 💬 **Advanced Chat Management**
- **Multi-Chat Interface**: Create and switch between unlimited conversations
- **Smart Organization**: Favorite chats get priority placement
- **Persistent Storage**: All conversations saved automatically in JSON format
- **Quick Actions**: Rename, delete, and favorite chats with intuitive controls

### ⚙️ **Comprehensive Settings**
- **Model Configuration**: Easy switching between available Ollama models
- **Parameter Tuning**: Slider-based controls for all model parameters
- **Memory Management**: Configurable conversation buffer and smart summarization
- **UI Customization**: Adjustable display preferences and themes

### 🔒 **Privacy First**
- **100% Local**: No data sent to external servers
- **Offline Capable**: Works entirely without internet connection
- **Your Models**: Use your own locally hosted models
- **Data Control**: All conversations stored locally on your machine

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** running locally with your preferred model

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gambadio/quantum_chat.git
   cd quantum_chat
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Ollama** (if not already done):
   ```bash
   # Install Ollama (visit https://ollama.ai for platform-specific instructions)
   
   # Pull the recommended model
   ollama pull qwen2.5:14b
   
   # Start Ollama server (if not running)
   ollama serve
   ```

4. **Launch Quantum Chat**:
   ```bash
   cd src
   python app.py
   ```

## 📁 Project Structure

```
quantum_chat/
├── src/                    # Core application code
│   ├── app.py             # Main application and GUI logic
│   ├── llm.py             # Ollama integration and LLM handling
│   ├── styles.py          # UI styling and theming system
│   ├── settings.py        # Configuration management
│   └── utils.py           # Utility functions and chat ordering
├── assets/                # Visual assets and icons
│   └── images/           # SVG icons and graphics
├── chats/                 # Stored conversation data (auto-created)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎯 Usage Guide

### Starting Your First Chat
1. **Launch the app** and you'll see the sleek sidebar interface
2. **Click "New Chat"** to create your first conversation
3. **Type your message** in the input field at the bottom
4. **Press Enter** or click "Send" to get your AI response

### Managing Your Conversations
- **⭐ Favorite**: Click the star icon to pin important chats to the top
- **✏️ Rename**: Click the edit icon to give your chat a meaningful name
- **🗑️ Delete**: Remove conversations you no longer need
- **🔄 Switch**: Click any chat in the sidebar to continue previous conversations

### Customizing Your Experience
1. **Open Settings** via the bottom button in the sidebar
2. **Configure Model**: Choose your preferred Ollama model
3. **Adjust Parameters**: Fine-tune response creativity and length
4. **Set Memory**: Control how much conversation history to maintain

## ⚙️ Configuration

### Model Settings
- **Temperature** (0.0-1.0): Controls response creativity and randomness
- **Max Tokens** (100-4000): Maximum length of AI responses
- **Top P** (0.0-1.0): Nucleus sampling parameter for coherence
- **Frequency Penalty** (0.0-2.0): Reduces repetitive phrases
- **Presence Penalty** (0.0-2.0): Encourages topic diversity

### Memory Management
- **Buffer Size**: Number of message pairs to keep in active memory
- **Summary Mode**: Automatic conversation summarization for long chats
- **Summary Interval**: How often to create memory summaries

### Supported Models
The application works with any Ollama-compatible model, with optimized presets for:
- `qwen2.5:14b` (Recommended - Best balance of quality and speed)
- `qwen1.5:14b` (Alternative high-quality option)
- `qwen1.5:7b` (Faster option for lower-end hardware)
- `qwen1.5:4b` (Lightweight option)

## 🛠️ Technical Architecture

### Core Components

**Main Application (`app.py`)**
- Tkinter-based GUI with custom theming
- Multi-threaded message processing
- Real-time chat interface with message bubbles
- Comprehensive settings management

**LLM Integration (`llm.py`)**
- Langchain integration with Ollama
- Conversation memory management
- Streaming response handling
- Error recovery and fallback

**Styling System (`styles.py`)**
- Cyberpunk color palette
- SVG icon loading and caching
- Custom widget styling
- Responsive layout components

**Settings Management (`settings.py`)**
- JSON-based configuration storage
- Automatic backup and versioning
- Validation and migration support
- Default value management

### Dependencies
- **langchain-community**: LLM integration framework
- **langchain-core**: Core langchain functionality
- **Pillow**: Image processing for UI elements
- **cairosvg**: SVG rendering and icon support

## 🎨 Customization

### Themes and Colors
The app features a carefully crafted cyberpunk color scheme defined in `styles.py`. Key colors include:
- **Background**: Deep space blues (`#1A1B3E`, `#202052`)
- **Accents**: Vibrant neons (`#B4A5FF`, `#FF9ECD`, `#94FBFF`)
- **Messages**: Distinct colors for user (`#FF61EF`) and AI (`#2D2E8F`)

### Adding Custom Models
1. Pull your model with Ollama: `ollama pull your-model:tag`
2. Add the model name to the dropdown in the settings interface
3. Adjust parameters as needed for optimal performance

### Icon Customization
Replace SVG files in `assets/images/` to customize the interface:
- `logo.svg`: Main application logo
- `user_avatar.svg`: User message avatar
- `robot_avatar.svg`: AI message avatar
- Various UI icons for actions and controls

## 🐛 Troubleshooting

### Common Issues

**"Connection refused" errors**
- Ensure Ollama is running: `ollama serve`
- Check the API URL in settings (default: `http://localhost:11434/v1`)
- Verify your model is pulled: `ollama list`

**UI elements not loading**
- Check that SVG files exist in `assets/images/`
- Ensure cairosvg is properly installed
- Try running with Python in verbose mode to see detailed errors

**Slow responses**
- Consider using a smaller model (7B or 4B parameter versions)
- Reduce max_tokens in settings
- Ensure sufficient system RAM for your chosen model

**Chat data not persisting**
- Check write permissions in the `chats/` directory
- Verify JSON files aren't corrupted
- Look for error messages in the console output

## 🤝 Contributing

Quantum Chat is designed to be extensible and welcomes contributions! Areas for enhancement:

- **Additional LLM Providers**: Support for other local and remote APIs
- **Plugin System**: Extensible architecture for custom features
- **Advanced Theming**: User-customizable color schemes and layouts
- **Export Features**: Chat export to various formats
- **Voice Integration**: Text-to-speech and speech-to-text capabilities

## 📄 License

This project is open source. Please check the repository for specific license terms.

## 🌟 Acknowledgments

- **Ollama Team**: For making local AI accessible and easy to use
- **Langchain**: For the powerful AI integration framework
- **Python Community**: For the incredible ecosystem of tools and libraries

---

*Built with ❤️ for the privacy-conscious AI enthusiasts who believe in local-first applications.*