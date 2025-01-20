from langchain_community.chat_models import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage
import logging

logger = logging.getLogger('QuantumChat.LLM')

class LLM:
    def __init__(self, settings):
        self.settings = settings
        self.setup_llm()
        self.message_history = []

    def setup_llm(self):
        """Initialize the LLM with current settings"""
        try:
            model_settings = self.settings['model_settings']
            
            # Configure callback manager for streaming
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            
            self.llm = ChatOllama(
                model=model_settings['model'],
                temperature=model_settings['temperature'],
                top_p=model_settings['top_p'],
                frequency_penalty=model_settings.get('frequency_penalty', 0.0),
                presence_penalty=model_settings.get('presence_penalty', 0.0),
                max_tokens=model_settings['max_tokens'],
                callback_manager=callback_manager,
                base_url="http://localhost:11434/v1"
            )
            
            logger.info(f"LLM initialized with model: {model_settings['model']}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise Exception(f"LLM initialization failed: {str(e)}")

    def update_settings(self, settings):
        """Update LLM settings and reinitialize"""
        self.settings = settings
        self.setup_llm()

    def generate_response(self, user_input):
        """Generate AI response for user input"""
        try:
            # Add user message to history
            self.message_history.append(HumanMessage(content=user_input))
            
            # Keep only last 8 messages for context
            if len(self.message_history) > 16:
                self.message_history = self.message_history[-16:]
            
            # Generate response
            response = self.llm.invoke(self.message_history)
            
            # Add AI response to history
            self.message_history.append(AIMessage(content=response.content))
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")

    def clear_history(self):
        """Clear conversation history"""
        self.message_history = []