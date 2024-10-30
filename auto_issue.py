import requests
import re
import time

# GitHub API setup
repo = "Synthetic-CortexLabs/SpeakWise"
token = ""  # Replace with your generated token
headers = {"Authorization": f"token {token}"}

# Function to get existing labels
def get_existing_labels():
    response = requests.get(f"https://api.github.com/repos/{repo}/labels", headers=headers)
    if response.status_code == 200:
        return {label["name"] for label in response.json()}
    else:
        print("Error fetching labels:", response.json())
        return set()

# Function to create a new label if it doesn't exist
def create_label(label_name):
    if label_name in existing_labels:
        print(f"Label '{label_name}' already exists.")
        return  # Skip creation if label already exists

    data = {"name": label_name, "color": "d4c5f9"}  # Default color, can be customized
    response = requests.post(f"https://api.github.com/repos/{repo}/labels", headers=headers, json=data)
    if response.status_code == 201:
        print(f"Label '{label_name}' created.")
        existing_labels.add(label_name)  # Add to set to prevent re-creation in the future
    else:
        print(f"Failed to create label '{label_name}':", response.json())

# Fetch existing labels in the repo
existing_labels = get_existing_labels()

# Open and read issues.md file
with open("issues.md", "r") as file:
    content = file.read()

# Regular expression to match each issue's details
issues = re.findall(r"### \*\*Issue \d+: (.*?)\*\*\n\n- \*\*Description\*\*:([\s\S]*?)- \*\*Label\*\*: (.*?)\n- \*\*Time Frame\*\*: (.*?)\n\n---", content)

for title, description, labels, time_frame in issues:
    labels_list = [label.strip() for label in labels.split(",")]

    # Check for missing labels and create them if necessary
    for label in labels_list:
        create_label(label)

    # Create GitHub issue
    data = {
        "title": title,
        "body": f"{description}\n\n**Estimated Time Frame**: {time_frame}",
        "labels": labels_list
    }
    response = requests.post(f"https://api.github.com/repos/{repo}/issues", headers=headers, json=data)

    if response.status_code == 201:
        print(f"Issue '{title}' created successfully.")
    else:
        print(f"Failed to create issue '{title}'. Error:", response.json())

    time.sleep(5)  # Adding a 5-second delay between each issue creation request
