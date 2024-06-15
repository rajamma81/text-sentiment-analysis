import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

# Azure Blob Storage credentials
blob_connection_string = "DefaultEndpointsProtocol=https;AccountName=rey;AccountKey=tPmKy5LG15Ysqifl8vHr4bNydpLed1JMt8PclUGwuMJqXVfmo9uU2pbRWF8gYKZaoMxP0V+QtQkA+AStqqyy4A==;EndpointSuffix=core.windows.net"
blob_connection_key="tPmKy5LG15Ysqifl8vHr4bNydpLed1JMt8PclUGwuMJqXVfmo9uU2pbRWF8gYKZaoMxP0V+QtQkA+AStqqyy4A=="
container_name = "blobtext"
input_blob_name = "analysis.txt"
output_blob_name = "analysis. txt"

# Azure Cognitive Services - Text Analytics credentials
text_analytics_endpoint = "https://loction.cognitiveservices.azure.com/"
text_analytics_key = "ecc51283dfab4ab7a297a0e5a5ae28d4"

def analyze_sentiment(blob_data):
    text_analytics_client = TextAnalyticsClient(endpoint=text_analytics_endpoint, credential=AzureKeyCredential(text_analytics_key))
    # Convert blob content to string
    text = blob_data.decode('utf-8', errors='ignore')
    # Analyze sentiment of the text
    sentiment_analysis = text_analytics_client.analyze_sentiment([text])
    return sentiment_analysis[0].sentiment, sentiment_analysis[0].confidence_scores

try:
    # Initialize Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Get input blob content
    input_blob_client = container_client.get_blob_client(input_blob_name)
    input_blob_data = input_blob_client.download_blob().readall()

    # Analyze sentiment
    sentiment, confidence_scores = analyze_sentiment(input_blob_data)

    # Upload sentiment analysis result to output blob
    output_blob_client = container_client.get_blob_client(output_blob_name)
    output_blob_client.upload_blob(f"Sentiment: {sentiment}, Confidence Scores: {confidence_scores}")

    print("Sentiment analysis completed and results uploaded successfully.")
except ResourceNotFoundError:
    print("Blob not found.")
except HttpResponseError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")