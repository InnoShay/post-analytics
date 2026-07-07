from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

EMAIL = "24f2006027@ds.study.iitm.ac.in"
API_KEY = "ak_relr3o507bdft10bjag3iyaa"

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "running"}


@app.options("/analytics")
async def analytics_options():
    return Response(status_code=200)


@app.post("/analytics")
async def analytics(request: Request):
    api_key = request.headers.get("X-API-Key")

    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = await request.json()

    total_events = len(events)
    users = set()
    revenue = 0.0
    user_totals = {}

    for event in events:
        user = event["user"]
        amount = float(event["amount"])

        users.add(user)

        if amount > 0:
            revenue += amount
            user_totals[user] = user_totals.get(user, 0.0) + amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user,
    }