# 🧠 FREUD AI - COMPLETE RETRAINING BACKUP DOCUMENT

**Use this document in new chats if token limit is reached**

Last Updated: January 27, 2026

---

## 📊 PROJECT STATUS

### Current Situation:
- **Existing Model**: GPT-Neo 125M (too small, generates loops)
- **Dataset**: ~30K training samples, 80 intents
- **Problem**: Repetitive responses, conversation loops, leaked tags
- **Goal**: Retrain with larger model for better quality

### Solution:
Train **Microsoft Phi-2 (2.7B params)** using **QLoRA** on **Kaggle P100** GPU

---

## 🎯 WHAT WE'RE BUILDING

### Model Architecture:
- **Base**: Microsoft Phi-2 (2.7B parameters)
- **Method**: QLoRA (4-bit quantization + Low-Rank Adaptation)
- **Training**: 3 epochs on ~30K samples
- **Hardware**: Kaggle P100 GPU (16GB VRAM)
- **Time**: ~3-4 hours

### Why This Works Better:
1. ✅ 20x larger model (2.7B vs 125M params)
2. ✅ QLoRA trains efficiently (only 0.5% of params)
3. ✅ Phi-2 better at following instructions
4. ✅ Proper stopping tokens prevent loops
5. ✅ Fits in P100 with 4-bit quantization

---

## 📦 FILES PROVIDED

### 1. freud_retraining_guide.md
Complete documentation explaining the entire process, why it works, and what to expect.

### 2. freud_dataset_builder.py
Python script that:
- Loads your Dataset.json
- Augments responses to prevent repetition
- Creates single-turn and multi-turn samples
- Splits into train/validation (90/10)
- Outputs to `freud_training_data/` folder

**Usage:**
```bash
python freud_dataset_builder.py
```

### 3. freud_trainer.ipynb
Complete Kaggle notebook with:
- All installation steps
- Data loading and verification
- Model loading with 4-bit quantization
- QLoRA configuration
- Training with checkpoints
- Testing
- Upload to HuggingFace

**Duration**: 3-4 hours on Kaggle P100

### 4. freud_inference_test.py
Local testing script with:
- Interactive mode (chat with model)
- Automated test suite
- Quality checks
- Response validation

**Usage:**
```bash
python freud_inference_test.py
```

### 5. deployment_guide.md
Step-by-step guide for:
- Testing model locally
- Deploying to HuggingFace Spaces
- Updating Flutter app
- Monitoring and troubleshooting

### 6. requirements.txt
All Python dependencies needed

---

## 🚀 STEP-BY-STEP EXECUTION PLAN

### Phase 1: Data Preparation (5 minutes)

1. **Place Dataset.json** in working directory
2. **Run dataset builder:**
   ```bash
   python freud_dataset_builder.py
   ```
3. **Verify output:**
   - `freud_training_data/train.json` (~27K samples)
   - `freud_training_data/validation.json` (~3K samples)
   - `freud_training_data/dataset_stats.json`

### Phase 2: Upload to Kaggle (5 minutes)

1. **Zip the training data:**
   ```bash
   zip -r freud_training_data.zip freud_training_data/
   ```

2. **Upload to Kaggle:**
   - Go to kaggle.com/datasets
   - Click "New Dataset"
   - Upload `freud_training_data.zip`
   - Make it public
   - Note the dataset path

3. **Upload notebook:**
   - Upload `freud_trainer.ipynb`
   - Link to your dataset
   - Enable GPU (P100)
   - Enable internet

### Phase 3: Training (3-4 hours)

1. **Update configuration** in notebook:
   ```python
   TRAIN_DATA_PATH = "/kaggle/input/your-dataset-name/train.json"
   VAL_DATA_PATH = "/kaggle/input/your-dataset-name/validation.json"
   HF_MODEL_NAME = "your-username/freud-phi2-mental-health"
   ```

2. **Run all cells** in order

3. **Monitor progress:**
   - Loss should decrease
   - Check checkpoint saves
   - ~1000 steps per epoch

4. **Login to HuggingFace** when prompted

