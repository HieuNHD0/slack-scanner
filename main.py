import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Set the Slack API token
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

# Define the set of keywords to search for
keywords = ["keyword1", "keyword2", "keyword3"]

# Define the time period during which to scan the channels
start_time = time.time() - 3600  # Scan the past hour

# Initialize the results dictionary
results = {}

# Get a list of all channels in the workspace
try:
    channels = client.conversations_list().get("channels")
except SlackApiError as e:
    print("Error getting channel list: {}".format(e))

# Loop through each channel and retrieve its message history
for channel in channels:
    try:
        history = client.conversations_history(channel=channel["id"]).get("messages")
    except SlackApiError as e:
        print("Error getting history for channel {}: {}".format(channel["name"], e))
        continue

    # Loop through each message in the channel's history
    for message in history:
        # Check if the message contains any of the keywords
        if any(keyword in message["text"] for keyword in keywords):
            # Check if the message was sent during the time period we are scanning
            if float(message["ts"]) >= start_time:
                # Add the channel and message to the results dictionary
                if channel["name"] not in results:
                    results[channel["name"]] = []
                results[channel["name"]].append(message["text"])

# Print the results of the scan
if len(results) == 0:
    print("No channels contain the set of keywords.")
else:
    for channel, messages in results.items():
        print("Channel {}: {}".format(channel, messages))
