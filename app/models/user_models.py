from pydantic import BaseModel

class UserPublic(BaseModel):
    username: str
    
class User(UserPublic):
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    
class UserInDB(User):
    hashed_password: str
