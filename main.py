
import os, sys

path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, path)

from src.chatbot import Chatbot


def main():
    chatbot = Chatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()