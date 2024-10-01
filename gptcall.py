import os
from openai import OpenAI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API"))
genai.configure(api_key=os.getenv("GEMINI_API"))

class YTResponse(BaseModel):
    start_time: str


def gemini_call(context, query):
    prompt = """
    **Role**: Expert in video transcription analysis.

    **Task**: Identify the most relevant transcript chunk matching a user query.

    **Context**: You have a YouTube transcript divided into chunks, each with text, start time, and duration.

    **Instructions**:

    1. **Read** the user's response carefully.
    2. **Evaluate** each chunk for:
       - **Direct relevance** to the response.
       - **Key ideas or main topics** related to the query.
       - **Importance** in the video's overall flow.
    3. **Select** the chunk that best matches the query.
       - If multiple chunks are relevant, choose the one with the most critical information.
    4. **Return** the chunk's text and **indicate its start time**.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""{context} give start_time in second.millisecond format. e.g. 100.45 {prompt} response: {query}""",
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
        )
    )

    print(response.text)
    return response.text

def gpt_calll(context):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": f"""extracct start time from given context. and make it in seconds.millisecond format.(e.g. 102.87)"""},
            {"role": "user", "content": f"""
            {context}
            """}
        ],
        response_format=YTResponse,
        temperature=0.2
    )
    print(response.choices[0].message.parsed.start_time)
    return response.choices[0].message.parsed.start_time


