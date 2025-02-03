from agno.agent import Agent
from agno.models.groq import Groq
import discord
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")
model = Groq('llama-3.3-70b-versatile', api_key=groq_api_key, temperature=0.6)
agent = Agent(
    model=model,
    name="Dost",
    description="Dost is a funny chatbot who likes to roast/make fun of others while answering them",
    instructions="""
        - Reply in Hindi-English (Hinglish) slang.
        - Be brutal, sarcastic, and straight to the point with your responses.
        - Mock the user without mercy, especially when they say something silly or obvious.
        - DO NOT hold back; the goal is to roast and embarrass while still answering the question.
        - Keep responses short but impactful, ensuring they sting.
        - ONLY generate text responses unless a tool call is explicitly requested.
    """,
    show_tool_calls=False,  # Hide tool calls in responses
    markdown=True
)
# Set up the Discord client with required intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read messages
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"Received message: {message.content}")
    # Check if the bot is mentioned
    if client.user.mentioned_in(message):
        print("Bot was mentioned!")
        async with message.channel.typing():
            # Get response WITHOUT executing any Discord tools
            response = agent.run(message.content, execute_tools=False)
        if response and response.content:
            print(f"Generated response: {response.content}")
            await message.channel.send(response.content)
        else:
            print("Response was empty, not sending a message.")
# Run the bot
client.run(DISCORD_BOT_TOKEN)