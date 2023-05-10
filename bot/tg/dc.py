from typing import Optional
from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: int
    # first_name: Optional[str] = None
    # username: Optional[str] = None
    # type: str


class From(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: Optional[str] = None


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str


class ChatMember(BaseModel):
    user: User
    status: str
    until_date: Optional[int] = None


class MyChatMember(BaseModel):
    chat: Chat
    from_: From = Field(alias='from')
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember


class Message(BaseModel):
    chat: Chat
    text: str | None = None


class UpdateObj(BaseModel):
    update_id: int
    message: Optional[Message] = None
    my_chat_member: Optional[MyChatMember] = None


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message
