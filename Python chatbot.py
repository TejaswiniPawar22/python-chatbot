import nltk
from datetime import datetime
import random
import webbrowser
import re

# Download the necessary nltk data
nltk.download('punkt')

class MultiPurposeChatbot:
    def __init__(self):
        self.greetings = ["hello", "hi", "hey", "hola", "greetings", "what's up"]
        self.time_queries = ["time", "clock", "hour"]
        self.jokes = ["joke", "funny", "laugh"]
        self.search_queries = ["search", "google", "find"]
        self.currency_queries = ["convert", "currency", "exchange rate", "conversion"]
        self.game_queries = ["game", "play", "guess"]

        # Example currency conversion rates (as of a specific date)
        self.conversion_rates = {
            'usd_to_eur': 0.85,
            'eur_to_usd': 1.18,
            'usd_to_inr': 74.15,
            'inr_to_usd': 0.0135
        }

    def handle_greeting(self):
        return random.choice(["Hello!", "Hi there!", "Hey!", "Greetings!"])

    def handle_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return f"The current time is {current_time}"

    def handle_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
        ]
        return random.choice(jokes)

    def handle_search(self, query):
        search_query = query.replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        return f"Searching for '{search_query}' on Google..."

    def handle_currency_conversion(self, query):
        tokens = nltk.word_tokenize(query.lower())
        
        try:
            # Find the amount, from_currency, and to_currency in the tokens
            amount = float(tokens[1])
            from_currency = tokens[2].upper()
            to_currency = tokens[-1].upper()  # Use the last token as to_currency

            # Create the conversion key
            conversion_key = f'{from_currency.lower()}_to_{to_currency.lower()}'
            
            # Perform the conversion if the key exists
            if conversion_key in self.conversion_rates:
                rate = self.conversion_rates[conversion_key]
                converted_amount = amount * rate
                return f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}"
            else:
                return "Sorry, I can't convert between those currencies."
        except (IndexError, ValueError):
            return "Please provide the conversion in the format: 'convert [amount] [from_currency] to [to_currency]'."

    def handle_game(self):
        number = random.randint(1, 10)
        attempts = 3

        while attempts > 0:
            guess = input("Guess a number between 1 and 10: ")

            try:
                guess = int(guess)
            except ValueError:
                print("Please enter a valid number.")
                continue

            if guess == number:
                return "Congratulations! You guessed the correct number!"
            elif guess < number:
                print("Too low! Try again.")
            else:
                print("Too high! Try again.")

            attempts -= 1

        return f"Sorry, you're out of attempts. The correct number was {number}."

    def get_response(self, user_input):
        tokens = nltk.word_tokenize(user_input.lower())
        
        if any(word in tokens for word in self.greetings):
            return self.handle_greeting()
        
        elif any(word in tokens for word in self.time_queries):
            return self.handle_time()

        elif any(word in tokens for word in self.jokes):
            return self.handle_joke()

        elif any(word in tokens for word in self.search_queries):
            return self.handle_search(user_input)

        elif any(word in tokens for word in self.currency_queries):
            return self.handle_currency_conversion(user_input)
        
        elif any(word in tokens for word in self.game_queries):
            return self.handle_game()

        '''else:
            return "I'm not sure how to respond to that. Could you ask something else?"'''

# Instantiate the chatbot
bot = MultiPurposeChatbot()

# Main loop
while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "bye", "quit"]:
        print("Chatbot: Goodbye!")
        break
    
    response = bot.get_response(user_input)
    print(f"Chatbot: {response}")
