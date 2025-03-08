import base64
import traceback
from typing import Dict, List, Union, Callable
from utils.struct.openai import (
    AudioFormats,
    ClientToServerMessage,
    EventType,
    InputAudioBufferAppend,
    InputAudioTranscription,
    ResponseFunctionCallArgumentsDone,
    ServerVADUpdateParams,
    SessionUpdate,
    SessionUpdateParams,
    Voices,
    parse_server_message,
    generate_event_id,
    to_json,
)
import json

from asyncio.log import logger
from asyncio import AbstractEventLoop
import aiohttp
import asyncio
from agent.audio_stream_track import CustomAudioStreamTrack

class OpenAIIntelligence:
    def __init__(
        self, 
        loop: AbstractEventLoop, 
        api_key,
        model: str = "gpt-4o-realtime-preview-2024-10-01",
        instructions="""\
            Actively listen to the user's questions and provide concise, relevant responses. 
            Acknowledge the user's intent before answering. Keep responses under 2 sentences.\
        """,
        base_url: str = "api.openai.com",
        voice: Voices = Voices.Alloy,
        temperature: float = 0.8,
        tools: List[Dict[str, Union[str, any]]] = [],
        input_audio_transcription: InputAudioTranscription = InputAudioTranscription(
            model="whisper-1"
        ),
        clear_audio_queue: Callable[[], None] = lambda: None,
        handle_function_call: Callable[[ResponseFunctionCallArgumentsDone], None] = lambda x: None,
        modalities=["text", "audio"],
        max_response_output_tokens=512,
        turn_detection: ServerVADUpdateParams = ServerVADUpdateParams(
            type="server_vad",
            threshold=0.5,
            prefix_padding_ms=300,
            silence_duration_ms=200,
        ),
        audio_track: CustomAudioStreamTrack = None,
    
        ):
        self.model = model
        self.loop = loop
        self.api_key = api_key
        self.instructions = instructions
        self.base_url = base_url
        self.temperature = temperature
        self.voice = voice
        self.tools = tools
        self.modalities = modalities
        self.max_response_output_tokens = max_response_output_tokens
        self.input_audio_transcription = input_audio_transcription
        self.clear_audio_queue = clear_audio_queue
        self.handle_function_call = handle_function_call
        self.turn_detection = turn_detection
        self.ws = None
        self.audio_track = audio_track
        
        self._http_session = aiohttp.ClientSession(loop=self.loop)
        self.session_update_params = SessionUpdateParams(
            model=self.model,
            instructions=self.instructions,
            input_audio_format=AudioFormats.PCM16,
            output_audio_format=AudioFormats.PCM16,
            temperature=self.temperature,
            voice=self.voice,
            tool_choice="auto",
            tools=self.tools,
            turn_detection=self.turn_detection,
            modalities=self.modalities,
            max_response_output_tokens=self.max_response_output_tokens,
            input_audio_transcription=self.input_audio_transcription,
        )

    async def connect(self):
        # url = f"wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
        url = f"wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
        logger.info("Establishing OpenAI WS connection... ")
        self.ws = await self._http_session.ws_connect(
            url=url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "OpenAI-Beta": "realtime=v1",
            },
        )
        logger.info("OpenAI WS connection established")
        self.receive_message_task = self.loop.create_task(
            self.receive_message_handler()
        )

        print("List of tools", self.tools)

        await self.update_session(self.session_update_params)

        await self.receive_message_task

    async def update_session(self, session: SessionUpdateParams):
        print("Updating session", session.tools)
        await self.send_request(
            SessionUpdate(
                event_id=generate_event_id(),
                session=session,
            )
        )
        
    
    async def send_request(self, request: ClientToServerMessage):
        request_json = to_json(request)
        await self.ws.send_str(request_json)
        
    async def send_audio_data(self, audio_data: bytes):
        """audio_data is assumed to be pcm16 24kHz mono little-endian"""
        base64_audio_data = base64.b64encode(audio_data).decode("utf-8")
        message = InputAudioBufferAppend(audio=base64_audio_data)
        await self.send_request(message)

    async def receive_message_handler(self):
        while True:
            async for response in self.ws:
                try:
                    await asyncio.sleep(0.01)
                    if response.type == aiohttp.WSMsgType.TEXT:
                        # print("Received message", response)
                        self.handle_response(response.data)
                    elif response.type == aiohttp.WSMsgType.ERROR:
                        logger.error("Error while receiving data from openai", response)
                except Exception as e:
                    traceback.print_exc()
                    print("Error in receiving message:", e)

    def clear_audio_queue(self):
        pass
                
    def on_audio_response(self, audio_bytes: bytes):
        self.loop.create_task(
            self.audio_track.add_new_bytes(iter([audio_bytes]))
        )
        
    def handle_response(self, message: str):
        message = json.loads(message)

        match message["type"]:
            
            case EventType.SESSION_CREATED:
                logger.info(f"Server Message: {message["type"]}")
                # print("Session Created", message["session"])
                
            case EventType.SESSION_UPDATE:
                logger.info(f"Server Message: {message["type"]}")
                # print("Session Updated", message["session"])

            case EventType.RESPONSE_AUDIO_DELTA:
                logger.info(f"Server Message: {message["type"]}")
                self.on_audio_response(base64.b64decode(message["delta"]))
                
            case EventType.RESPONSE_AUDIO_TRANSCRIPT_DONE:
                logger.info(f"Server Message: {message["type"]}")
                print(f"Response Transcription: {message["transcript"]}")
            
            case EventType.ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
                logger.info(f"Server Message: {message["type"]}")
                print(f"Client Transcription: {message["transcript"]}")
            
            case EventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                logger.info(f"Server Message: {message["type"]}")
                logger.info("Clearing audio queue")
                self.clear_audio_queue()

        
            case EventType.ERROR:
                logger.error(f"Server Error Message: ", message["error"])