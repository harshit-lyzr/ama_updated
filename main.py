from app import extract_video_id, generate_youtube_url, get_transcript
from gptcall import gpt_calll, gemini_call
import streamlit as st


response = {
    "answer": """
    Early-stage startups often grapple with several key challenges:
Product-Market Fit: Finding and refining a product that resonates with a significant market need.
Capital: Securing enough funding to grow while avoiding over-capitalization that can lead to misaligned spending.
Talent Acquisition: Attracting and retaining top talent, especially when competing with established companies.
Customer Acquisition: Efficiently acquiring customers and scaling the user base without unsustainable costs.
Market Understanding: Fully comprehending the competitive landscape and differentiating from similar offerings.
Operational Scaling: Building the infrastructure and processes to scale without losing quality or control.
Founder Dynamics: Ensuring alignment among founders on vision, equity, roles, and the direction of the company.
""",
    "links": [
        "https://www.youtube.com/watch?v=gZ6N-jD3jmw",
        "https://www.youtube.com/watch?v=KzLVx7MLYA0",
        "https://www.youtube.com/watch?v=jYZPvrJBUn0"
]
}


def final_response(url, responses):
    transcript = get_transcript(url)
    get_start_time_context = gemini_call(transcript, responses)
    get_start_time_in_json_mode = gpt_calll(get_start_time_context)
    yt_link = generate_youtube_url(url, get_start_time_in_json_mode)
    return yt_link


st.markdown(response["answer"])

yt_links = []
for link in response["links"]:
    final_link = final_response(extract_video_id(link), response["answer"])
    yt_links.append(final_link)

for link in yt_links:
    st.markdown(link)
