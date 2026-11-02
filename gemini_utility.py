import os
import time
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# README and the Streamlit app use GEMINI_API_KEY. GOOGLE_API_KEY remains a fallback.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
DEFAULT_MODEL = "gemini-2.0-flash"
FALLBACK_MODEL = "gemini-1.5-flash"

# Configure Google.generativeai with API key
genai.configure(api_key=GEMINI_API_KEY)

def build_generation_config(temperature=None, max_output_tokens=None):
    """Map UI settings onto Gemini generation parameters.

    Returns None when both values are omitted so the SDK keeps its defaults.
    A temperature of 0.0 is a real setting and must be forwarded.
    """
    config = {}
    if temperature is not None:
        config["temperature"] = float(temperature)
    if max_output_tokens is not None:
        config["max_output_tokens"] = int(max_output_tokens)
    return config or None

def _generation_kwargs(temperature=None, max_output_tokens=None, stream=False):
    kwargs = {}
    config = build_generation_config(temperature, max_output_tokens)
    if config:
        kwargs["generation_config"] = config
    if stream:
        kwargs["stream"] = True
    return kwargs

def load_gemini_pro_model(model_name=DEFAULT_MODEL):
    """Load a Gemini model for text generation."""
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"Warning: Could not load {model_name}, falling back to {FALLBACK_MODEL}. Error: {e}")
        return genai.GenerativeModel(FALLBACK_MODEL)

def load_gemini_pro_vision_model(model_name=DEFAULT_MODEL):
    """Load a Gemini model for image and text prompts."""
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"Warning: Could not load {model_name} for vision, falling back to {FALLBACK_MODEL}. Error: {e}")
        return genai.GenerativeModel(FALLBACK_MODEL)

def gemini_pro_vision_response(prompt, image, temperature=None, max_output_tokens=None, model_name=DEFAULT_MODEL):
    """Get response from Gemini Vision model - image/text to text"""
    try:
        gemini_pro_vision_model = load_gemini_pro_vision_model(model_name)
        response = gemini_pro_vision_model.generate_content(
            [prompt, image],
            **_generation_kwargs(temperature, max_output_tokens),
        )
        result = response.text
        return result
    except Exception as e:
        return f"Error generating vision response: {str(e)}"

def embeddings_model_response(input_text):
    """Get response from embeddings model - text to embeddings"""
    try:
        # Use the latest embedding model
        embedding_model = "models/text-embedding-004"
        embedding = genai.embed_content(
            model=embedding_model,
            content=input_text,
            task_type="retrieval_document"
        )
        embedding_list = embedding["embedding"]
        return embedding_list
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Fallback to older model
        try:
            embedding_model = "models/embedding-001"
            embedding = genai.embed_content(
                model=embedding_model,
                content=input_text,
                task_type="retrieval_document"
            )
            embedding_list = embedding["embedding"]
            return embedding_list
        except Exception as fallback_e:
            return f"Error generating embeddings: {str(fallback_e)}"

def gemini_pro_response(user_prompt, temperature=None, max_output_tokens=None, model_name=DEFAULT_MODEL):
    """Get response from Gemini model - text to text"""
    try:
        gemini_pro_model = load_gemini_pro_model(model_name)
        response = gemini_pro_model.generate_content(
            user_prompt,
            **_generation_kwargs(temperature, max_output_tokens),
        )
        result = response.text
        return result
    except Exception as e:
        return f"Error generating response: {str(e)}"

def gemini_stream_response(user_prompt, temperature=None, max_output_tokens=None, model_name=DEFAULT_MODEL):
    """Get streaming response from Gemini model"""
    try:
        gemini_pro_model = load_gemini_pro_model(model_name)
        response = gemini_pro_model.generate_content(
            user_prompt,
            **_generation_kwargs(temperature, max_output_tokens, stream=True),
        )
        return response
    except Exception as e:
        return f"Error generating streaming response: {str(e)}"

def get_available_models():
    """Get list of available Gemini models"""
    try:
        models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                models.append(model.name)
        return models
    except Exception as e:
        print(f"Error fetching models: {e}")
        return ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

def check_api_key():
    """Check if API key is valid"""
    try:
        models = list(genai.list_models())
        return True
    except Exception as e:
        print(f"API key validation failed: {e}")
        return False
