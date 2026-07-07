from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

EMAIL = "24f2006027@ds.study.iitm.ac.in"
API_KEY = "ak_relr3o507bdft10bjag3iyaa"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analytics")
def analytics(events: list[dict], x_api_key: str = Header(None, alias="X-API-Key")):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    total_events = len(events)

    unique_users = len({e["user"] for e in events})

    revenue = 0.0
    user_totals = {}

    for event in events:
        user = event["user"]
        amount = float(event["amount"])

        if amount > 0:
            revenue += amount
            user_totals[user] = user_totals.get(user, 0) + amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }