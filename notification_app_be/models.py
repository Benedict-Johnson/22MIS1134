from pydantic import BaseModel


class Notification(BaseModel):
    ID: str
    Type: str
    Message: str
    Timestamp: str


class PriorityNotification(Notification):
    score: float
