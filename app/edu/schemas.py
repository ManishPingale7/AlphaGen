from pydantic import BaseModel

class UserProfileRequest(BaseModel):
    user_profile: str


class SkillRatings(BaseModel):
    creative: str
    technical: str
    strategic: str
    content: str
    Editing: str
