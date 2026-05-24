from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_network_problem(

    problem,

    issue,

    rating,

    recommendation,

    fix
): 

    prompt = f"""

    You are a professional network engineer.

    USER QUESTION:
    {problem}

    DETECTED ISSUE:
    {issue}

    NETWORK RATING:
    {rating}/10

    RECOMMENDATION:
    {recommendation}

    AUTO FIX:
    {fix}

    Give clean professional answer.

    Use:
    - proper headings
    - bullet points
    - short explanations
    - readable spacing

    Keep answer smart and structured.
    """

    try:

        chat = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            chat.choices[0]
            .message.content
        )

    except Exception as e:

        return f"AI Error: {str(e)}"