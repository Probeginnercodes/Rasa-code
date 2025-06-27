from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

# In-memory "DB"
db = {
    'users': {},
    'orders': {},
    'complaints': {}
}

class ActionRegisterUser(Action):
    def name(self):
        return "action_register_user"

    def run(self, dispatcher, tracker, domain):
        email = tracker.get_slot('email')
        user_id = f"u{len(db['users'])+1:04d}"
        db['users'][user_id] = email
        dispatcher.utter_message(text=f"🎉 You're registered! Your user ID is {user_id}.")
        return [SlotSet("user_id", user_id), FollowupAction("action_listen")]  # Added FollowupAction

class ActionListOrders(Action):
    def name(self):
        return "action_list_orders"

    def run(self, dispatcher, tracker, domain):
        uid = tracker.get_slot('user_id')
        orders = db['orders'].get(uid, [])
        dispatcher.utter_message(text=f"Here are your past orders: {orders}")
        return []

class ActionPlaceOrder(Action):
    def name(self):
        return "action_place_order"

    def run(self, dispatcher, tracker, domain):
        uid = tracker.get_slot('user_id')
        order = {"item": "phone", "price": 699}
        db['orders'].setdefault(uid, []).append(order)
        dispatcher.utter_message(text="Your order has been placed!")
        return []

class ActionCheckExisting(Action):
    def name(self):
        return "action_check_existing"

    def run(self, dispatcher, tracker, domain):
        uname = tracker.get_slot('username')
        exists = uname in db['complaints']
        return [SlotSet("complaint_exists", exists)]

class ActionHandleComplaint(Action):
    def name(self):
        return "action_handle_complaint"

    def run(self, dispatcher, tracker, domain):
        uname = tracker.get_slot('username')
        complaint = tracker.get_slot('complaint_text')
        tid = f"t{len(db['complaints'])+1:04d}"
        db['complaints'][uname] = {"complaint": complaint, "tracking_id": tid}
        dispatcher.utter_message(text=f"Your complaint's been logged! Tracking ID: {tid}.")
        return [SlotSet("tracking_id", tid)]

class ActionFetchByBudget(Action):
    def name(self):
        return "action_fetch_by_budget"

    def run(self, dispatcher, tracker, domain):
        try:
            budget = float(tracker.get_slot('budget'))
        except (TypeError, ValueError):
            dispatcher.utter_message(text="Please provide a valid budget amount.")
            return []

        # Phone database with realistic options
        phones = [
            {"name": "Samsung Galaxy A14", "price": 199, "currency": "€"},
            {"name": "Google Pixel 6a", "price": 349, "currency": "€"},
            {"name": "iPhone SE (2022)", "price": 429, "currency": "€"},
            {"name": "OnePlus Nord 3", "price": 499, "currency": "€"},
            {"name": "Samsung Galaxy A54", "price": 449, "currency": "€"},
            {"name": "Google Pixel 7", "price": 649, "currency": "€"},
            {"name": "iPhone 13", "price": 729, "currency": "€"},
            {"name": "Samsung Galaxy S23", "price": 899, "currency": "€"},
            {"name": "iPhone 14", "price": 929, "currency": "€"}
        ]

        # Filter phones within budget
        suggestions = [p for p in phones if p["price"] <= budget]
        
        if not suggestions:
            dispatcher.utter_message(text=f"Sorry, no phones found under {budget}€.")
            return []

        # Format suggestions
        suggestion_text = "\n".join(
            f"• {p['name']} — {p['currency']}{p['price']}" 
            for p in sorted(suggestions, key=lambda x: x["price"], reverse=True)[:3]  # Top 3
        )
        
        dispatcher.utter_message(
            text=f"Here are the best phones under {budget}€:\n{suggestion_text}\nWhich one interests you?"
        )
        return []

class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_default_fallback")
        return []