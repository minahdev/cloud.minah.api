from pydantic import BaseModel

class UserSchema(BaseModel):
    userId: str
    password: str
    nickname: str
    email: str
    role:str
    