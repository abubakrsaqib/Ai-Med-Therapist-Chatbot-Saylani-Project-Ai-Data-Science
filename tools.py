# TOOLS
# Setup Ollama with Medgemma tool

import ollama

def query_medgemma(prompt: str) -> str:
    """
    Calls MedGemma model with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """

    system_prompt = """
    You are Dr. Wasim Akram, a warm and experienced clinical psychologist.

    Respond to patients with:
    1. Emotional attunement
    2. Gentle normalization
    3. Practical guidance
    4. Strengths-focused support

    Key Principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Use natural transitions
    - Mirror the user's language level
    - Keep the conversation going with open-ended questions
    """

    try:
        response = ollama.chat(
            model="gemma4:latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                "num_predict": 350,
                "temperature": 0.7,
                "top_p": 0.9
            }
        )

        return response["message"]["content"].strip()

    except Exception as e:
        print("MedGemma Error:", e)
        return (
            "I'm having technical difficulties right now. "
            "Please try again in a moment."
        )


print(query_medgemma("What is your name?"))


# Setup Twilio Calling API Tool

from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SSID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    EMERGENCY_CONTACT
)

def call_emergency(user_number: str):
    client = Client(
        TWILIO_ACCOUNT_SSID,
        TWILIO_AUTH_TOKEN
    )

    call = client.calls.create(
        to=user_number,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"
    )

    return call.sid