5. **Wait for completion** (~3-4 hours)

### Phase 4: Testing (10 minutes)

1. **Download model** from HuggingFace or Kaggle

2. **Run test script:**
   ```bash
   python freud_inference_test.py
   ```

3. **Check for:**
   - ✅ No conversation loops
   - ✅ No leaked tags
   - ✅ Empathetic responses
   - ✅ Context awareness

4. **If tests fail:**
   - Adjust inference parameters
   - Check if model trained properly
   - Review training logs

### Phase 5: Deployment (30 minutes)

1. **Create HuggingFace Space:**
   - Name: `freud-ai-backend`
   - SDK: Gradio
   - Hardware: CPU or T4 GPU

2. **Update app.py** (from deployment guide)

3. **Push to Space:**
   ```bash
   git clone https://huggingface.co/spaces/your-username/freud-ai-backend
   cd freud-ai-backend
   # Add app.py and requirements.txt
   git add .
   git commit -m "Deploy Phi-2 model"
   git push
   ```

4. **Wait for build** (5-10 mins)

5. **Update Flutter app:**
   ```dart
   static const String backendUrl = 'https://your-username-freud-ai-backend.hf.space';
   ```

---

## ⚙️ CONFIGURATION REFERENCE

### Training Hyperparameters:
```python
BASE_MODEL = "microsoft/phi-2"  # 2.7B params
LEARNING_RATE = 2e-4
NUM_EPOCHS = 3
BATCH_SIZE = 4
GRADIENT_ACCUMULATION_STEPS = 4  # Effective batch = 16
MAX_SEQ_LENGTH = 512
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
```

### Inference Settings:
```python
max_new_tokens = 150
temperature = 0.7
top_p = 0.9
repetition_penalty = 1.2
no_repeat_ngram_size = 3
```

---

## 🐛 TROUBLESHOOTING GUIDE

### Issue: Out of Memory on Kaggle

**Solutions:**
1. Reduce `BATCH_SIZE` to 2
2. Reduce `MAX_SEQ_LENGTH` to 384
3. Use GPT-Neo 1.3B instead (backup option)

**Code change:**
```python
BASE_MODEL = "EleutherAI/gpt-neo-1.3B"  # Smaller alternative
BATCH_SIZE = 2  # Reduce if needed
```

### Issue: Model Still Generates Loops

**Solutions:**
1. Increase `repetition_penalty` to 1.3
2. Add stricter cleaning in backend:
   ```python
   # In clean_response()
   if "<|user|>" in text or "<|system|>" in text:
       text = text.split("<|")[0]  # Hard stop
   ```

### Issue: Training Loss Not Decreasing

**Solutions:**
1. Check data quality (run dataset builder again)
2. Increase learning rate to 3e-4
3. Reduce batch size (might be gradient vanishing)

### Issue: Space Won't Start

**Solutions:**
1. Check HuggingFace logs for errors
2. Verify model name is correct
3. Use CPU space if GPU fails
4. Check requirements.txt versions

---

## 📊 EXPECTED RESULTS

### Before (Current Model):
```
User: I feel sad
Model: I'm here to listen and support you. <|user|>: <|assistant|>: Tell me more...
```

### After (New Model):
```
User: I feel sad  
Model: I'm sorry you're feeling this way. Sadness can be really difficult to sit with. Would you like to talk about what's been weighing on you? Sometimes sharing can help lighten the burden.
```

---

## 🎯 QUALITY CHECKLIST

After training and deployment, verify:

**Model Quality:**
- [ ] No conversation loops
- [ ] No leaked formatting tags
- [ ] Empathetic and contextual responses
- [ ] Appropriate response length (50-200 words)
- [ ] No repetitive phrases
- [ ] Handles multiple emotions correctly

**Technical:**
- [ ] HuggingFace Space running (green status)
- [ ] API endpoint responds < 5 seconds
- [ ] Flutter app connects successfully
- [ ] No crashes or errors in production

**User Experience:**
- [ ] Responses feel human-like
- [ ] Appropriate for mental health context
- [ ] Follows conversation naturally
- [ ] Offers helpful suggestions when appropriate

