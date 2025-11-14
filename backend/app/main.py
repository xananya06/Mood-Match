from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Mood Match API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
try:
    from app.api.routes import mood, matching
    app.include_router(mood.router)
    app.include_router(matching.router)
    print("✅ All routes loaded successfully!")
except Exception as e:
    print(f"❌ Error loading routes: {e}")
    import traceback
    traceback.print_exc()

@app.get("/")
def read_root():
    return {"message": "Mood Match API is running! 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}



