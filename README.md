# Slack Bot - Local Development

A simple Slack bot that runs locally using Python and Socket Mode, perfect for free Slack workspaces.

## Features

- Runs locally without needing a public endpoint
- Uses Socket Mode for real-time communication
- Responds to mentions, messages, and slash commands
- Easy to extend with custom functionality

## Prerequisites

- Python 3.8 or higher
- A Slack workspace (free tier works)
- A Slack app created in your workspace

## Setup Instructions

### 1. Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Give your app a name (e.g., "My Local Bot") and select your workspace
4. Click "Create App"

### 2. Enable Socket Mode

1. In your app settings, go to **Socket Mode** (under "Settings" in the left sidebar)
2. Toggle "Enable Socket Mode" to ON
3. Click "Generate Token" under "App-Level Tokens"
4. Give it a name (e.g., "socket-mode-token") and add the `connections:write` scope
5. Copy the generated token (starts with `xapp-`) - this is your `SLACK_APP_TOKEN`

### 3. Configure Bot Token Scopes

1. Go to **OAuth & Permissions** (under "Features" in the left sidebar)
2. Scroll down to "Scopes" → "Bot Token Scopes"
3. Add the following scopes:
   - `app_mentions:read` - To respond when mentioned
   - `chat:write` - To send messages
   - `commands` - To handle slash commands
   - `im:read` - To read direct messages
   - `im:write` - To send direct messages
   - `channels:history` - To read channel messages (optional)
   - `groups:history` - To read private channel messages (optional)

### 4. Install the Bot to Your Workspace

1. Still in **OAuth & Permissions**, scroll to the top
2. Click "Install to Workspace"
3. Review the permissions and click "Allow"
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`) - this is your `SLACK_BOT_TOKEN`

### 5. Set Up the Project

1. Clone or navigate to this project directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and add your tokens:
   ```
   SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
   SLACK_APP_TOKEN=xapp-your-actual-app-token
   ```

### 6. Run the Bot

```bash
python bot.py
```

You should see:
```
INFO:__main__:Starting Slack bot in Socket Mode...
INFO:__main__:Bot is running! Press Ctrl+C to stop.
```

## Usage

Once the bot is running, you can interact with it in Slack:

- **Mention the bot**: `@YourBotName hello` - The bot will respond
- **Say hello**: Send a message containing "hello" in a DM or channel
- **Use slash command**: Type `/echo your message` - The bot will echo your message

## Customization

Edit `bot.py` to add your own functionality:

- Add new event handlers with `@app.event("event_name")`
- Add new message handlers with `@app.message("pattern")`
- Add new slash commands with `@app.command("/command")`
- Add interactive components with `@app.action("action_id")`

## Troubleshooting

- **"SLACK_BOT_TOKEN not found"**: Make sure your `.env` file exists and contains the correct token
- **"SLACK_APP_TOKEN not found"**: Make sure Socket Mode is enabled and you've created an app-level token
- **Bot doesn't respond**: Check that you've installed the bot to your workspace and added the required scopes
- **Connection issues**: Verify both tokens are correct and Socket Mode is enabled in your app settings

## Resources

- [Slack Bolt for Python Documentation](https://slack.dev/bolt-python/)
- [Socket Mode Guide](https://api.slack.com/apis/connections/socket)
- [Slack API Documentation](https://api.slack.com/)
