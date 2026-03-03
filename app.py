# Updated content to fix truncated strings and syntax errors for Render deployment.

# Import necessary libraries
import json
import os

# Define a function to load configuration

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# Main execution
if __name__ == '__main__':
    config = load_config()
    print(f"Configuration loaded: {config}")
