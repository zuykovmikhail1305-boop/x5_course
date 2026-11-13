import hashlib
from concurrent.futures import ProcessPoolExecutor
import asyncio
import time
import requests
import httpx


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


backoff = 1


async def robust_fetch(client: httpx.AsyncClient, url: str) -> int:

    global backoff

    for attemp in range(3):

        try:
        
            resp = await client.get(url, timeout=5)
            return resp.content

        except (httpx.TimeoutException, httpx.HTTPError) as e:
            if attemp == 2:
                raise

            delay = 2 ** attemp
            await asyncio.sleep(delay)



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

        
def heavy(body: bytes) -> str:
   return hashlib.sha256(body * 1000).hexdigest()


async def ticker():
    while True:
        print(".", end="", flush=True)
        await asyncio.sleep(0.1)


async def cpu_main():
    bodies, _ = await robust_main()
    tick = asyncio.create_task(ticker())
    await asyncio.sleep(0.5)                         

    start = time.perf_counter()
    hashes_naive = [heavy(b) for b in bodies.values()]
    print(f"\n  {len(hashes_naive)} хешей за {time.perf_counter() - start:.2f}s")
    await asyncio.sleep(0.5)

    print('=================')

    loop = asyncio.get_running_loop()
    start = time.perf_counter()

    with ProcessPoolExecutor() as pool:
        hashes_pool = await asyncio.gather(
            *(pool.run_in_executor(loop, heavy, b) for b in bodies.values())
        )

    print(f"\n  {len(hashes_pool)} хешей за {time.perf_counter() - start:.2f}s")

    tick.cancel()
    assert hashes_naive == hashes_pool
    print("Хеши совпадают")

    
if __name__ == "__main__":
    asyncio.run(cpu_main())

