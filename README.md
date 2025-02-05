# livekit_autonomous_voice_assistant
Engages an AI autonomous voice assistant in a real conversation

Source: https://www.youtube.com/watch?v=DNWLIAK4BUY&ab_channel=TechWithTim

Implements:
- Connects to LiveKit playground to start a conversation https://livekit.io/

Steps:

1) run a docker image

   $ docker container run -d python:3.10 sleep infinity

2) pip install -r requirements.txt

3) python3 agent.py dev

4) connect to Livekit agent playground https://agents-playground.livekit.io/

