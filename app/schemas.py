from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EmailModel(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    model_config = ConfigDict(from_attributes=True)


class UserBase(EmailModel):
    username: str = Field(description="Имя пользователя")
    city: str  = Field(description="Город проживания")
    role: str = Field(description="Роль пользователя")


class SUserRegister(UserBase):
    password: str = Field(description="пароль")


class SUserAuth(EmailModel):
    password: str = Field(description="пароль")
