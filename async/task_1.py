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


async def fetch(client: httpx.AsyncClient, url: str) -> int:
   resp = await client.get(url)
   return resp.status_code

async def slow_main():
   async with httpx.AsyncClient(follow_redirects=True) as client:
       for url in URLS:
           await fetch(client, url)   



timed("slow ", lambda: asyncio.run(slow_main()))
