from pydantic import BaseModel

class Flash_Card(BaseModel):
  question: str
  answer: str

class Cards_List(BaseModel):
  cards: list[Flash_Card]
