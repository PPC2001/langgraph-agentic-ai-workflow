# So now we are creating the graph , first thing you create is state

import os
from typing import TypedDict
from pydantic import BaseModel , field_validator
from dataclasses import dataclass , field
from langgraph.graph import MessageState

#first way (Most common approach)
class State(TypedDict):
    topic: str
    summary: str
    score: int


#2nd way using pydantic
class State(BaseModel):
    topic: str
    summary: str = ""
    score: int


    @field_validator("score")
    def score_must_be_positive(cls, value):
        if value < 0:
            raise ValueError("Score must be a positive integer")
        return value


# 3rd way using dataclasses and it is used very rarely
@dataclass
class State:
    topic: str
    summary: str = ""
    messages: list[str] = field(default_factory=list)



#4th way
class State(MessageState):
    topic: str
    summary: str = ""
    score: int

