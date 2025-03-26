from fastapi import APIRouter,HTTPException
from edu.course_recommender import UserProfiledCourseRecommender
from groq import Groq
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
import re

load_dotenv()

router = APIRouter(prefix="/edu", tags=["Education"])
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

recommender = UserProfiledCourseRecommender('data/courses.csv')


class UserProfileRequest(BaseModel):
    user_profile: str


class SkillRatings(BaseModel):
    creative: str
    technical: str
    strategic: str
    content: str
    Editing: str


@router.post("/skill-ratings")
async def submit_skill_ratings(ratings: SkillRatings):
    """
    Accepts skill ratings and prints them.
    """
    print("Received skill ratings:")
    print(f"Creative: {ratings.creative}")
    print(f"Technical: {ratings.technical}")
    print(f"Strategic: {ratings.strategic}")
    print(f"Content: {ratings.content}")
    print(f"Editing: {ratings.Editing}")
    
    return {"message": "Ratings received successfully", "ratings": ratings.dict()}


@router.post("/course-recommendation")
async def course_recommendation_endpoint(request: UserProfileRequest):
    """
    Accepts a user profile and returns course recommendations.
    """
    try:
        recommendations = recommender.recommend_courses(request.user_profile)
        # Convert the recommendations JSON string to a JSON object
        return json.loads(recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mcq-test")
async def generate_mcq_test():

    prompt = (
        "Create a 20-question multiple-choice test on 'Content Creation' with challenging, non-cliché questions. "
        "Divide the test evenly into five categories: creativity, clarity, engagement, technical proficiency, and strategic thinking (4 questions per category). "
        "Each question must include 4 concise answer options labeled A, B, C, D, with one correct answer. "
        "Output the result as a single valid JSON object using the following structure and nothing else (no explanations or chain-of-thought):\n\n"
        "{\"questions\": [\n"
        "    {\"characteristic\": \"...\", \"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"correct_answer\": \"...\"},\n"
        "    ...\n"
        "]}"
    )

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=2048,
        top_p=0.95,
        stream=False,
        reasoning_format="raw"
    )

    response_text = completion.choices[0].message.content

    print(response_text)

    # Try to extract JSON from triple-backticks (```json ... ```)
    match = re.search(r'```json(.*?)```', response_text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
    else:
        # Fallback: extract the substring starting at the first '{' and ending at the last '}'
        json_start = response_text.find('{')
        json_end = response_text.rfind('}')
        if json_start != -1 and json_end != -1:
            json_str = response_text[json_start:json_end+1]
        else:
            return {"error": "Failed to find JSON structure in the LLM response."}

    cleaned_json_str = clean_json(json_str)

    try:
        extracted_json = json.loads(cleaned_json_str)
    except json.JSONDecodeError as e:
        return {"error": f"JSON parsing error: {str(e)}\n{response_text}"}

    return {"response":extracted_json}


def clean_json(json_str: str) -> str:
    cleaned = re.sub(r',\s*([\]}])', r'\1', json_str)
    return cleaned