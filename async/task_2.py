import asyncio
import time
import requests
import httpx


URLS = [f"https://picsum.photos/seed/{i}/800/600" for i in range(20)]


def timed(label, fn, *args):
   """Запускает fn(*args) и печатает, сколько секунд она работала."""
   start = time.perf_counter()
   fn(*args)
   print(f"{label}: {time.perf_counter() - start:.2f}s")


def sync_main():
   for url in URLS:
       requests.get(url)   # по очереди, время складывается

async def fast_main():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        await asyncio.gather(*[asyncio.create_task(client.get(url)) for url in URLS])


if __name__ == "__main__":
   timed("sync ", sync_main)
   timed("async", lambda: asyncio.run(fast_main()))
