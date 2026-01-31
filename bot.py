"""
Slack Bot - Local Development Bot using Socket Mode
"""
import os
import ssl
import logging
from datetime import datetime
from dotenv import load_dotenv
import certifi
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create SSL context with certifi certificates (fixes macOS SSL issues)
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Create WebClient with SSL context
client = WebClient(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    ssl=ssl_context
)

# Initialize the Slack app with the configured client
app = App(client=client)


# Debug handler to log all events (helpful for troubleshooting)
@app.event({"type": ".*"})
def handle_all_events(event: dict, logger):
    """Log all events for debugging"""
    event_type = event.get("type")
    if event_type not in ["message", "app_mention"]:  # Only log non-message events to reduce noise
        logger.info(f"Received event: {event_type} - {event}")


@app.event("app_mention")
def handle_mention(event: dict, say):
    """Handle when the bot is mentioned in a channel - returns current date and time"""
    user = event.get("user")
    channel = event.get("channel")
    text = event.get("text", "")
    logger.info(f"Bot mentioned by user {user} in channel {channel}: {text}")
    
    # Get current date and time
    now = datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    current_time = now.strftime("%I:%M:%S %p")
    
    try:
        say(f"Current date: {current_date}\nCurrent time: {current_time}")
        logger.info("Successfully sent date/time response")
    except Exception as e:
        logger.error(f"Error sending response: {e}")


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
    """Handle all message events - logs for debugging"""
    # Skip bot messages and messages in channels (only handle DMs)
    channel_type = event.get("channel_type")
    subtype = event.get("subtype")
    
    # Skip bot messages and message subtypes
    if subtype:
        logger.debug(f"Skipping message with subtype: {subtype}")
        return
    
    # Only respond to direct messages
    if channel_type == "im":
        text = event.get("text", "")
        user = event.get("user")
        logger.info(f"Received DM from user {user}: {text}")
        say("I received your message! Mention me in a channel to get the current date and time.")


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
