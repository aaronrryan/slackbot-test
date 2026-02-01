"""
Slack Bot - Local Development Bot using Socket Mode
"""
import os
import ssl
import logging
import re
from datetime import datetime
from dotenv import load_dotenv
import certifi
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from openai import OpenAI

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

# Initialize OpenAI client
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_client = None
if openai_api_key:
    openai_client = OpenAI(api_key=openai_api_key)
    logger.info("OpenAI client initialized")
else:
    logger.warning("OPENAI_API_KEY not found - AI question answering will be disabled")


# Debug handler to log all events (helpful for troubleshooting)
@app.event({"type": ".*"})
def handle_all_events(event: dict, logger):
    """Log all events for debugging"""
    event_type = event.get("type")
    if event_type not in ["message", "app_mention"]:  # Only log non-message events to reduce noise
        logger.info(f"Received event: {event_type} - {event}")


@app.event("app_mention")
def handle_mention(event: dict, say):
    """Handle when the bot is mentioned in a channel - can answer questions or return date/time"""
    user = event.get("user")
    channel = event.get("channel")
    text = event.get("text", "")
    
    # Remove bot mention from text to get the actual question
    # Bot mentions are in format <@USER_ID>
    question = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    
    logger.info(f"Bot mentioned by user {user} in channel {channel}: {text}")
    logger.info(f"Extracted question: {question}")
    
    # If there's a question and OpenAI is configured, answer it
    if question and openai_client:
        try:
            logger.info(f"Processing question with OpenAI: {question}")
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant in a Slack workspace. Provide concise, clear answers."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            say(f"{answer}")
            logger.info("Successfully sent AI response")
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            say("Sorry, I encountered an error while processing your question. Please try again.")
    else:
        # Default: return current date and time
        now = datetime.now()
        current_date = now.strftime("%A, %B %d, %Y")
        current_time = now.strftime("%I:%M:%S %p")
        
        if not openai_client:
            say(f"Current date: {current_date}\nCurrent time: {current_time}\n\n*Note: OpenAI API key not configured. Ask me a question after setting OPENAI_API_KEY in your .env file.*")
        else:
            say(f"Current date: {current_date}\nCurrent time: {current_time}\n\n*Ask me a question to get an AI-powered answer!*")


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
    """Handle direct messages - answer questions with AI"""
    # Skip bot messages and messages in channels (only handle DMs)
    channel_type = event.get("channel_type")
    subtype = event.get("subtype")
    
    # Skip bot messages and message subtypes
    if subtype:
        logger.debug(f"Skipping message with subtype: {subtype}")
        return
    
    # Only respond to direct messages
    if channel_type == "im":
        text = event.get("text", "").strip()
        user = event.get("user")
        logger.info(f"Received DM from user {user}: {text}")
        
        # If OpenAI is configured and there's a question, answer it
        if text and openai_client:
            try:
                logger.info(f"Processing DM question with OpenAI: {text}")
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant in a Slack workspace. Provide concise, clear answers."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
                say(f"{answer}")
                logger.info("Successfully sent AI response to DM")
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {e}")
                say("Sorry, I encountered an error while processing your question. Please try again.")
        else:
            if not openai_client:
                say("I received your message! However, OpenAI API key is not configured. Set OPENAI_API_KEY in your .env file to enable AI question answering.\n\nYou can also mention me in a channel to get the current date and time.")
            else:
                say("Ask me a question and I'll answer it using AI! Or mention me in a channel to get the current date and time.")


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
