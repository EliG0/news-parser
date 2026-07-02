# parser/services/DownloadService.py
import asyncio
from typing import List, Dict

import aiohttp

import logging
logger = logging.getLogger(__name__)

class DownloadService:
    def __init__(self, headers: Dict[str, str] = None) -> None:
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    async def downloadPage(self, session: aiohttp.ClientSession, url: str):
        timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with session.get(url, headers=self.headers, timeout=timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    return {'url': url, 'html': html}

                logger.warning(f"Сайт вернул статус {response.status}: {url}")
                return None

        except asyncio.TimeoutError:
            logger.error(f"Превышено время ожидания (Таймаут 10с) для: {url}")
            return None

        except aiohttp.ClientError:
            logger.error(f"Ошибка для {url}")
            return None

        except Exception as e:
            logger.error(f"Ошибка сети при попытке скачать {url}: {e}")
            return None


    async def downloadAllPages(self, urls: List[str]):
        semaphore = asyncio.Semaphore(10)

        async def sem_download(session, url):
            async with semaphore:
                return await self.downloadPage(session, url)

        async with aiohttp.ClientSession() as session:
            tasks = [sem_download(session, url) for url in urls]

            results = await asyncio.gather(*tasks)
            results = list(filter(lambda x: x is not None, results))
            return results

    def download(self, urls: List[str]):
        if not urls:
            return []

        return asyncio.run(self.downloadAllPages(urls))
