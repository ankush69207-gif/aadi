import json
import os

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

def handle_memory_command(user_input, memory):
    """Checks for memory commands."""
    if user_input.lower().startswith("yaad rakho"):
        content = user_input[len("yaad rakho"):].strip()
        if content:
            return memory.remember(content)
        else:
            return "Kya yaad rakhna hai? Kuch batao toh sahi! 🙂"
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
    # Determine language/intent crudely
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
    # Extract message content if present
    return "Message taiyaar hai! Kisko bhejna hai? (Currently simulating send...) 📤"

def get_persona_response(user_input):
    """Fallback response logic based on keywords or general mood."""
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
        return "Achha? Aur batao? Main sun rahi hoon. 🙂"

def process_input(user_input, memory):
    if not user_input:
        return ""

    lower_input = user_input.lower()

    # Check specific commands
    mem_response = handle_memory_command(user_input, memory)
    if mem_response:
        return mem_response

    if "build website" in lower_input:
        return handle_website_guide()

    if "code do" in lower_input:
        return handle_code_request(user_input)

    if "send" in lower_input and len(lower_input) < 10: # simple check for just "send" command
        return handle_send_message(user_input)

    # Fallback to general persona chat
    return get_persona_response(user_input)

def main():
    print("Mental: Hello! ❤️ (Type 'exit' to leave)")
    memory = MentalMemory()

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
