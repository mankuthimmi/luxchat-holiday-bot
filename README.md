# Luxchat Holiday Bot

A Python bot for Luxchat (Matrix protocol) that answers questions about Luxembourg public holidays.

## Features

- ✅ Check if a specific date is a holiday
- ✅ Get list of all holidays for a given year
- ✅ Responds to user queries in Luxchat rooms
- ✅ Supports multiple date formats (DD-MM-YYYY, YYYY-MM-DD)

## Prerequisites

- Python 3.7 or higher
- A Luxchat account with bot credentials
- Internet connection (to fetch live government holiday data)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/mankuthimmi/luxchat-holiday-bot.git
cd luxchat-holiday-bot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Bot Credentials
Edit `luxchat_holiday_bot.py` and update these lines with your Luxchat details:

```python
HOMESERVER_URL = "https://your-luxchat-homeserver.lu"  # Your Luxchat server URL
BOT_USERNAME = "@bot_username:your-luxchat-homeserver.lu"  # Bot username
BOT_PASSWORD = "your_bot_password"  # Bot password
```

### Step 4: Run the Bot
```bash
python luxchat_holiday_bot.py
```

The bot will login and start listening for messages. Holiday data is automatically fetched from the official Luxembourg government database.

## Usage

In your Luxchat room, ask the bot questions like:

### Check if a Date is a Holiday
- "Is 25-12-2025 a holiday?"
- "Is 2025-12-25 a holiday?"
- "25.12.2025 holiday?"

**Bot responds:** ✓ Yes, 25-12-2025 is a holiday: **Christmas Day**

### Get Holidays for a Year
- "Holidays in 2025"
- "Show me 2025 holidays"
- "2025 holidays"

**Bot responds:** Lists all Luxembourg public holidays for 2025

### Get Help
- "help"
- "holiday"

**Bot responds:** Shows usage instructions

## Date Formats Supported

- `YYYY-MM-DD` (e.g., 2025-12-25)
- `DD-MM-YYYY` (e.g., 25-12-2025)
- `DD.MM.YYYY` (e.g., 25.12.2025)

## Project Structure

```
luxchat-holiday-bot/
├── luxchat_holiday_bot.py    # Main bot script
├── requirements.txt           # Python dependencies
├── holidays.json              # Luxembourg holidays data
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```

## Data Source

This bot uses the **python-holidays library** which automatically provides:
- ✅ Official Luxembourg public holidays
- ✅ Automatically updated annually
- ✅ Connected to government holiday database
- ✅ No manual updates needed

The holiday data is maintained by the python-holidays community and reflects the official Luxembourg government holidays published at [luxembourg.public.lu](https://luxembourg.public.lu/en/vivre/quality-of-life/jours-feries-legaux.html)

## Troubleshooting

### Authentication Error
- Verify your Luxchat credentials
- Check if your bot account has the correct permissions
- Ensure `HOMESERVER_URL` is correct

### "No module named 'holidays'" Error
- Install the holidays library: `pip install holidays`
- Or reinstall dependencies: `pip install -r requirements.txt`

### Bot Not Responding
- Check that the bot is running (no errors in console)
- Make sure you mention the bot or it's a direct message
- Verify the bot has permissions to send messages in the room
- Check your internet connection (needed to fetch holiday data)

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please open an issue on GitHub.