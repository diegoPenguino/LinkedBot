import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def extract_post_details(raw_text: str) -> dict:
    """
    Extracts a title and a summary from the user's raw text.
    Returns a dict with 'title' and 'summary'.
    """
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts a 'title' and 'summary' from text. The summary should be concise but capture the key details. Output strictly in JSON format with keys 'title' and 'summary'."},
            {"role": "user", "content": f"Extract title and summary from this text:\n\n{raw_text}"}
        ],
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        return {"title": "Unknown Title", "summary": raw_text}

async def draft_linkedin_post(title: str, summary: str, raw_text: str) -> dict:
    """
    Drafts a LinkedIn post and recommends media.
    Returns a dict with 'draft' and 'media_recommendation'.
    """
    personal_context = os.getenv("PERSONAL_CONTEXT", "")
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are an expert LinkedIn copywriter and social media manager. "
                    "Your job is to write an engaging LinkedIn post based on the provided title and summary. "
                    f"Author Background and Style: {personal_context}\n"
                    "You should also recommend how many pictures or what kind of media to include. "
                    "Output strictly in JSON format with keys 'draft' (the post content) and 'media_recommendation' (your advice on pictures/media)."
                )
            },
            {"role": "user", "content": f"Title: {title}\nSummary: {summary}\nOriginal context: {raw_text}\n\nPlease generate the LinkedIn post draft and media recommendation."}
        ],
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        return {"draft": "Could not generate draft.", "media_recommendation": "Could not generate recommendation."}
