import asyncio
import edge_tts

# গল্পের পার্টগুলো এখানে থাকবে
story_parts = [
    "শোননা সোনা... সারাদিন তো কত কথাই হয়, কিন্তু তোমাকে ছাড়া একটি মুহূর্তও আমার ভালো কাটে না।",
    "রাতের এই নিস্তব্ধতায় শুধু তোমার কথা মনে পড়ে, আর ইচ্ছে করে এই মুহূর্তে তোমার খুব কাছাকাছি চলে আসি...",
    "তোমার বাহুডোরে হারিয়ে যাই। তুমি কি একটুও অনুভব করতে পারো আমার এই নিঃশব্দের আকুলতা",
    # তোর বাকি লাইনগুলো এখানে কমা দিয়ে দিয়ে বসাবি
]

# মাইক্রোসফটের মিষ্টি বাংলা নারী কণ্ঠ
VOICE = "bn-BD-NabanitaNeural" 

async def generate_long_story():
    print("বড় গল্পের অডিও পার্টগুলো তৈরি শুরু হয়েছে...")
    
    for i, text_part in enumerate(story_parts):
        output_path = f"/sdcard/Download/story_part_{i+1}.mp3"
        
        try:
            communicate = edge_tts.Communicate(
                text=text_part, 
                voice=VOICE, 
                rate="-10%"
            )
            await communicate.save(output_path)
            print(f"পার্ট {i+1} সফলভাবে সেভ হয়েছে: {output_path}")
        except Exception as e:
            print(f"⚠️ পার্ট {i+1} এ একটু সমস্যা হয়েছিল, তাই এটি এড়িয়ে পরের পার্টে যাচ্ছি। (ত্রুটি: {e})")

    print("==================================================")
    print(" আলহামদুলিল্লাহ! অডিও প্রসেসিং সম্পন্ন হয়েছে!")
    print("==================================================")

# কোড রান করা
asyncio.run(generate_long_story())