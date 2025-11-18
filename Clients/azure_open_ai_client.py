import os

from openai import AzureOpenAI
from dotenv import load_dotenv
from openai import OpenAI
env_file = ".env"

# Load environment variables from .env file
load_dotenv(env_file)
azure_oai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OPENAI_API_KEY")
# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version="2024-02-15-preview"
)
