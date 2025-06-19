import time

class UserInterface:
    def __init__(self):
        pass

    def display_suggestions(self, suggestions, latency, confidence_scores):
        if not suggestions:
            print("No suggestions available.")
            return

        print("Top 3 Suggestions:")
        for i, suggestion in enumerate(suggestions[:3]):
            print(f"- {suggestion} (Confidence: {confidence_scores[i]:.2f})")

        print(f"Latency: {latency:.2f} ms")

    def get_user_input(self):
        while True:
            prefix = input("Type a prefix: ")
            start_time = time.time()
            yield prefix, start_time