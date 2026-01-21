// lib/services/ai_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class AIService {
  // ===============================
  // CONFIGURATION
  // ===============================
  
  static const String _hfUsername = 'Dalton-Khatri';
  static const String _modelName = 'freud-mental-health-assistant';
  static const String _hfToken = '';
  
  // ✅ UPDATED: Using new HuggingFace router endpoint (old one deprecated)
  static const String _apiUrl = 'https://router.huggingface.co/models/$_hfUsername/$_modelName';
  
  // Generation parameters
  static const int _maxNewTokens = 200;  // Increased from 150
  static const double _temperature = 0.7;
  static const double _topP = 0.9;
  static const int _timeout = 60; // Increased to 60 seconds

  // ===============================
  // NEPAL CRISIS HELPLINES
  // ===============================
  
  static const String _crisisMessage = """
I'm concerned about what you're sharing. Please know that you're not alone, and there are people who can help immediately.

🆘 Nepal Crisis Helplines:
• National Mental Health Helpline: 1660 0102005
• Transcultural Psychosocial Organization (TPO): 9840021600
• Centre for Mental Health and Counselling (CMC): 01-4102037

If you're in immediate danger, please:
• Call Police: 100
• Call Ambulance: 102
• Reach out to a trusted friend or family member

I'm here to support you, but professional help is crucial right now. Please consider calling one of these numbers.""";

  static final List<String> _crisisKeywords = [
    'suicide', 'kill myself', 'end it all', 'want to die', 
    'self harm', 'hurt myself', 'no reason to live',
    'better off dead', 'end my life', 'take my life',
    'aatmahatya', 'marnu', 'jeevan sakaunu',
  ];

  // ===============================
  // EMOTION DETECTION
  // ===============================
  
  String _detectEmotion(String message) {
    final lowerMessage = message.toLowerCase();
    
    if (lowerMessage.contains(RegExp(r'\b(sad|lonely|empty|depressed|down|hopeless|cry|tears)\b'))) {
      return 'sad';
    }
    if (lowerMessage.contains(RegExp(r'\b(anxious|anxiety|worry|worried|nervous|panic|scared|afraid|fear)\b'))) {
      return 'anxious';
    }
    if (lowerMessage.contains(RegExp(r'\b(stress|stressed|overwhelm|overwhelmed|pressure|exhausted|tired)\b'))) {
      return 'stressed';
    }
    if (lowerMessage.contains(RegExp(r'\b(angry|mad|furious|frustrated|irritated|annoyed)\b'))) {
      return 'angry';
    }
    if (lowerMessage.contains(RegExp(r'\b(happy|joy|joyful|excited|great|good|wonderful|amazing)\b'))) {
      return 'happy';
    }
    
    return 'neutral';
  }

  // ===============================
  // CRISIS DETECTION
  // ===============================
  
  bool detectCrisis(String message) {
    final lowerMessage = message.toLowerCase();
    return _crisisKeywords.any((keyword) => lowerMessage.contains(keyword));
  }

  // ===============================
  // BUILD PROMPT
  // ===============================
  
  String _buildPrompt(List<Map<String, dynamic>> context) {
    final StringBuffer prompt = StringBuffer();
    
    // Check what format your model expects
    // Format Option 1: With special tokens (current)
    bool useSpecialTokens = true;
    
    if (useSpecialTokens) {
      // System message
      prompt.writeln('<|system|>: You are Freud, a calm, empathetic therapeutic AI assistant.');
      
      // Conversation history (limit to last 5 messages)
      final recentContext = context.length > 5 ? context.sublist(context.length - 5) : context;
      
      for (var message in recentContext) {
        final role = message['role'];
        final content = message['content'];
        
        if (role == 'user') {
          final emotion = _detectEmotion(content);
          prompt.writeln('<|user|>:');
          prompt.writeln('[emotion: $emotion]');
          prompt.writeln(content);
        } else if (role == 'assistant') {
          prompt.writeln('<|assistant|>:');
          prompt.writeln(content);
        }
      }
      
      // Prompt for assistant response
      prompt.write('<|assistant|>:\n');
    } else {
      // Format Option 2: Simple format (try this if Option 1 doesn't work)
      prompt.writeln('You are Freud, a calm empathetic mental health assistant.\n');
      
      // Only use last message for simplicity
      if (context.isNotEmpty) {
        final lastMessage = context.last;
        if (lastMessage['role'] == 'user') {
          prompt.writeln('User: ${lastMessage['content']}\n');
          prompt.write('Freud:');
        }
      }
    }
    
    return prompt.toString();
  }

  // ===============================
  // GENERATE RESPONSE (WITH DEBUG)
  // ===============================
  
  Future<String> generateResponse(List<Map<String, dynamic>> context) async {
    try {
      // Get the last user message
      final lastUserMessage = context.lastWhere(
        (msg) => msg['role'] == 'user',
        orElse: () => {'content': ''},
      )['content'] as String;

      // CRISIS DETECTION
      if (detectCrisis(lastUserMessage)) {
        return _crisisMessage;
      }

      // Build the prompt
      final prompt = _buildPrompt(context);
      
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('📤 SENDING TO MODEL:');
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print(prompt);
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

      // Call HuggingFace API
      final response = await http.post(
        Uri.parse(_apiUrl),
        headers: {
          'Authorization': 'Bearer $_hfToken',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'inputs': prompt,
          'parameters': {
            'max_new_tokens': _maxNewTokens,
            'temperature': _temperature,
            'top_p': _topP,
            'return_full_text': false,
            'do_sample': true,
          },
          'options': {
            'wait_for_model': true,
            'use_cache': false,  // Disable cache for testing
          },
        }),
      ).timeout(Duration(seconds: _timeout));

      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('📥 API RESPONSE:');
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('Status Code: ${response.statusCode}');
      print('Response Body: ${response.body}');
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        
        print('🔍 Parsed Data Type: ${data.runtimeType}');
        print('🔍 Parsed Data: $data');
        
        // HuggingFace returns a list with generated text
        if (data is List && data.isNotEmpty) {
          String generatedText = data[0]['generated_text'] ?? '';
          
          print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          print('✨ RAW GENERATED TEXT (BEFORE CLEANING):');
          print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          print(generatedText);
          print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          
          // Clean up the response
          generatedText = _cleanResponse(generatedText);
          
          print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          print('🧹 CLEANED TEXT (AFTER CLEANING):');
          print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          print(generatedText);
          print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          
          if (generatedText.isEmpty) {
            print('⚠️ CLEANED TEXT IS EMPTY! Using fallback.');
            return _getFallbackResponse(context);
          }
          
          print('✅ SUCCESS! Returning cleaned text.');
          return generatedText;
        } else {
          print('❌ UNEXPECTED RESPONSE FORMAT!');
          print('Expected: List with generated_text');
          print('Got: $data');
          return _getFallbackResponse(context);
        }
      } else if (response.statusCode == 503) {
        print('⏳ MODEL IS LOADING (503)');
        return "I'm warming up! Please wait about 20 seconds and send your message again. This happens when the model hasn't been used recently.";
      } else {
        print('❌ API ERROR ${response.statusCode}:');
        print(response.body);
        return _getFallbackResponse(context);
      }
      
    } catch (e, stackTrace) {
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('❌ EXCEPTION IN AI SERVICE:');
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      print('Error: $e');
      print('Stack Trace: $stackTrace');
      print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      return _getFallbackResponse(context);
    }
  }

  // ===============================
  // CLEAN RESPONSE
  // ===============================
  
  String _cleanResponse(String response) {
    print('🧹 CLEANING RESPONSE...');
    print('Input length: ${response.length}');
    
    // Remove extra whitespace
    response = response.trim();
    print('After trim: ${response.length} chars');
    
    // Remove any remaining tags
    response = response.replaceAll(RegExp(r'<\|.*?\|>'), '');
    print('After removing tags: ${response.length} chars');
    
    // Remove emotion tags
    response = response.replaceAll(RegExp(r'\[emotion:.*?\]'), '');
    print('After removing emotion tags: ${response.length} chars');
    
    // Stop at the next user turn if model generated it
    if (response.contains('<|user|>')) {
      response = response.split('<|user|>')[0].trim();
      print('After stopping at <|user|>: ${response.length} chars');
    }
    
    // IMPORTANT: Don't limit to 3 lines - let the full response through!
    // Only split if there are way too many lines (> 10)
    final lines = response.split('\n').where((line) => line.trim().isNotEmpty).toList();
    print('Total non-empty lines: ${lines.length}');
    
    if (lines.length > 10) {
      response = lines.take(10).join('\n');
      print('Limited to 10 lines');
    }
    
    final cleaned = response.trim();
    print('Final cleaned length: ${cleaned.length} chars');
    
    return cleaned;
  }

  // ===============================
  // FALLBACK RESPONSES
  // ===============================
  
  String _getFallbackResponse(List<Map<String, dynamic>> context) {
    print('⚠️ USING FALLBACK RESPONSE');
    
    if (context.isEmpty) {
      return "Hello! I'm Freud, your AI companion for mental wellness. I'm here to listen and support you. How are you feeling today?";
    }

    final lastMessage = context.last['content'].toString().toLowerCase();

    if (lastMessage.contains(RegExp(r'\b(anxious|anxiety|worry)\b'))) {
      return "I understand you're feeling anxious. That can be really overwhelming. Would you like to try a simple breathing exercise? Take a deep breath in for 4 counts, hold for 4, and exhale for 4.";
    } else if (lastMessage.contains(RegExp(r'\b(sad|depressed|down|lonely)\b'))) {
      return "I hear that you're going through a difficult time. It's okay to feel this way. Would you like to talk about what's making you feel sad?";
    } else if (lastMessage.contains(RegExp(r'\b(stressed|overwhelm)\b'))) {
      return "Stress can be really challenging. Let's work through this together. What's the main source of your stress right now?";
    } else if (lastMessage.contains(RegExp(r'\b(happy|good|great|wonderful)\b'))) {
      return "That's wonderful to hear! I'm glad you're feeling positive. Would you like to share what's bringing you joy?";
    } else {
      return "Thank you for sharing that with me. I'm listening. Can you tell me more about how you're feeling?";
    }
  }
}
