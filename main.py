from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import random
import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# --- CORS Configuration ---
# Allows all origins for now. For production, you would specify your frontend's exact origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Pydantic model for request body validation
class UserInput(BaseModel):
    user_input: str

# Pydantic model for the LLM's structured response
class FanjankhanInterpretation(BaseModel):
    interpretation: str = Field(..., description="The main interpretation of the user's input, like a fortune-telling.")
    hope: float = Field(..., description="A float between 0.0 and 1.0 indicating the level of hope in the interpretation.", ge=0.0, le=1.0)
    energy: float = Field(..., description="A float between 0.0 and 1.0 indicating the level of energy or vitality in the interpretation.", ge=0.0, le=1.0)
    complexity: float = Field(..., description="A float between 0.0 and 1.0 indicating the complexity or depth of the interpretation.", ge=0.0, le=1.0)

# Define the tool for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "interpret_fanjankhan",
            "description": "Interprets the user's input related to fortune-telling or abstract concepts, returning a structured interpretation.",
            "parameters": FanjankhanInterpretation.model_json_schema(),
        },
    }
]

@app.post("/interpret", response_model=FanjankhanInterpretation)
async def interpret_input(data: UserInput):
    user_text = data.user_input

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are an experienced and mystical 'Fanjankhan' (fortune-teller using coffee cup reading).
                    Your task is to provide an interpretation of the user's input.
                    The interpretation should be insightful, slightly mysterious, and focus on general life aspects, future prospects, and emotional states.
                    Do NOT address the user by name. The response should be in Persian.
                    Always use the provided tool to structure your response, ensuring 'interpretation', 'hope', 'energy', and 'complexity' fields are filled.
                    The 'hope', 'energy', and 'complexity' values should be floats between 0.0 and 1.0, reflecting the sentiment and depth of your interpretation.
                    """,
                },
                {"role": "user", "content": user_text},
            ],
            model="gpt-4o-mini",
            tool_choice={"type": "function", "function": {"name": "interpret_fanjankhan"}},
            tools=tools,
            temperature=0.7, # Adjust for creativity
            max_tokens=500, # Max tokens for the overall response
        )

        # Extract the tool call arguments
        tool_call_arguments = chat_completion.choices[0].message.tool_calls[0].function.arguments
        # Parse the JSON string into a dictionary
        interpretation_data = json.loads(tool_call_arguments)

        # Validate with Pydantic model
        validated_interpretation = FanjankhanInterpretation(**interpretation_data)
        return validated_interpretation

    except Exception as e:
        # Log the error for debugging
        print(f"Error during LLM interpretation: {e}")
        # Return a fallback interpretation
        return FanjankhanInterpretation(
            interpretation=f"متاسفانه در حال حاضر قادر به تفسیر نیستم. خطای فنی: {e}",
            hope=0.2,
            energy=0.3,
            complexity=0.5
        )

# Optional: Add a root endpoint for health check or basic info
@app.get("/")
async def root():
    return {"message": "FastAPI Backend for Hana's Digital Fanjankhan is running!"}
