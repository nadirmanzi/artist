#!/bin/bash

# Start a new tmux session in the background named 'dev_servers'
tmux new-session -d -s dev_servers -n Django 'cd backend && source venv/bin/activate && python manage.py runserver'

# Create a second window (tab) for the frontend
tmux new-window -t dev_servers:1 -n Bun 'cd frontend && bun run dev'

# Attach your current terminal to the session
tmux attach-session -t dev_servers
