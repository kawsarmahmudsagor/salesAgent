from pydantic import BaseModel, EmailStr

class AdminBase(BaseModel):
    email: EmailStr
    name: str
    role: str

class AdminCreate(AdminBase):
    password: str  

class AdminRead(AdminBase):
    id: int
   
    class Config:
        orm_mode = True