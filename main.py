from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai, os, json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"])
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class BusinessInput(BaseModel):
    business_type: str
    target_audience: str
    budget: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
async def generate(data: BusinessInput):
    prompt = f"""Business: {data.business_type}
Audience: {data.target_audience}
Budget: ${data.budget}/month
Return ONLY this JSON, no markdown:
{{"strategy":"...","posts":["...","..."]}}"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    raw = r.choices[0].message.content
    clean = raw.replace("```json","").replace("```","").strip()
    return json.loads(clean)
