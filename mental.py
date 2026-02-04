import json
import os
import sys

# Try to import Gemini library
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

MEMORY_FILE = "memory.json"

class MentalMemory:
    def __init__(self):
        self.data = self._load_memory()

    def _load_memory(self):
        if not os.path.exists(MEMORY_FILE):
            return {}
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_memory(self):
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def remember(self, text):
        """Stores a fact/note."""
        if "notes" not in self.data:
            self.data["notes"] = []
        self.data["notes"].append(text)
        self.save_memory()
        return "Theek hai, yaad rakhungi! ❤️ Notes mein save kar liya."

    def get_notes(self):
        return self.data.get("notes", [])

    def set_api_key(self, key):
        self.data["api_key"] = key
        self.save_memory()
        return "Brain connect ho gaya! 🧠 Ab main smart hoon."

    def get_api_key(self):
        return self.data.get("api_key")

def handle_memory_command(user_input, memory):
    """Checks for memory commands."""
    if user_input.lower().startswith("yaad rakho"):
        content = user_input[len("yaad rakho"):].strip()
        if content:
            return memory.remember(content)
        else:
            return "Kya yaad rakhna hai? Kuch batao toh sahi! 🙂"
    return None

def handle_api_setup(user_input, memory):
    if user_input.lower().startswith("set api"):
        key = user_input[len("set api"):].strip()
        if key:
            return memory.set_api_key(key)
        else:
            return "API Key toh do! (Usage: 'Set API <YOUR_KEY>') 🔑"
    return None

def handle_website_guide():
    steps = [
        "Chalo website banate hain! 🚀",
        "Step 1: Folder structure banao (index.html, style.css, script.js).",
        "Step 2: HTML mein basic skeleton likho (`<html>`, `<body>`).",
        "Step 3: Content add karo - Headings, paragraphs, aur images.",
        "Step 4: CSS se styling karo taaki sundar dikhe 🎨.",
        "Step 5: JS add karo agar interactivity chahiye.",
        "Kaunsa step samjhau detail mein? 🙂"
    ]
    return "\n".join(steps)

def handle_code_request(user_input):
    lower_input = user_input.lower()
    if "html" in lower_input:
        return """Ye lo HTML ka basic code! ❤️
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Hello World! 🌍</h1>
    <p>Welcome to my page.</p>
</body>
</html>
```
Try karo aur batao kaisa laga!"""
    elif "python" in lower_input:
        return """Python code chahiye? Ye lo simple example:
```python
def hello():
    print("Hello from Python! 🐍")

if __name__ == "__main__":
    hello()
```
Run karke dekhna!"""
    else:
        return """Kaunsi language mein code chahiye? HTML, Python, JS? Batao na! 💻"""

def handle_send_message(user_input):
    return "Message taiyaar hai! Kisko bhejna hai? (Currently simulating send...) 📤"

def get_ai_response(user_input, api_key):
    """Uses Google Gemini API if available."""
    if not HAS_GENAI:
        return "Mere paas 'Brain' (google-generativeai library) install nahi hai. `pip install google-generativeai` run karo! 🧠"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        # Persona prompt
        prompt = f"You are Mental, a caring, supportive girlfriend-style assistant. Speak in Hinglish. Keep it warm and helpful. User says: {user_input}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Oof, brain freeze! 🤕 (API Error: {str(e)})"

def get_persona_response(user_input, memory):
    """Smart response logic."""
    api_key = memory.get_api_key()

    # If API key is present, try to use it for general chat
    if api_key:
        return get_ai_response(user_input, api_key)

    # Fallback to basic logic
    lower = user_input.lower()

    if "sad" in lower or "upset" in lower or "tired" in lower:
        return "Aww, kya hua? 😔 Take a break, pani piyo. Main hoon na yahan. ❤️"
    elif "hello" in lower or "hi" in lower:
        return "Hello ji! Kaise ho aap? Aaj kya naya seekhenge? ✨"
    elif "thank" in lower:
        return "You're welcome! Hamesha aapke saath. 🤗"
    elif "bye" in lower:
        return "Bye! Jaldi aana wapas. Miss karungi! 👋"
    else:
        return "Achha? Aur batao? (Tip: 'Set API <KEY>' to make me smarter!) 🙂"

def process_input(user_input, memory):
    if not user_input:
        return ""

    lower_input = user_input.lower()

    # Check specific commands
    mem_response = handle_memory_command(user_input, memory)
    if mem_response:
        return mem_response

    api_response = handle_api_setup(user_input, memory)
    if api_response:
        return api_response

    if "build website" in lower_input:
        return handle_website_guide()

    if "code do" in lower_input:
        return handle_code_request(user_input)

    if "send" in lower_input and len(lower_input) < 10:
        return handle_send_message(user_input)

    # Fallback/Smart chat
    return get_persona_response(user_input, memory)

def main():
    print("Mental: Hello! ❤️ (Type 'exit' to leave)")
    if not HAS_GENAI:
        print("(Tip: Install 'google-generativeai' for smart mode!)")

    memory = MentalMemory()
    if not memory.get_api_key():
        print("(Running in Basic Mode. Use 'Set API <KEY>' to unlock brain.)")

    while True:
        try:
            user_input = input("You: ").strip()
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Mental: Bye! Jaldi aana wapas. Miss karungi! 👋")
            break

        if not user_input:
            continue

        response = process_input(user_input, memory)
        print(f"Mental: {response}")

if __name__ == "__main__":
    main()
