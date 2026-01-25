# app.py - FastAPI version (simpler, more reliable)
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re

app = FastAPI()

# Load model
MODEL_NAME = "Dalton-Khatri/freud-mental-health-assistant"
print(f"Loading {MODEL_NAME}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("✅ Model loaded!")

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 150
    temperature: float = 0.7

class GenerateResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "Freud AI is running", "model": MODEL_NAME}

@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    """Generate response from Freud model"""
    try:
        inputs = tokenizer(
            request.prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=1024
        )
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant response
        if "<|assistant|>:" in full_response:
            response = full_response.split("<|assistant|>:")[-1].strip()
            if "<|user|>:" in response:
                response = response.split("<|user|>:")[0].strip()
            response = re.sub(r'\[emotion:.*?\]', '', response).strip()
        else:
            response = full_response.strip()
        
        return GenerateResponse(response=response)
        
    except Exception as e:
        return GenerateResponse(response=f"Error: {str(e)}")

# For HF Spaces compatibility
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
