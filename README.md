# 🧠 FableForge AI - Story Engine

> **Transform your imagination into captivating stories with the power of AI**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.0-FF6B6B.svg)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-4285F4.svg)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg)](https://python.org)

An AI-powered storytelling platform. The user interface is Streamlit, not Gradio. Chat, stories, and the writing assistant call Google's Gemini models. Comic video generation does not run in this app: it calls the external Hugging Face Space [`ADOPLE/Video-Generator-AI`](https://huggingface.co/spaces/ADOPLE/Video-Generator-AI) and shows the video that Space returns. The `gradio_client` package is only the client for that Space.
![FableForge AI Architecture](FableForge-Architecture.png)
## ✨ Features

- 🤖 **AI ChatBot** - Intelligent conversations with streaming responses
- 📚 **Story Generator** - Create stories from images or text prompts  
- 🎬 **Comic Video Generator** - Send a script to an external Hugging Face Space and play the video it returns
- 🎯 **AI Assistant** - Writing help, grammar check, translation
- 🎨 **Creative Writing** - Poems, lyrics, character descriptions

## 🚀 Quick Setup with install.py

The easiest way to get started is using our automated installation script:

### **Option 1: Automated Installation**

1. **Download and run the installer**
   ```bash
   python install.py
   ```

The installer will automatically:
- ✅ Check Python version compatibility (3.9+)
- 📦 Install all required packages
- ⚙️ Create `.env` file template
- 🔑 Guide you through API key setup
- 🧪 Test the installation
- 🚀 Launch the application

### **What install.py does:**

- **Python Version Check**: Ensures you have Python 3.9 or higher
- **Package Installation**: Installs all dependencies from requirements.txt
- **Environment Setup**: Creates `.env` file with proper template
- **API Key Configuration**: Guides you to set up required API keys
- **Installation Testing**: Verifies all packages work correctly
- **Application Launch**: Optionally starts the Streamlit app

## 🛠 Manual Installation

### **Prerequisites**
- Python 3.9 or higher
- Google API Key ([Get one here](https://aistudio.google.com/app/apikey))
- Hugging Face Token ([Get one here](https://huggingface.co/settings/tokens))

### **Steps**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohit6304/FableForgeAI-StoryEngine.git
   cd FableForgeAI-StoryEngine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_google_api_key_here
   HUGGINGFACE_API_KEY=your_hugging_face_token_here
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 How to Use

### **ChatBot**
- Start conversations with AI
- Toggle streaming mode for real-time responses
- Save chat history
- Adjust temperature and token settings

### **Story Generator**
- **Image Stories**: Upload an image and add text prompts
- **Text Stories**: Describe your story idea in detail
- **Creative Writing**: Generate poems, lyrics, character descriptions
- Choose genre, length, and tone
- Generate audio narration

### **Comic Video Generator**
- Write your story script
- Optionally preview a Gemini rewrite of that script (uses the sidebar model, temperature, and max tokens)
- Generate the video. The script is sent to the external Hugging Face Space `ADOPLE/Video-Generator-AI`
- Download the video that Space returns

This page sends only the script. It does not offer comic style, duration, character, or audio controls, because those values are not passed to the Space.

### **AI Assistant**
- **Writing Help**: Improve text, check grammar
- **Translation**: Multi-language support
- **Tone Change**: Adjust writing style
- **Research**: Get information and analysis

## ⚙️ Configuration

### **Model Settings**
- Choose from multiple Gemini models. The selection is sent with each Gemini request
- Temperature (0.0–1.0) and max tokens (100–2048) are sent as Gemini `temperature` and `max_output_tokens`

### **Audio Settings**
- Optional text-to-speech for generated stories
- Uses the Hugging Face inference API (`facebook/mms-tts-eng`) and requires `HUGGINGFACE_API_KEY`
- One English voice; there is no voice picker

## 📋 Requirements

```
streamlit>=1.45.0
google-generativeai>=0.8.5
python-dotenv>=1.0.1
Pillow>=10.3.0
requests>=2.32.3
gradio-client>=1.3.0
numpy>=1.26.4
```

## 🔧 Environment Variables

Your `.env` file should contain:

```env
# Google Gemini API Key. GEMINI_API_KEY is preferred.
# If it is unset, the app reads GOOGLE_API_KEY instead.
GEMINI_API_KEY=your_api_key_here

# Hugging Face API Key (for story audio)
HUGGINGFACE_API_KEY=your_token_here
```

## Troubleshooting

**API Key Issues:**
- Verify your `.env` file exists and contains valid keys
- Check API key permissions and quotas

**Installation Problems:**
- Use `python install.py` for automated setup
- Ensure Python 3.9+ is installed
- Try creating a virtual environment

**Import Errors:**
- Run `pip install -r requirements.txt` again
- Check Python path and virtual environment



