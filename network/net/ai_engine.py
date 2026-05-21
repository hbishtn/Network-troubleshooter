import google.generativeai as genai

genai.configure(api_key="AIzaSyBfyBFOz4Hpine_SU3wRlR2GHEIljapsBc")

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_network_problem(problem, ping, dns, speed):

    prompt = f"""
    You are an expert network engineer.
    Explain in simple English.
    Keep answer short.
    Only important points.
    No long report format.
    Also make bold the important points.

     USER PROBLEM:
{problem}

    SYSTEM TEST RESULTS:
    Ping Result:
{ping}

    DNS Result:
{dns}

    Speed Test:
{speed}

    Now give:
    1. Root cause
    2. Exact fix
    3. Step by step solution
    4. Beginner explanation
    """

    response = model.generate_content(prompt)
    return response.text