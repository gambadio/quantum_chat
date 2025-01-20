from langchain_ollama import ChatOllama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage
import logging

logger = logging.getLogger('QuantumChat.LLM')

class LLM:
    def __init__(self, settings):
        self.settings = settings
        self.message_history = []
        self.setup_llm()

    def setup_llm(self):
        try:
            self.llm = ChatOllama(
                model="qwen2.5:14b",
                temperature=0.7,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
                base_url="http://127.0.0.1:11434"  # Removed /v1 from URL
            )
            logger.info("LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise

    def generate_response(self, user_input):
        try:
            self.message_history.append(HumanMessage(content=user_input))
            if len(self.message_history) > 16:
                self.message_history = self.message_history[-16:]
            
            response = self.llm.invoke(self.message_history)
            self.message_history.append(AIMessage(content=response.content))
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"  # Return error message instead of raising

    def clear_history(self):
        self.message_history = []