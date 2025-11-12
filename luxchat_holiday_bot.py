import json
import re
from datetime import datetime
from matrix_client.client import MatrixClient

# Configuration
HOMESERVER_URL = "https://your-luxchat-homeserver.lu"  # Replace with your Luxchat server URL
BOT_USERNAME = "@bot_username:your-luxchat-homeserver.lu"  # Replace with bot username
BOT_PASSWORD = "your_bot_password"  # Replace with bot password
HOLIDAYS_FILE = "holidays.json"  # Path to your holidays.json file

class HolidayBot:
    def __init__(self, homeserver, username, password, holidays_file):
        self.client = MatrixClient(homeserver)
        self.username = username
        self.password = password
        self.holidays = self.load_holidays(holidays_file)
        
    def load_holidays(self, holidays_file):
        """Load holidays from JSON file"""
        try:
            with open(holidays_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {holidays_file} not found!")
            return {}
    
    def login(self):
        """Login to Matrix/Luxchat"""
        try:
            self.client.login_with_password(self.username, self.password)
            print(f"Logged in as {self.username}")
        except Exception as e:
            print(f"Login failed: {e}")
            return False
        return True
    
    def is_holiday(self, date_str):
        """Check if a specific date is a holiday"""
        try:
            # Normalize date format (try YYYY-MM-DD or DD-MM-YYYY)
            date_obj = None
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y', '%Y/%m/%d']:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            
            if not date_obj:
                return None, "Invalid date format. Please use YYYY-MM-DD or DD-MM-YYYY"
            
            date_key = date_obj.strftime('%Y-%m-%d')
            
            if date_key in self.holidays:
                return True, self.holidays[date_key]
            else:
                return False, None
        except Exception as e:
            return None, str(e)
    
    def get_year_holidays(self, year_str):
        """Get all holidays for a specific year"""
        try:
            year = int(year_str)
            year_holidays = {date: name for date, name in self.holidays.items() 
                           if date.startswith(str(year))}
            
            if not year_holidays:
                return "No holidays found for year " + year_str
            
            response = f"Luxembourg holidays for {year}:\n\n"
            for date, name in sorted(year_holidays.items()):
                response += f"• {date}: {name}\n"
            
            return response
        except ValueError:
            return "Invalid year format. Please provide a year (e.g., 2025)"
    
    def process_message(self, message_text):
        """Process incoming messages and return response"""
        message_lower = message_text.lower().strip()
        
        # Check if asking about a specific date
        date_patterns = [
            r'is\s+(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})\s+a\s+holiday',
            r'is\s+(\d{4}-\d{1,2}-\d{1,2})\s+a\s+holiday',
            r'(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})\s+holiday',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, message_lower)
            if match:
                date_str = match.group(1)
                is_hol, holiday_name = self.is_holiday(date_str)
                
                if is_hol is None:
                    return holiday_name
                elif is_hol:
                    return f"✓ Yes, {date_str} is a holiday: **{holiday_name}**"
                else:
                    return f"✗ No, {date_str} is not a public holiday in Luxembourg."
        
        # Check if asking for year holidays
        year_pattern = r'holidays?\s+(?:in\s+)?(?:for\s+)?(\d{4})|(\d{4})\s+holidays?'
        year_match = re.search(year_pattern, message_lower)
        if year_match:
            year = year_match.group(1) or year_match.group(2)
            return self.get_year_holidays(year)
        
        # Check for general help requests
        if 'help' in message_lower or 'holiday' in message_lower:
            return (
                "🇱🇺 **Luxembourg Holiday Bot**\n\n"
                "I can help you with Luxembourg holidays! Ask me:\n"
                "• Is 25-12-2025 a holiday?\n"
                "• Holidays in 2025\n"
                "• 2025 holidays\n\n"
                "Use dates in format: DD-MM-YYYY or YYYY-MM-DD"
            )
        
        return None
    
    def start(self):
        """Start the bot and listen for messages"""
        if not self.login():
            return
        
        self.client.add_listener(self.on_message)
        print("Bot is running. Press Ctrl+C to stop.")
        
        try:
            self.client.listen_forever()
        except KeyboardInterrupt:
            print("Bot stopped.")
    
    def on_message(self, room, event):
        """Handle incoming messages"""
        if event['type'] != 'm.room.message':
            return
        
        if event['content']['msgtype'] != 'm.text':
            return
        
        # Don't respond to own messages
        if event['sender'] == self.client.user_id:
            return
        
        message_text = event['content']['body']
        
        # Check if message mentions the bot or is a direct reply
        if self.client.user_id not in message_text and '@' not in message_text:
            return
        
        # Process the message
        response = self.process_message(message_text)
        
        if response:
            room.send_text(response)

# Main execution
if __name__ == "__main__":
    bot = HolidayBot(HOMESERVER_URL, BOT_USERNAME, BOT_PASSWORD, HOLIDAYS_FILE)
    bot.start()
