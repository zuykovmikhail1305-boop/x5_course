import asyncio
import time
import requests
import httpx


URLS = [f"https://picsum.photos/seed/{i}/800/600" for i in range(20)]
URLS.extend(

    ["https://no-such-site.invalid",
    "https://httpbin.org/delay/10" ]

)


def timed(label, fn, *args):
   """Запускает fn(*args) и печатает, сколько секунд она работала."""
   start = time.perf_counter()
   fn(*args)
   print(f"{label}: {time.perf_counter() - start:.2f}s")


sem = asyncio.Semaphore(5)

async def robust_fetch(client: httpx.AsyncClient, url: str) -> bytes:
    async with sem:
        for attempt in range(3):
            try:
                resp = await client.get(url, timeout=httpx.Timeout(20, connect=5))
                resp.raise_for_status()
                return resp.content
            except httpx.HTTPError:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)



async def robust_main():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        results = await asyncio.gather(
            *(robust_fetch(client, url) for url in URLS),
            return_exceptions=True,
        )

        ok, errors = {}, []
        for url, res in zip(URLS, results):
            if isinstance(res, Exception):
                errors.append((url, repr(res)))
            else:
                ok[url] = res

        print(f"Успешно: {len(ok)}, ошибок: {len(errors)}")
        for url, err in errors:
            print(f"  {url} -> {err}")
        return ok, errors

        


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(robust_main())
    print(f"robust: {time.perf_counter() - start:.2f}s")