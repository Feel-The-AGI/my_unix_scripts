#!/bin/bash

ACCESS_TOKEN=""
# GitHub username
GITHUB_USERNAME="Feel-The-AGI"

# Navigate to the directory containing all your repos
cd /home/trainora/Desktop/repo || exit

# List of your repository names
repos=(
    "AI-Foundations"
    "alina-gpt-3.5-turbo-bot"
    "AI_Engineering_Roadmap_2024"
    "nlp_for_beginners"
    "AIrticle"
    "semblance_halo"
    "Discord-bot-js"
    "simple_shell"
    "MoryaAI"
    "synthetic_data_generator"
    "MuraAI"
)

for repo in "${repos[@]}"; do
    echo "Processing ${repo}..."
    # Check if the directory exists and is a Git repository
    if [ -d "$repo" ] && [ -d "$repo/.git" ]; then
        cd "$repo"
        # Initialize the repository if not already a Git repository
        git init
        # Add remote GitHub URL to your repository
        git remote add origin "https://$GITHUB_USERNAME:$ACCESS_TOKEN@github.com/$GITHUB_USERNAME/$repo.git"
        # Add all files to the repository
        git add .
        # Commit the added files
        git commit -m "Initial commit"
        # Push the repository to GitHub
        git push -u origin main
        echo "${repo} has been processed."
    else
        echo "Creating ${repo}..."
        # Create a new GitHub repository
        curl -u "$GITHUB_USERNAME:$ACCESS_TOKEN" https://api.github.com/user/repos -d "{\"name\":\"$repo\"}"
        # Initialize the local repository and push
        mkdir "$repo"
        cd "$repo"
        git init
        git remote add origin "https://$GITHUB_USERNAME:$ACCESS_TOKEN@github.com/$GITHUB_USERNAME/$repo.git"
        git add .
        git commit -m "Initial commit"
        git push -u origin main
        echo "${repo} created and pushed."
    fi
    # Go back to the repos directory before processing the next repository
    cd /home/trainora/Desktop/repo
done

echo "All repositories have been processed."

