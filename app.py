from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]

happy_words = {
    "love", "great", "awesome", "excellent", "good",
    "happy", "wonderful", "amazing", "fantastic",
    "best", "like", "enjoy"
}

sad_words = {
    "bad", "terrible", "awful", "hate", "sad",
    "worst", "angry", "disappointed", "poor",
    "horrible", "upset"
}

@app.get("/")
def home():
    return {"message": "working"}

@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    results = []

    for sentence in req.sentences:
        text = sentence.lower()

        happy_score = sum(word in text for word in happy_words)
        sad_score = sum(word in text for word in sad_words)

        if happy_score > sad_score:
            label = "happy"
        elif sad_score > happy_score:
            label = "sad"
        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}