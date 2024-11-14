from tools import search_products

class ShoppingAssistant:
    def handle_input(self, user_input):
        if "search" in user_input:
            product_name = user_input.split("search")[-1].strip()
            return search_products(description=product_name)
        return "Sorry, I didn't understand that. Could you rephrase?"
