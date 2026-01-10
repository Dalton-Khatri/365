eng_to_nepali = {
    "hello": "नमस्ते",
    "good morning": "शुभ प्रभात",
    "good night": "शुभ रात्री",
    "thank you": "धन्यवाद",
    "please": "कृपया",
    "yes": "हो",
    "no": "होइन",
    "water": "पानी",
    "food": "खाना",
    "house": "घर",
    "student": "विद्यार्थी",
    "teacher": "शिक्षक",
    "computer": "कम्प्युटर",
    "book": "किताब",
    "school": "विद्यालय",
    "friend": "साथी",
    "love": "माया"
}

word = input("Enter your sentence: ").lower()
output =""
for words in word.split(" "):
    if words in eng_to_nepali:
        output += eng_to_nepali[words]+ " "
    else:
        print("Word not found")
print(f"Nepali: {output}")
