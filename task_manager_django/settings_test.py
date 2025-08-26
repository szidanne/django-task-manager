from .settings import *

# Use SQLite for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",   # or BASE_DIR / "test.sqlite3" if you prefer a file
    }
}

# Optional speedups for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
