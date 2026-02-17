from aiortc import VideoStreamTrack, RTCPeerConnection
from aiortc.contrib.signaling import TcpSocketSignaling
import cv2
import asyncio
from av import VideoFrame

class WebcamVideoStreamTrack(VideoStreamTrack):
    def __init__(self, camera_id):
        super().__init__()
        self.web_cam = cv2.VideoCapture(camera_id)
        self.web_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.web_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    async def recv(self):
        await asyncio.sleep(1/30)
        ret, frame = self.web_cam.read()
        if not ret:
            return None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = VideoFrame.from_ndarray(frame_rgb, format="rgb24")
        return video_frame

async def setup_and_run_server(server_ip, server_port, webcam_id):
    signaling = TcpSocketSignaling(server_ip, server_port)
    await signaling.connect()
    connection = RTCPeerConnection()
    video_streamer = WebcamVideoStreamTrack(webcam_id)
    connection.addTrack(video_streamer)

    offer = await connection.createOffer()
    await connection.setLocalDescription(offer)
    await signaling.send(offer)
    response = await signaling.receive()
    await connection.setRemoteDescription(response)

    print("Serveur pret - Streaming en cours...")
    while True:
        await asyncio.sleep(1)