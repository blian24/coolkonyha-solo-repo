import pandas as pd
from datetime import datetime, timedelta

class DataManager:
    def __init__(self):
        # Mock Data for Initial Setup
        self.mock_cases = [
            {"Client": "Alpha Corp", "Contact": "John Doe", "Status": "3. Árajánlat Készítés", "Last Update": "2023-10-26", "Next Step": "Send Quote"},
            {"Client": "Beta Ltd", "Contact": "Jane Smith", "Status": "5. Szállítás / Várakozás", "Last Update": "2023-10-25", "Next Step": "Track Shipment"},
            {"Client": "Gamma Inc", "Contact": "Bob Jones", "Status": "1. Beérkező Érdeklődés", "Last Update": "2023-10-27", "Next Step": "Identify Needs"},
        ]
        
        # Dynamic mock dates relative to today
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        day_before = today - timedelta(days=2)
        
        self.mock_delta_log = {
            str(today): [
                "New email from Gamma Inc regarding 'Product X inquiry'",
                "Shipment for Beta Ltd delayed by 1 day"
            ],
            str(yesterday): [
                "Alpha Corp requested quote revision",
                "Sent invoice to Delta Co"
            ],
            str(day_before): [
                "System maintenance completed",
                "Backup successful"
            ]
        }
        
        self.mock_actions = [
            {"id": 1, "task": "Approve Quote for Alpha Corp", "type": "approval"},
            {"id": 2, "task": "Review new lead: Gamma Inc", "type": "review"}
        ]

    def get_active_cases(self):
        """Returns a pandas DataFrame of active cases."""
        return pd.DataFrame(self.mock_cases)

    def get_delta_log(self, date=None):
        """Returns a list of recent events for a specific date."""
        if date is None:
            date = datetime.now().date()
        
        date_str = str(date)
        return self.mock_delta_log.get(date_str, ["No events recorded for this day."])

    def get_pending_actions(self):
        """Returns a list of pending actions."""
        return self.mock_actions
