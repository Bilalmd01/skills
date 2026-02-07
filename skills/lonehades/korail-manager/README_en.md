# Korail Manager Skill

Korail(KTX/SRT) reservation automation skill. It can search for trains, reserve tickets, and watch for available seats automatically.

## ⚠️ Important: Setup

For easy setup, run the included setup script. This will create the necessary virtual environment and install all dependencies for you.

```bash
bash scripts/setup.sh
```

This script only needs to be run once after installing or updating the skill.

<details>
<summary><strong>Manual Setup Steps</strong></summary>

If you prefer to set up the environment manually:

**1. Create a Virtual Environment:**
From the workspace root (`/home/ben/.openclaw/workspace`), run the following command to create a virtual environment inside the skill's directory:
```bash
python3 -m venv skills/korail-manager/venv
```

**2. Install Dependencies:**
Activate the environment and install the required packages from `requirements.txt`:
```bash
skills/korail-manager/venv/bin/pip install -r skills/korail-manager/requirements.txt
```
</details>

## Usage

All scripts **must** be run using the Python interpreter from the virtual environment created above.

### Search for Trains (`search.py`)
```bash
skills/korail-manager/venv/bin/python skills/korail-manager/scripts/search.py --dep "부산" --arr "서울" --date "20260208"
```

### Watch for Seats (`watch.py`)

This script will run in the background, check for available seats every `interval` seconds, and attempt to reserve one if found. It sends a Telegram notification on success.

**Arguments:**
- `--dep`: Departure station
- `--arr`: Arrival station
- `--date`: Date (YYYYMMDD)
- `--start-time`: Start hour of the time window to watch (e.g., 15 for 3 PM)
- `--end-time`: End hour of the time window (e.g., 17 for 5 PM)
- `--interval`: Check interval in seconds (default: 300)

**Example:**
```bash
skills/korail-manager/venv/bin/python skills/korail-manager/scripts/watch.py --dep "부산" --arr "서울" --date "20260208" --start-time 15 --end-time 17 --interval 300
```

### Cancel Reservation (`cancel.py`)
```bash
skills/korail-manager/venv/bin/python skills/korail-manager/scripts/cancel.py
```

## Environment Variables
This skill requires credentials for Korail login and notifications.
**These must be set for the skill to function correctly.**

The recommended way is to create a `.env` file in the skill's root directory (`skills/korail-manager/.env`).

1.  Copy the example file: `cp .env.example .env`
2.  Edit the new `.env` file and fill in your actual credentials.

```dotenv
# skills/korail-manager/.env
KORAIL_ID="YOUR_KORAIL_ID"
KORAIL_PW="YOUR_KORAIL_PASSWORD"
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"
SLACK_WEBHOOK_URL="YOUR_SLACK_WEBHOOK_URL" # Optional
```

⚠️ **Warning:** The `.env` file is listed in `.gitignore` and will not be committed to your repository. However, it contains sensitive credentials. **Do not share this file publicly or commit it to version control.**

The scripts will automatically load these variables when run.

<details>
<summary><strong>How to get Telegram Token and Chat ID?</strong></summary>

**1. Find your Bot Token:**
   - In Telegram, search for the `@BotFather` bot.
   - Send the `/mybots` command.
   - Select your bot from the list.
   - Click the **API Token** button to view your token.

**2. Find your Chat ID:**
   - In Telegram, search for the `@userinfobot`.
   - Start a chat with it.
   - The bot will immediately reply with your user information, including your **Id**. This number is your Chat ID.

</details>

<details>
<summary><strong>How to get a Slack Webhook URL?</strong></summary>

1.  **Go to Slack Apps:** Navigate to `https://api.slack.com/apps`.
2.  **Create or Select an App:** Click "Create New App" (or select an existing app you want to use for notifications).
    *   Choose "From scratch", give it a name (e.g., "Korail Alerts"), and select your workspace.
3.  **Enable Incoming Webhooks:** In the left sidebar under "Add features and functionality", click "Incoming Webhooks" and turn the feature **On**.
4.  **Add Webhook to Workspace:** Click the "Add New Webhook to Workspace" button at the bottom of the page.
5.  **Select Channel:** Choose the channel where you want to receive alerts and click "Allow".
6.  **Copy URL:** A new Webhook URL (starting with `https://hooks.slack.com/...`) will appear in the list. Copy this URL.
7.  **Set Environment Variable:** Use this copied URL for the `SLACK_WEBHOOK_URL` environment variable.

</details>

After adding these lines, restart your terminal or run `source ~/.bashrc` (or `source ~/.zshrc`) to apply the changes.

## Security & Privacy
This skill makes outbound network calls to:
1. **Korail (letskorail.com):** To search and reserve tickets.
2. **Telegram API:** To send reservation alerts (if configured).
3. **Slack Webhook:** To send reservation alerts (if configured).

Credentials are ONLY read from environment variables and are NOT stored or transmitted elsewhere.