---

## 📈 PERFORMANCE METRICS

### Dataset:
- Training samples: ~27,000
- Validation samples: ~3,000
- Emotions covered: 80 intents
- Average conversation length: 2-3 turns

### Model:
- Parameters: 2.7 billion
- Trainable params: ~14 million (0.5%)
- Quantization: 4-bit (NF4)
- Memory footprint: ~3.5 GB

### Training:
- Epochs: 3
- Steps per epoch: ~1,000
- Total training time: 3-4 hours
- GPU: Kaggle P100 (16GB)

### Inference:
- Response time: 2-4 seconds (CPU), <1s (GPU)
- Max tokens: 150
- Context window: 512 tokens

---

## 🔧 BACKUP PLAN: If Phi-2 Doesn't Work

### Use GPT-Neo 1.3B Instead:

**In freud_trainer.ipynb**, change:
```python
BASE_MODEL = "EleutherAI/gpt-neo-1.3B"
```

**LoRA targets change to:**
```python
target_modules = ["c_attn", "c_proj", "c_fc"]  # GPT-Neo specific
```

**Everything else stays the same!**

---

## 📞 QUICK REFERENCE COMMANDS

### Dataset Preparation:
```bash
python freud_dataset_builder.py
```

### Local Testing:
```bash
python freud_inference_test.py
```

### HuggingFace Login:
```bash
huggingface-cli login
```

### Download Model:
```bash
huggingface-cli download your-username/freud-phi2-mental-health --local-dir ./model
```

### Deploy to Space:
```bash
git clone https://huggingface.co/spaces/your-username/freud-ai-backend
cd freud-ai-backend
# Add files
git add .
git commit -m "Deploy model"
git push
```

---

## 🎓 KEY INSIGHTS

### Why QLoRA Works:
- Trains only 0.5% of parameters
- Uses 4-bit quantization (4x less memory)
- LoRA adapters can be merged later
- Same quality as full fine-tuning
- Enables large model training on limited hardware

### Why Phi-2:
- Microsoft-trained on high-quality data
- Better instruction following
- More coherent responses
- Designed for chat/dialogue
- Fits in 16GB VRAM with quantization

### Training Tips:
- Save checkpoints frequently (every 500 steps)
- Monitor validation loss (should decrease)
- Use gradient accumulation for larger effective batch
- Warmup prevents training instability
- Lower learning rate for stability

---

## 🎯 SUCCESS CRITERIA

Your retraining is successful when:

✅ Model trains without OOM errors
✅ Training loss decreases steadily
✅ Validation loss decreases (not overfitting)
✅ Test responses are clean (no loops/tags)
✅ Responses are empathetic and contextual
✅ Model deploys to HuggingFace successfully
✅ Flutter app works with new model
✅ Users report better conversation quality

---

## 📝 NOTES FOR NEW CHAT

If you need to start a new chat due to token limits, provide:

1. **This backup document**
2. **Your specific issue** (if training failed, where?)
3. **Error messages** (logs, screenshots)
4. **What you've tried** (debugging steps)

This document contains everything needed to continue without repeating explanations!

---

## 🔗 RESOURCES

- [Phi-2 Model Card](https://huggingface.co/microsoft/phi-2)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [PEFT Documentation](https://huggingface.co/docs/peft)
- [Kaggle GPU Quotas](https://www.kaggle.com/code)
- [HuggingFace Spaces](https://huggingface.co/docs/hub/spaces)

---

## ✅ FINAL CHECKLIST

Before starting, make sure you have:

- [ ] Dataset.json file ready
- [ ] All 6 Python files saved locally
- [ ] Kaggle account with GPU quota available (4+ hours)
- [ ] HuggingFace account with token
- [ ] Python 3.10+ installed locally
- [ ] 20GB+ free disk space
- [ ] Stable internet connection
- [ ] 4-6 hours of time available

---

**Everything you need is in this document and the provided files!**

**Good luck with your training! 🚀**

*Created: January 27, 2026*
*Version: 1.0*
