# which_settings.py

# -------------------------------
# 1. Import the 'os' module from Python's standard library.
#    'os' lets you interact with the operating system, such as
#    reading environment variables (like DJANGO_SETTINGS_MODULE).
import os

# -------------------------------
# 2. Import the 'settings' object from Django’s configuration system.
#    This gives access to all active Django settings (like DEBUG, ALLOWED_HOSTS, etc.)
#    based on whichever settings module Django has loaded.
from django.conf import settings

# -------------------------------
# 3. Print the value of the environment variable 'DJANGO_SETTINGS_MODULE'.
#    - This variable tells Django *which settings file* to use (e.g. "myproject.settings.dev").
#    - If it’s not set, os.environ.get() will return None instead of crashing.
print("DJANGO_SETTINGS_MODULE =", os.environ.get("DJANGO_SETTINGS_MODULE"))

# -------------------------------
# 4. Print the value of the 'DEBUG' setting from Django.
#    - getattr() safely tries to get the attribute from 'settings'.
#    - If 'DEBUG' doesn’t exist, it returns "???" instead of raising an error.
#    - This shows whether Django is running in debug mode (True/False).
print("DEBUG =", getattr(settings, "DEBUG", "???"))

# -------------------------------
# 5. Print the value of the 'ALLOWED_HOSTS' setting.
#    - 'ALLOWED_HOSTS' defines which host/domain names this Django site can serve.
#    - Using getattr() with a default of "???" avoids breaking the script
#      if that setting isn’t defined.
print("ALLOWED_HOSTS =", getattr(settings, "ALLOWED_HOSTS", "???"))

# -------------------------------
# 6. Print the file path where the active settings were loaded from.
#    - 'settings.__file__' gives the absolute path to the settings file in use.
#    - This helps confirm which settings module Django is actually using
#      (useful when multiple settings files exist, like dev/test/prod).
print("Settings loaded from:", settings.__file__)
