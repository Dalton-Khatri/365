# 🚀 Freud AI - Deployment Guide

## Complete guide to deploy your trained model to production

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Download Trained Model](#download-trained-model)
3. [Test Model Locally](#test-model-locally)
4. [Deploy to HuggingFace Spaces](#deploy-to-huggingface-spaces)
5. [Update Flutter App](#update-flutter-app)
6. [Testing & Monitoring](#testing--monitoring)
7. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

Before deploying, make sure you have:

- ✅ Successfully trained model on Kaggle
- ✅ Model uploaded to HuggingFace Hub
- ✅ HuggingFace account with access token
- ✅ Python 3.10+ installed locally (for testing)
- ✅ Flutter app ready to update

---

## 2. Download Trained Model

### Option A: Download from HuggingFace

```bash
# Install huggingface-cli if not installed
pip install huggingface-hub

# Login to HuggingFace
huggingface-cli login

# Download your model
huggingface-cli download your-username/freud-phi2-mental-health --local-dir ./freud_model
```

### Option B: Download from Kaggle

1. Go to your Kaggle notebook
2. Navigate to the output directory: `freud_phi2_model_merged/`
3. Click "Download" button
4. Extract the zip file locally

---

## 3. Test Model Locally

**Critical**: Always test before deploying to production!

```bash
# Install dependencies
pip install torch transformers accelerate

# Run the test script
python freud_inference_test.py
```

### What to Check:

1. **No conversation loops** - Model stops after one response
2. **No leaked tags** - No `<|user|>` or `<|system|>` in output
3. **Quality responses** - Empathetic, contextual, helpful
4. **No repetition** - Doesn't repeat the same phrases
5. **Appropriate length** - Not too short, not rambling

### Example Good Response:

```
User: I feel sad
Freud: I'm sorry you're feeling this way. Sadness can be really difficult to sit with. Would you like to talk about what's been weighing on you? Sometimes sharing can help lighten the burden.
```

### Example Bad Response (Don't Deploy!):

```
User: I feel sad
Freud: I'm here to listen and support. <|user|>: Tell me more <|assistant|>: I'm here...
```

If you see bad responses, go back to training and:
- Increase `repetition_penalty` during inference
- Check if special tokens are properly set
- Consider retraining with better stopping criteria

---

## 4. Deploy to HuggingFace Spaces

### Step 1: Create New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Name: `freud-ai-backend`
4. SDK: **Gradio** (not Docker, easier)
5. Hardware: **CPU Basic** (free) or **T4 GPU** (paid, faster)

### Step 2: Update app.py for New Model

Create this `app.py` in your Space:

```python
# app.py - Updated for Phi-2 Model
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
import gradio as gr

app = FastAPI()

# Load your trained model
MODEL_NAME = "your-username/freud-phi2-mental-health"  # UPDATE THIS
print(f"🔄 Loading {MODEL_NAME}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("✅ Model loaded successfully!")

SYSTEM_PROMPT = (
    "You are Freud, a calm, empathetic therapeutic AI assistant. "
    "You respond thoughtfully, kindly, and supportively. "
    "You ask gentle follow-up questions and never judge the user."
)

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 150
    temperature: float = 0.7

class GenerateResponse(BaseModel):
    response: str

def clean_response(text: str, original_prompt: str = "") -> str:
    """Extract and clean only the assistant's response"""
    if original_prompt:
        text = text.replace(original_prompt, "").strip()
    
    # Stop at next <|user|> tag
    if "<|user|>" in text:
        text = text.split("<|user|>")[0]
    
    # Remove all formatting tags
    text = re.sub(r'<\|.*?\|>:?', '', text)
    text = re.sub(r'\[emotion:.*?\]', '', text)
    text = text.strip()
    
    return text

@app.get("/")
def read_root():
    return {
        "status": "✅ Freud AI is running",
        "model": MODEL_NAME,
        "version": "3.0 - Phi-2"
    }

@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    """Generate response from Freud model"""
    try:
        inputs = tokenizer(
            request.prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=0.9,
                do_sample=True,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        cleaned_response = clean_response(full_response, request.prompt)
        
        if len(cleaned_response) < 10:
            cleaned_response = "I'm here to listen. Could you tell me more?"
        
        return GenerateResponse(response=cleaned_response)
        
    except Exception as e:
        return GenerateResponse(response=f"Error: {str(e)}")

# Gradio interface (for testing in browser)
def chat(message):
    prompt = f"{SYSTEM_PROMPT}\n<|user|>:\n[emotion: neutral]\n{message}\n<|assistant|>:\n"
    request = GenerateRequest(prompt=prompt)
    response = generate(request)
    return response.response

demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(lines=2, placeholder="How are you feeling?"),
    outputs=gr.Textbox(label="Freud's Response"),
    title="🧠 Freud Mental Health AI",
    description="Talk to Freud about your feelings"
)

# Launch both FastAPI and Gradio
if __name__ == "__main__":
    import uvicorn
    import threading
    
    # Start FastAPI in background
    threading.Thread(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=7860),
        daemon=True
    ).start()
    
    # Launch Gradio
    demo.launch(server_name="0.0.0.0", server_port=7861)
```

### Step 3: Update requirements.txt

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
gradio==4.36.1
transformers==4.36.2
torch==2.1.2
accelerate==0.26.1
pydantic==2.5.3
```

### Step 4: Push to Space

```bash
# Clone your space
git clone https://huggingface.co/spaces/your-username/freud-ai-backend
cd freud-ai-backend

# Add files
cp app.py .
cp requirements.txt .

# Commit and push
git add .
git commit -m "Deploy Phi-2 model"
git push
```

### Step 5: Wait for Build

- HuggingFace will build your Space (5-10 minutes)
- Check the logs for any errors
- Once running, test at: `https://your-username-freud-ai-backend.hf.space`

---

## 5. Update Flutter App

### Update ai_service.dart

Change only the backend URL:

```dart
class AIService {
  // Update this line to your new Space URL
  static const String backendUrl = 'https://your-username-freud-ai-backend.hf.space';
  
  // Rest of the code stays the same!
}
```

That's it! Your app now uses the new, better model.

---

## 6. Testing & Monitoring

### Test Checklist After Deployment:

```
□ Space is running (green status on HuggingFace)
□ Can access /{space-url} and see status JSON
□ Can access /{space-url}/generate with POST request
□ Flutter app connects successfully
□ Test greeting: "Hi"
□ Test sad emotion: "I feel sad"
□ Test anxious emotion: "I'm worried"
□ Test happy emotion: "I had a great day"
□ No conversation loops in any response
□ No leaked tags (<|user|>, <|system|>)
□ Responses are empathetic and contextual
□ Response time is acceptable (<5 seconds)
```

### Monitor Performance:

1. **HuggingFace Space Logs**
   - Check for errors
   - Monitor memory usage
   - Watch request count

2. **Flutter App**
   - Monitor crash reports
   - Track response quality
   - Collect user feedback

3. **User Experience**
   - Add feedback buttons in app
   - Track conversation quality ratings
   - Monitor for complaints about repetition

---

## 7. Troubleshooting

### Issue: Space Won't Start

**Symptoms**: Red status on HuggingFace, build fails

**Solutions**:
- Check logs for error messages
- Verify `requirements.txt` versions match
- Make sure model name is correct
- Check if you have enough quota (GPU spaces cost credits)

### Issue: Model Too Large / Out of Memory

**Symptoms**: Space crashes with OOM error

**Solutions**:
- Use CPU space instead of GPU (slower but works)
- Load model in 8-bit quantization:
  ```python
  model = AutoModelForCausalLM.from_pretrained(
      MODEL_NAME,
      load_in_8bit=True,  # Add this
      device_map="auto"
  )
  ```
- Upgrade to paid GPU space (T4 or A10G)

### Issue: Responses Still Have Loops

**Symptoms**: Model outputs `<|user|>` tags

**Solutions**:
- Check `clean_response()` function is being called
- Increase `repetition_penalty` to 1.3
- Add `no_repeat_ngram_size=3` in generation
- Retrain with better stopping tokens

### Issue: Responses Too Slow

**Symptoms**: Takes >10 seconds per response

**Solutions**:
- Upgrade to GPU space
- Reduce `max_tokens` to 100
- Use smaller model (GPT-Neo 1.3B)
- Cache frequently used responses

### Issue: Flutter App Can't Connect

**Symptoms**: Timeout errors, connection refused

**Solutions**:
- Verify Space URL is correct (no trailing slash)
- Check Space is running (green status)
- Try accessing Space URL in browser first
- Check network settings in Flutter app

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ HuggingFace Space shows green "Running" status
✅ Can access Space URL in browser
✅ API endpoint `/generate` works via POST
✅ Flutter app connects and sends/receives messages
✅ Responses are clean (no tags, no loops)
✅ Responses are high quality (empathetic, contextual)
✅ Average response time < 5 seconds
✅ No crashes or errors in production

---

## 📞 Next Steps

1. **Monitor for a week** - Collect user feedback
2. **A/B test** - Compare with old model
3. **Iterate** - Fine-tune based on real usage
4. **Scale** - Upgrade hardware if needed

---

## 🆘 Need Help?

If you encounter issues:

1. Check HuggingFace Space logs
2. Review this deployment guide
3. Test model locally first
4. Check model card on HuggingFace

---

**Good luck with your deployment! 🚀**

*Last updated: January 2026*
