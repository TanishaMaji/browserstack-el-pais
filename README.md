## Translation API Note
This project uses public LibreTranslate endpoints for Spanish to English translation.
Public endpoints may be rate limited or temporarily unavailable, which can return empty responses.
The script includes retries and a graceful fallback ("[Translation failed]") to ensure the pipeline completes without crashing.
In production, a stable paid API such as Google Cloud Translate / DeepL should be used.