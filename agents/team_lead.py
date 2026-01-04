from utils.data_manager import DataManager

class TeamLeadAgent:
    def __init__(self):
        self.data_manager = DataManager()

    def get_dashboard_data(self, date=None):
        """Aggregates data for the dashboard."""
        return {
            "active_cases": self.data_manager.get_active_cases(),
            "delta_log": self.data_manager.get_delta_log(date),
            "pending_actions": self.data_manager.get_pending_actions()
        }

    def handle_chat_input(self, user_input):
        """Processes user chat input."""
        # Simple echo/mock response for now
        return f"I received your message: '{user_input}'. I am the Team Lead Agent (Mock)."
