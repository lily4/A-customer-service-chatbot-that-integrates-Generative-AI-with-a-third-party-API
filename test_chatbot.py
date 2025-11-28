from api_service import get_random_quote
from chatbot import handle_message

def test_quote_api():
    quote = get_random_quote("art")
    assert "content" in quote
    assert "author" in quote

def test_chatbot_reply():
    reply = handle_message("hello")
    assert isinstance(reply, str)
    assert len(reply) > 0
