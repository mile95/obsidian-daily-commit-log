#!/bin/sh

echo "Installing obsidian daily commit log..."

# Create ~/gitconfigs/hooks
mkdir -p ~/gitconfigs/hooks

# Copy commit-msg.py to newly created directory
cp commit-msg.py ~/gitconfigs/hooks/commit-msg

# Define the content you want to add to ~/.gitconfig
config_content="[core]\n\thooksPath = ~/gitconfigs/hooks"

if [ -f ~/.gitconfig ]; then
    if ! grep -qF "[core]" ~/.gitconfig; then
        # Append the content to ~/.gitconfig
        echo "$config_content" >> ~/.gitconfig
    fi
else
    echo "$config_content" > ~/.gitconfig
fi




