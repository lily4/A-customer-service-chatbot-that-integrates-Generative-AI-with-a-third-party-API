from api_service import get_random_quote
from gemini_client import enhance_message

STORE_NAME = "Aurora Art & Craft"
INSTAGRAM_HANDLE = "@aurora.art.craft"  # fictional handle


def handle_message(message: str) -> str:
    msg = message.lower().strip()

    # greetings
    if msg in {"hi", "hello", "hey", "hola"}:
        base_reply = (
            f"Hello! I'm the virtual assistant for {STORE_NAME}.\n"
            "You can ask me about products, workshops, returns, shipping, or opening hours. "
            "You can also say 'inspire me' for a creativity quote."
        )
        return enhance_message(base_reply, "warm, welcoming customer service tone")

    # products / supplies
    if "what do you sell" in msg or "products" in msg or "supplies" in msg:
        base_reply = (
            f"{STORE_NAME} specializes in paper crafts and mixed-media art supplies.\n"
            "- Premium origami and craft paper\n"
            "- Watercolor paper, brushes, and paints\n"
            "- Craft tools like cutters, glue, and cutting mats\n"
            "- DIY kits that are great for beginners\n"
            "If you tell me what kind of project you’re working on, I can suggest materials."
        )
        return enhance_message(base_reply, "helpful, informative and encouraging")

    # workshops / classes
    if "workshop" in msg or "class" in msg or "classes" in msg:
        base_reply = (
            "We regularly host small-group workshops such as:\n"
            "- Origami for beginners\n"
            "- Watercolor basics\n"
            "- Creative journaling sessions\n\n"
            f"Upcoming dates and sign-up details are shared on our Instagram stories ({INSTAGRAM_HANDLE})."
        )
        return enhance_message(base_reply, "enthusiastic and inviting")

    # opening hours
    if "hours" in msg or "open" in msg or "time" in msg:
        base_reply = (
            f"{STORE_NAME} is open from Tuesday to Saturday, 10:00 AM to 6:00 PM (local time).\n"
            "For online questions sent by Instagram DM, we usually reply within about 24 hours."
        )
        return enhance_message(base_reply, "clear and concise")

    # returns / refund policy
    if "return" in msg or "refund" in msg or "exchange" in msg:
        base_reply = (
            "We accept returns or exchanges on unused, unopened items within 14 days of purchase "
            "with a receipt. Custom-made pieces and digital downloads are non-refundable.\n"
            "If you have a specific issue with an order, please contact us with your order details "
            "so we can review it."
        )
        return enhance_message(base_reply, "reassuring and professional")

    # shipping / pickup
    if "shipping" in msg or "delivery" in msg or "pickup" in msg:
        base_reply = (
            f"{STORE_NAME} offers local pickup and standard shipping.\n"
            "Most orders arrive within 5–7 business days, depending on your location. "
            "Exact timing and costs are confirmed when you place your order."
        )
        return enhance_message(base_reply, "informative and friendly")

    # contact / human agent
    if "contact" in msg or "talk to a person" in msg or "human" in msg:
        base_reply = (
            f"If you’d like to talk to a person, you can send us a DM on Instagram ({INSTAGRAM_HANDLE}) "
            "or email us at support@aurora-art-craft.example. "
            "We usually respond within one business day."
        )
        return enhance_message(base_reply, "supportive and polite")

    # inspiration / quote
    if "inspire" in msg or "quote" in msg or "motivate" in msg or "creative block" in msg:
        try:
            quote = get_random_quote(tag="inspirational|art|creativity")
            text = quote.get("content", "")
            author = quote.get("author", "Unknown")

            base_reply = (
                "Here’s a little creative inspiration for you:\n\n"
                f"“{text}”\n— {author}"
            )
            return enhance_message(base_reply, "gentle, encouraging, creative tone")
        except Exception as e:
            # In case the API fails, we still want a nice message
            base_reply = (
                "I’m having trouble fetching a quote right now, but please remember: "
                "your creativity matters, and even small steps count."
            )
            return enhance_message(base_reply, "kind and encouraging")

    # default help
    base_reply = (
        f"Thanks for reaching out to {STORE_NAME}.\n"
        "You can ask me about:\n"
        "- What we sell (art supplies, paper, DIY kits)\n"
        "- Workshops and classes\n"
        "- Returns and exchanges\n"
        "- Shipping or pickup options\n"
        "Or you can say 'inspire me' to get a creativity quote."
    )
    return enhance_message(base_reply, "friendly customer service tone")
