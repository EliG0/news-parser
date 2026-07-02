from pathlib import Path


def simple_merge(files, output='merge.txt'):
    """Просто собирает содержимое файлов в один txt"""
    with open(output, 'w', encoding='utf-8') as out:
        for file in files:
            path = Path(file)
            if path.exists() and path.is_file():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        out.write(f"\n=== {path.name} ===\n\n")
                        out.write(f.read())
                        out.write("\n\n")
                    print(f"✅ {path.name}")
                except:
                    print(f"❌ {path.name} (ошибка)")
            else:
                print(f"❌ {file} (не найден)")


if __name__ == "__main__":
    simple_merge(["services/DownloadService.py",
                  "services/ExtractService.py",
                  "services/MatchService.py",
                  "services/StorageService.py",
                  "services/Pipeline.py",
                  "services/Model.py",
                  "strategies/Strategy.py",
                  "strategies/WebsiteStrategy.py",
                  "strategies/RSSStrategy.py",
                  "admin.py",
                  "models.py",
                  "serializers.py",
                  "views.py",
                  "Crawler.py",
                  ])
