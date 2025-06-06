# AI Translator Agent using VideoSDK and OpenAI Realtime API

This project is a real-time translation application that enables people speaking different languages to communicate with each other seamlessly. The system consists of a full-stack implementation with both frontend and backend components that work together to create a video conferencing experience with AI-powered translation.

![openai realtime api - Speech to Speech Architecture](https://assets.videosdk.live/images/ai%20voice%20agent%20deepgram%20architecture.png)

### Start with the project

```sh
git clone https://github.com/videosdk-community/videosdk-openai-realtime-translator.git
```

```sh
cd videosdk-openai-realtime-translator
```

### Client Setup

1. Navigate to `client` dir:
   ```sh
   cd client
   ```
2. Make a copy of the environment configuration file:

   ```sh
   cp .env.example .env
   ```

3. Create a `.env` file in the `client` folder with:

   ```env
   VITE_APP_VIDEOSDK_TOKEN=your_videosdk_auth_token_here
   ```

Obtain your VideoSDK Auth Token from [app.videosdk.live](https://app.videosdk.live)

### Server Setup (Python FastAPI)

Create Virtual Environment (from project root):

```sh
python -m venv .venv
```

Create a virtual environment:

Install Dependencies:

```sh
pip install -r requirements.txt
```

Create Server Environment File (in project root):

```sh
cp .env.example .env
```

Add these keys to your `.env` file:

```sh
OPENAI_API_KEY=your_openai_key_here
```

🔑 Obtaining API Keys

- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **VideoSDK Token**: [https://app.videosdk.live](https://app.videosdk.live)

---

### ▶️ Running the Application

Start the Server (From Project Root):

```sh
uvicorn app:app
```

Start the Client (From `/client` Folder):

```sh
npm run dev
```

---

## System Architecture

The architecture consists of three main components:

1. **Frontend Web Application** - A React-based interface for users to join meetings
2. **Backend Server** - A FastAPI service that manages the AI translation agent
3. **AI Translation Agent** - A Python-based service that handles real-time translation

## Technical Components

### Frontend (React with TypeScript)

The frontend is built with React and TypeScript, using the VideoSDK.live platform for real-time video conferencing. Key files include:

- `App.tsx` - The main application component that handles meeting creation, joining, and user interface
- `MeetingControls.tsx` - Controls for meeting management (end call, invite AI, copy meeting ID)
- `ParticipantCard.tsx` - Component to display participants with video/audio and speaking indicators

The UI is styled with a dark theme using Tailwind CSS, featuring a sleek interface with gradients and modern controls.

### Backend (Python with FastAPI)

The backend service uses FastAPI to manage API endpoints and the translation agent:

- `main.py` - Defines the FastAPI server with endpoints to join the AI translator to meetings
- `ai_agent.py` - Core agent logic that handles meeting participation and audio processing
- `audio_stream_track.py` - Manages audio streaming for real-time processing
- `openai_intelligence.py` - Interfaces with OpenAI's API for speech-to-text and translation

### Translation Functionality

The translation system works through these steps:

1. **Audio Capture** - Captures audio from meeting participants
2. **Speech Processing** - Converts audio to PCM format and sends to OpenAI
3. **Language Detection & Translation** - OpenAI identifies the language and translates in real-time
4. **Audio Output** - The translated speech is streamed back into the meeting

## Key Features

1. **Real-time Translation** - Translates conversations between participants in different languages
2. **Language Selection** - Users can select their preferred language when joining a meeting
3. **Meeting Creation/Joining** - Users can create new meetings or join existing ones
4. **Push-to-Talk** - Users can hold the space bar or click a button to speak
5. **AI Integration** - An AI agent joins as a participant to provide translation services
6. **Visual Speaking Indicators** - UI animations show who is currently speaking

## Workflow

1. A user creates a meeting and selects their preferred language
2. Another user joins the meeting with their preferred language
3. The first user invites the AI translator by clicking the "Invite AI Translator" button
4. When a participant speaks, their audio is sent to the AI agent
5. The AI agent translates the speech and broadcasts it back in the other participant's language
6. The UI shows speaking indicators to help users know when to speak

## Technical Implementation Details

### Audio Processing Pipeline

1. Participant audio is captured as frames and sent to `add_audio_listener` function
2. Audio is converted to the proper format (PCM-16, 16kHz mono)
3. Processed audio is sent to OpenAI via WebSocket API
4. OpenAI responds with translated audio
5. The AI agent broadcasts the translated audio to the meeting

### OpenAI Intelligence Module

- Handles WebSocket communication with OpenAI's real-time API
- Processes audio transcripts and translations
- Manages session instructions for translation requirements

### Meeting Management

- Uses VideoSDK.live's React SDK for video conferencing
- Manages participant states, audio/video streams, and UI indicators
- Handles the "Hold to Speak" functionality to prevent audio feedback

## User Flow

1. User lands on the application and either creates a new meeting or joins an existing one
2. User enters their name and selects their preferred language
3. In the meeting, they can see other participants, including the AI translator when it joins
4. Users communicate by holding space or the "Hold to Speak" button
5. The AI translates speech in real-time between participants

## Customization

The translation behavior is configured using a dynamic instruction set that tells the AI agent how to handle the translation based on participants' languages. The system automatically detects which languages are being spoken and translates accordingly.

This comprehensive application demonstrates effective integration of WebRTC, AI translation services, and modern web development to create a practical solution for breaking language barriers in real-time communication.

For more information, check out [docs.videosdk.live](https://docs.videosdk.live).


Build AI Voice Agent using OpenAI Realtime API and VideoSDK
https://www.youtube.com/watch?v=RaWwrdU29g4
