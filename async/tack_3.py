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


backoff = 1


async def robust_fetch(client: httpx.AsyncClient, url: str) -> int:

    for attemp in range(3):

        try:
        
            resp = await client.get(url, timeout=5)
            return resp.status_code

        except (httpx.TimeoutException, httpx.HTTPError) as e:
            if attemp == 2:
                raise

            backoff = backoff * 2
            await asyncio.sleep(backoff)



async def robust_main():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        results = await asyncio.gather(
            *(robust_fetch(client, url) for url in URLS),
            return_exceptions=True,
        )

        


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(robust_main())
    print(f"robust: {time.perf_counter() - start:.2f}s")