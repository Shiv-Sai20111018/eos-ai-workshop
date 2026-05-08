import random
import time

print("=" * 50)
print("🤖 ShivBot AI Assistant")
print("Type 'bye' to exit")
print("=" * 50)

# Greetings
greetings = [
    "hello",
    "hi",
    "hey",
    "yo"
]

# Responses
hello_responses = [
    "Hey bro 👋",
    "Hello there 😎",
    "Yo 🔥",
    "Nice to meet you 🤖"
]

how_are_you_responses = [
    "I'm doing awesome 😎",
    "Running perfectly 🔥",
    "Feeling very intelligent today 🤖"
]

ai_responses = [
    "AI means Artificial Intelligence 🤖",
    "AI helps computers think and learn 🧠",
    "AI is used in chatbots, self-driving cars, and more 🚗"
]

jokes = [
    "Why did the AI go to school? To improve its neural network 😭",
    "I told my computer a joke... now it won't stop laughing 💀",
    "Python programmers don't die, they just stop responding 😎"
]

motivation = [
    "Keep learning bro 🔥",
    "Small steps every day = huge progress 🚀",
    "You are literally building AI projects 😭🔥"
]

# Chat memory
user_name = ""

# Typing effect
def bot_reply(message):
    print("Bot is typing...")
    time.sleep(1)
    print(f"Bot: {message}")

# Main chatbot loop
while True:

    user = input("You: ").lower().strip()

    # Exit
    if user == "bye":
        bot_reply("Goodbye bro 👋")
        break

    # Greetings
    elif user in greetings:
        bot_reply(random.choice(hello_responses))

    # Name storing
    elif "my name is" in user:
        user_name = user.replace("my name is", "").strip()
        bot_reply(f"Nice to meet you, {user_name} 😎")

    elif "what is my name" in user:

        if user_name:
            bot_reply(f"Your name is {user_name} 🔥")
        else:
            bot_reply("I don't know your name yet 😭")

    # How are you
    elif "how are you" in user:
        bot_reply(random.choice(how_are_you_responses))

    # AI questions
    elif "what is ai" in user:
        bot_reply(random.choice(ai_responses))

    elif "what is machine learning" in user:
        bot_reply(
            "Machine Learning helps computers learn from data without explicit programming 🧠"
        )

    elif "what is deep learning" in user:
        bot_reply(
            "Deep Learning uses neural networks with many layers 🤖"
        )

    elif "what is cnn" in user:
        bot_reply(
            "CNN is a neural network mainly used for image processing 🖼️"
        )

    elif "what is nlp" in user:
        bot_reply(
            "NLP helps computers understand human language 💬"
        )

    elif "what are transformers" in user:
        bot_reply(
            "Transformers are advanced AI models used in ChatGPT and modern NLP 🔥"
        )

    # Time
    elif "time" in user:
        current_time = time.strftime("%H:%M:%S")
        bot_reply(f"Current time is {current_time} ⏰")

    # Jokes
    elif "joke" in user:
        bot_reply(random.choice(jokes))

    # Motivation
    elif "motivate me" in user:
        bot_reply(random.choice(motivation))

    # Favorite things
    elif "favorite game" in user:
        bot_reply("Minecraft and AI simulators are awesome 😭🔥")

    elif "favorite language" in user:
        bot_reply("Python is my favorite because it is simple and powerful 🐍")

    # Creator
    elif "who made you" in user:
        bot_reply("Shiv Sai created me 😎🔥")

    # Unknown response
    else:
        bot_reply(
            "I don't understand that yet 😭 Try asking about AI, NLP, CNN, Transformers, or tell me a joke request."
        )
