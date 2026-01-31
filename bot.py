"""
Slack Bot - Local Development Bot using Socket Mode
"""
import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.event("app_mention")
def handle_mention(event: dict, say):
    """Handle when the bot is mentioned in a channel"""
    user = event.get("user")
    text = event.get("text", "")
    logger.info(f"Bot mentioned by user {user}: {text}")
    say(f"Hello! You mentioned me. I received: {text}")


@app.message("hello")
def handle_hello(message: dict, say):
    """Respond to messages containing 'hello'"""
    user = message.get("user")
    logger.info(f"User {user} said hello")
    say(f"Hi there! <@{user}>")


@app.command("/echo")
def handle_echo_command(ack, respond, command):
    """Handle /echo slash command"""
    ack()  # Acknowledge the command request
    text = command.get("text", "")
    respond(f"Echo: {text}")


@app.event("message")
def handle_message_events(event: dict, say):
    """Handle all message events (optional - can be removed if too noisy)"""
    # Only respond to direct messages, not channel messages
    channel_type = event.get("channel_type")
    if channel_type == "im":
        text = event.get("text", "")
        logger.info(f"Received DM: {text}")
        say("I received your message! Type 'hello' or mention me to interact.")


def main():
    """Main function to start the bot"""
    bot_token = os.environ.get("SLACK_BOT_TOKEN")
    app_token = os.environ.get("SLACK_APP_TOKEN")
    
    if not bot_token:
        logger.error("SLACK_BOT_TOKEN not found in environment variables")
        raise ValueError("SLACK_BOT_TOKEN is required")
    
    if not app_token:
        logger.error("SLACK_APP_TOKEN not found in environment variables")
        raise ValueError("SLACK_APP_TOKEN is required")
    
    logger.info("Starting Slack bot in Socket Mode...")
    
    # Create Socket Mode handler
    handler = SocketModeHandler(app, app_token)
    
    # Start the handler
    handler.start()
    
    logger.info("Bot is running! Press Ctrl+C to stop.")


if __name__ == "__main__":
    main()
