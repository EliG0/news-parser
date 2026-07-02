---

Django, Django REST Framework (DRF), django-import-export, django-rest-spectacular

aiohttp, asyncio, BeautifulSoup4, feedparser, requests, trafilatura

---

**`Strategies`:** На основе типа источника (`site`, `rss`, `vk`) выбирает нужный алгоритм поиска
первичных ссылок.

* `WebsiteStrategy` — парсинг HTML-кода через BeautifulSoup4 и фильтрация по регулярным выражениям (`source.patterns`).
* `RSSStrategy` — загрузка XML-фидов через `requests` и разбор структуры с помощью `feedparser`
* `VKStrategy` — пока заглушка, а так парсинг VK API

**`DownloadService`:** Асинхронный пакетный загрузчик страниц на базе `aiohttp`

**`ExtractService`:** Извлечение чистого текста статьи с помощью `trafilatura`.

**`MatchService`:** Проверка текста на пересечение со списком ключевых слов с использованием регулярных
выражений

**`StorageService`:** Запись в БД

---

## 🔌 Django REST Framework API

Реализовано REST API на базе `ModelViewSet`

* **Эндпоинт списков и деталей:** `/api/articles/`
* **Сваггер:** `/api/swagger/`

---

## ⚙️ Админ-панель Django

* **`django-import-export`**
* **`trigger_parser`**, позволяющий вручную запустить итерацию парсинга только для выбранных галочками сайтов.

---