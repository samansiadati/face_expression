from pydantic import BaseModel

class Expression(BaseModel):
    angry: float
    disgust: float
    fear: float
    happy: float
    sad:float
    surprise:float
    neutral:float
