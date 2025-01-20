# src/llm.py
from langchain_ollama import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage
import logging

logger = logging.getLogger('QuantumChat.LLM')

class LLM:
    def __init__(self, settings):
        """Initialize LLM with settings from settings.json"""
        self.settings = settings
        self.message_history = []
        self.setup_llm()

    def setup_llm(self):
        """Initialize the LLM with settings"""
        try:
            self.llm = ChatOllama(
                model="qwen2.5:14b",  # Using Qwen 2.5 14B model
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                max_tokens=4096,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
                base_url="http://127.0.0.1:11434/v1"
            )
            logger.info("LLM initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise

    def generate_response(self, user_input):
        """Generate AI response for user input"""
        try:
            self.message_history.append(HumanMessage(content=user_input))
            
            # Keep conversation context manageable
            if len(self.message_history) > 16:
                self.message_history = self.message_history[-16:]
            
            response = self.llm.invoke(self.message_history)
            self.message_history.append(AIMessage(content=response.content))
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def clear_history(self):
        """Clear conversation history"""
        self.message_history = []