from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer
from aiortc.contrib.signaling import TcpSocketSignaling
import asyncio
import cv2
import threading

class VideoReceiver:
    def __init__(self):
        self.running = True
        self.current_frame = None
        self.frame_count = 0

    def display_thread(self):
        cv2.namedWindow("WebRTC Client", cv2.WINDOW_NORMAL)
        print("Fenetre creee")
        
        while self.running:
            if self.current_frame is not None:
                cv2.imshow("WebRTC Client", self.current_frame)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                self.running = False
        
        cv2.destroyAllWindows()
        print("Fenetre fermee")

    async def receive_track(self, track):
        print("Track recu: " + track.kind)
        
        thread = threading.Thread(target=self.display_thread)
        thread.start()
        
        while self.running:
            try:
                frame = await asyncio.wait_for(track.recv(), timeout=2.0)
                self.frame_count += 1
                
                img = frame.to_ndarray(format="rgb24")
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                self.current_frame = img
                
                if self.frame_count % 30 == 0:
                    print(f"Recu {self.frame_count} frames")
                    
            except asyncio.TimeoutError:
                print("Timeout - pas de frame")
                continue
            except Exception as e:
                print("Erreur: " + str(e))
                break
        
        thread.join()

async def run_client(server_ip, server_port):
    print(f"Connexion a {server_ip}:{server_port}")
    
    signaling = TcpSocketSignaling(server_ip, server_port)
    await signaling.connect()
    print("Signaling connecte")
    
    # Même configuration que le serveur
    config = RTCConfiguration([
        RTCIceServer("stun:stun.l.google.com:19302")
    ])
    
    pc = RTCPeerConnection(configuration=config)
    receiver = VideoReceiver()
    
    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            print("Track video recu")
            asyncio.create_task(receiver.receive_track(track))
    
    @pc.on("iceconnectionstatechange")
    async def on_ice():
        print(f"ICE: {pc.iceConnectionState}")
        if pc.iceConnectionState == "connected":
            print("CONNECTE AU SERVEUR")
    
    print("Attente offre...")
    offer = await signaling.receive()
    await pc.setRemoteDescription(offer)
    print("Offre recue")
    
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    await signaling.send(answer)
    print("Reponse envoyee")
    
    print("Connecte - Attente video...")
    
    while receiver.running:
        await asyncio.sleep(1)
    
    await pc.close()
    await signaling.close()