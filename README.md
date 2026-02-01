# Slack Bot - Local Development

A simple Slack bot that runs locally using Python and Socket Mode, perfect for free Slack workspaces.

## Features

- Runs locally without needing a public endpoint
- Uses Socket Mode for real-time communication
- Responds to mentions, messages, and slash commands
- **AI-powered question answering** using OpenAI API
- Returns current date and time when mentioned
- Easy to extend with custom functionality

## Prerequisites

- Python 3.8 or higher
- A Slack workspace (free tier works)
- A Slack app created in your workspace
- (Optional) OpenAI API key for AI question answering - Get one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

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
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```
   
   **Note**: The `OPENAI_API_KEY` is optional. If not provided, the bot will still work but won't be able to answer questions with AI.

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

- **Ask a question (with AI)**: 
  - Mention the bot: `@YourBotName What is Python?` - The bot will answer using AI
  - Or send a direct message with your question
- **Get date/time**: `@YourBotName` (without a question) - The bot will respond with the current date and time
- **Say hello**: Send a message containing "hello" in a DM or channel
- **Use slash command**: Type `/echo your message` - The bot will echo your message

**Important**: 
- Make sure to invite the bot to the channel first using `/invite @YourBotName`
- For AI question answering, make sure you've set `OPENAI_API_KEY` in your `.env` file

## Customization

Edit `bot.py` to add your own functionality:

- Add new event handlers with `@app.event("event_name")`
- Add new message handlers with `@app.message("pattern")`
- Add new slash commands with `@app.command("/command")`
- Add interactive components with `@app.action("action_id")`

## Troubleshooting

- **"SLACK_BOT_TOKEN not found"**: Make sure your `.env` file exists and contains the correct token
- **"SLACK_APP_TOKEN not found"**: Make sure Socket Mode is enabled and you've created an app-level token
- **Bot connects but doesn't respond**:
  1. **Invite the bot to the channel**: In Slack, type `/invite @YourBotName` in the channel where you want to use it
  2. **Check Event Subscriptions**: Go to your app settings → Event Subscriptions → Make sure "Enable Events" is ON
  3. **Subscribe to bot events**: Under "Subscribe to bot events", add:
     - `app_mentions` (to respond when mentioned)
     - `message.channels` (to read channel messages)
     - `message.im` (to read direct messages)
  4. **Check bot scopes**: Ensure you have `app_mentions:read`, `chat:write`, and `channels:history` scopes
  5. **Restart the bot**: After changing app settings, restart your bot (`Ctrl+C` and run `python3 bot.py` again)
  6. **Check logs**: The bot logs all events - look for "Bot mentioned" messages in the terminal
- **Connection issues**: Verify both tokens are correct and Socket Mode is enabled in your app settings

## Resources

- [Slack Bolt for Python Documentation](https://slack.dev/bolt-python/)
- [Socket Mode Guide](https://api.slack.com/apis/connections/socket)
- [Slack API Documentation](https://api.slack.com/)
