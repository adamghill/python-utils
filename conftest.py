import pytest
from django.conf import settings


def pytest_configure():
    templates = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["tests"],
        }
    ]
    databases = {"default": {"ENGINE": "django.db.backends.sqlite3",}}
    installed_apps = []
    caches = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }

    settings.configure(
        TEMPLATES=templates,
        ROOT_URLCONF="project.urls",
        DATABASES=databases,
        INSTALLED_APPS=installed_apps,
        UNIT_TEST=True,
        CACHES=caches,
    )


@pytest.fixture(autouse=True)
def reset_settings(settings):
    """
    This takes the original settings before the test is run, runs the test, and then resets them afterwards.
    This is required because mutating nested dictionaries does not reset them as expected by `pytest-django`.
    More details in https://github.com/pytest-dev/pytest-django/issues/601#issuecomment-440676001.
    """

    # Get original settings
    cache_settings = {**settings.CACHES}

    # Run test
    yield

    settings.CACHES = cache_settings
