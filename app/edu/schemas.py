from pydantic import BaseModel

class UserProfileRequest(BaseModel):
    user_profile: str


class SkillRatings(BaseModel):
    creative: str
    engagement: str
    technical_proficiency: str
    strategic_thinking: str
    clarity: str
