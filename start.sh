#!/bin/bash

# ১. পুরনো সার্ভিস ও ব্যাকগ্রাউন্ড লগ পরিষ্কার করা
fuser -k 5000/tcp 2>/dev/null
rm -f /root/tunnel.log

# ২. স্ক্রিন ক্লিয়ার করা
clear

# ৩. হ্যাকার স্টাইল ব্যানার
echo -e "\033[1;31m======================================================================"
echo -e "\033[1;33m                [!] --- [ HACKER GQ ATIKUL ] --- [!]                  "
echo -e "\033[1;31m======================================================================"

echo -e "\n\033[1;32m[x] Initializing Python Server & Secure Tunnel...\033[0m"

# ৪. পাইথন সার্ভার ব্যাকগ্রাউন্ডে চালু করা
python3 /sdcard/Download/server.py > /dev/null 2>&1 & 
sleep 2

# ৫. ক্লাউডফ্লেয়ার টানেল ব্যাকগ্রাউন্ডে চালানো
/root/cloudflared tunnel --url http://localhost:5000 > /root/tunnel.log 2>&1 &

echo -e "\033[1;33m[x] Waiting for secure tunnel connection...\033[0m"

# ৬. সময় বাড়িয়ে ১৫ সেকেন্ডের লুপ চেক (যাতে কোনোভাবেই ফেইল না করে)
URL=""
for i in {1..15}; do
    sleep 1
    URL=$(grep -o 'https://[-0-9a-z]*\.trycloudflare\.com' /root/tunnel.log | head -n 1)
    if [ -n "$URL" ]; then
        break
    fi
done

# ৭. স্ক্রিন পরিষ্কার করে প্রিমিয়াম লুকে লিংক প্রদর্শন
clear

echo -e "\033[1;31m======================================================================"
echo -e "\033[1;33m                [!] --- [ HACKER GQ ATIKUL ] --- [!]                  "
echo -e "\033[1;31m======================================================================"

if [ -n "$URL" ]; then
    echo -e "\n\033[1;32m[+] SECURE TUNNEL ESTABLISHED SUCCESSFULLY!\033[0m"
    echo -e "\033[1;37m----------------------------------------------------------------------\033[0m"
    echo -e "\033[1;36m  TARGET URL : \033[1;33m$URL\033[0m"
    echo -e "\033[1;37m----------------------------------------------------------------------\033[0m\n"
else
    echo -e "\n\033[1;31m[-] ERROR: Tunnel connection failed. Check your internet connection.\033[0m\n"
fi

# ৮. সেশন ধরে রাখা
wait