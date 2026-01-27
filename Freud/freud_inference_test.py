"""
Freud Mental Health AI - Inference Testing Script
==================================================

Test your trained model locally before deploying to production.

Usage:
    python freud_inference_test.py

Author: Your Project
Date: January 2026
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path
import sys


class FreudTester:
    """
    Test harness for Freud mental health model.
    
    This class helps you test your model's responses interactively
    to ensure quality before deployment.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the tester with a trained model.
        
        Args:
            model_path: Path to your trained model directory or HuggingFace model name
        """
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        
        self.system_prompt = (
            "You are Freud, a calm, empathetic therapeutic AI assistant. "
            "You respond thoughtfully, kindly, and supportively. "
            "You ask gentle follow-up questions and never judge the user."
        )
    
    def load_model(self):
        """Load the model and tokenizer"""
        print(f"🔄 Loading model from {self.model_path}...")
        
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # Set padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map="auto",
                torch_dtype=torch.float16,  # Use FP16 for faster inference
                trust_remote_code=True
            )
            
            print(f"✅ Model loaded successfully!")
            print(f"📊 Parameters: {self.model.num_parameters():,}")
            print(f"🎮 Device: {next(self.model.parameters()).device}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)
    
    def generate_response(
        self,
        user_input: str,
        emotion: str = "neutral",
        max_tokens: int = 150,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """
        Generate a response from the model.
        
        Args:
            user_input: The user's message
            emotion: Emotion tag (sad, anxious, happy, etc.)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated response string
        """
        # Build prompt in training format
        prompt = (
            f"<|system|>: {self.system_prompt}\n"
            f"<|user|>:\n"
            f"[emotion: {emotion}]\n"
            f"{user_input.strip()}\n"
            f"<|assistant|>:\n"
        )
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.model.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                repetition_penalty=1.2,  # Prevent repetition
                no_repeat_ngram_size=3,  # Prevent repeating 3-grams
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract assistant's response
        response = self._extract_response(full_response, prompt)
        
        return response
    
    def _extract_response(self, full_text: str, original_prompt: str) -> str:
        """Extract only the assistant's response from generated text"""
        # Remove the original prompt
        response = full_text.replace(original_prompt, "").strip()
        
        # Stop at next user tag if present
        if "<|user|>" in response:
            response = response.split("<|user|>")[0].strip()
        
        # Remove any remaining tags
        import re
        response = re.sub(r'<\|.*?\|>:?', '', response)
        response = re.sub(r'\[emotion:.*?\]', '', response)
        
        return response.strip()
    
    def run_test_suite(self):
        """Run a predefined test suite to check model quality"""
        print("\n" + "="*80)
        print("🧪 RUNNING TEST SUITE")
        print("="*80 + "\n")
        
        test_cases = [
            ("Hi", "greeting", "Should greet warmly"),
            ("Hello there", "greeting", "Should greet and ask how they are"),
            ("I feel sad", "sad", "Should be empathetic"),
            ("I'm really depressed", "sad", "Should offer support"),
            ("I'm anxious about my exam", "anxious", "Should validate and help"),
            ("I'm so stressed", "stressed", "Should acknowledge and offer help"),
            ("I had a great day!", "happy", "Should celebrate with them"),
            ("I'm angry at my friend", "angry", "Should validate feelings"),
            ("Thanks for your help", "thanks", "Should acknowledge graciously"),
            ("Goodbye", "goodbye", "Should end warmly"),
        ]
        
        passed = 0
        failed = 0
        
        for i, (user_input, emotion, expected_behavior) in enumerate(test_cases, 1):
            print(f"\nTest {i}/{len(test_cases)}: {expected_behavior}")
            print(f"👤 User ({emotion}): {user_input}")
            
            try:
                response = self.generate_response(user_input, emotion)
                print(f"🤖 Freud: {response}")
                
                # Basic quality checks
                is_good = self._check_quality(response, user_input)
                
                if is_good:
                    print("✅ PASS")
                    passed += 1
                else:
                    print("⚠️ NEEDS REVIEW")
                    failed += 1
                    
            except Exception as e:
                print(f"❌ FAIL: {e}")
                failed += 1
            
            print("-" * 80)
        
        print(f"\n📊 Test Results: {passed}/{len(test_cases)} passed")
        
        if failed == 0:
            print("🎉 All tests passed! Model looks good!")
        else:
            print(f"⚠️ {failed} tests need review. Check responses above.")
    
    def _check_quality(self, response: str, user_input: str) -> bool:
        """Basic quality checks for responses"""
        # Check 1: Response not empty
        if not response or len(response) < 10:
            return False
        
        # Check 2: No leaked tags
        if '<|' in response or '|>' in response:
            return False
        
        # Check 3: Not too long (rambling)
        if len(response) > 500:
            return False
        
        # Check 4: Not repeating user input verbatim
        if user_input.lower() in response.lower():
            # Some overlap is okay, but not entire message
            if len(user_input) > 20 and user_input.lower() == response.lower()[:len(user_input)]:
                return False
        
        return True
    
    def interactive_mode(self):
        """Run in interactive mode for manual testing"""
        print("\n" + "="*80)
        print("💬 INTERACTIVE MODE")
        print("="*80)
        print("\nType your messages to test the model.")
        print("Commands:")
        print("  /emotion <emotion> - Set emotion (sad, anxious, happy, etc.)")
        print("  /quit - Exit")
        print("="*80 + "\n")
        
        current_emotion = "neutral"
        
        while True:
            try:
                user_input = input(f"\n👤 You ({current_emotion}): ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    if user_input == '/quit':
                        print("👋 Goodbye!")
                        break
                    elif user_input.startswith('/emotion'):
                        parts = user_input.split()
                        if len(parts) > 1:
                            current_emotion = parts[1]
                            print(f"✓ Emotion set to: {current_emotion}")
                        else:
                            print("⚠️ Usage: /emotion <emotion_name>")
                        continue
                    else:
                        print("⚠️ Unknown command")
                        continue
                
                # Generate response
                response = self.generate_response(user_input, current_emotion)
                print(f"🤖 Freud: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main execution function"""
    print("🧠 Freud Mental Health AI - Inference Tester")
    print("="*80 + "\n")
    
    # Model path - UPDATE THIS to your model location
    MODEL_PATH = "freud_phi2_model_merged"  # Or your HuggingFace model name
    
    # Check if model exists
    if not Path(MODEL_PATH).exists():
        print(f"❌ Model not found at: {MODEL_PATH}")
        print("\n💡 Options:")
        print("   1. Download from HuggingFace: your-username/freud-phi2-mental-health")
        print("   2. Update MODEL_PATH to your model location")
        print("   3. Use HuggingFace model name directly")
        sys.exit(1)
    
    # Initialize tester
    tester = FreudTester(MODEL_PATH)
    tester.load_model()
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Run test suite (automated tests)")
    print("2. Interactive mode (chat with the model)")
    print("3. Both")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        tester.run_test_suite()
    elif choice == "2":
        tester.interactive_mode()
    elif choice == "3":
        tester.run_test_suite()
        print("\n" + "="*80)
        tester.interactive_mode()
    else:
        print("Invalid choice. Running test suite...")
        tester.run_test_suite()


if __name__ == "__main__":
    main()
