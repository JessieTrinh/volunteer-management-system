import os, sys, django
# ---------------------------------------------------------------
# Import the core Python and Django modules you'll need.
# - os → lets you work with file paths and environment variables
# - sys → allows you to modify the system path and interact with command-line arguments
# - django → gives access to Django’s setup() and configuration system
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# Force absolute path to your settings file
# ---------------------------------------------------------------
# __file__ refers to the current file's path (where this script is located).
# os.path.dirname(__file__) → gives the folder containing this script.
# os.path.join(..., "volunteerhub") → adds "volunteerhub" to that folder path.
# This effectively constructs the full path to the 'volunteerhub' project directory.
BASE_DIR = os.path.join(os.path.dirname(__file__), "volunteerhub")

# Append the path to sys.path so Python knows where to look for imports.
# Without this, "volunteerhub" might not be found when importing Django settings.
# In short: this ensures Python can locate your Django project’s modules.
sys.path.append(BASE_DIR)


# ---------------------------------------------------------------
# Print where the script is looking for the settings file.
# This helps verify that BASE_DIR is correctly pointing to your project directory.
print(">>> Looking for volunteerhub.settings inside:", BASE_DIR)


# ---------------------------------------------------------------
# Force Django to load the correct settings file.
# ---------------------------------------------------------------
# Here, you explicitly tell Django which settings module to use.
# Normally, Django learns this from the environment or manage.py.
# You’re manually setting it to "volunteerhub.settings".
# That means Django will look for a file called "settings.py"
# inside the "volunteerhub" folder.
os.environ["DJANGO_SETTINGS_MODULE"] = "volunteerhub.settings"


try:
    # -----------------------------------------------------------
    # Initialize Django manually.
    # -----------------------------------------------------------
    # 'django.setup()' loads all of Django’s internal machinery:
    # - settings configuration
    # - app registry
    # - URL routing
    # This must be called before you can safely import Django components
    # that depend on project settings.
    django.setup()

    # -----------------------------------------------------------
    # Import key Django modules after setup succeeds.
    # -----------------------------------------------------------
    from django.conf import settings      # Access Django’s loaded settings
    from django.urls import get_resolver  # Access Django’s URL resolver (for listing URLs)

    # -----------------------------------------------------------
    # Print various diagnostic information.
    # -----------------------------------------------------------
    # settings.DEBUG → tells whether the project is in debug mode (True/False)
    print("DEBUG =", settings.DEBUG)

    # getattr(settings, "ROOT_URLCONF", "MISSING") → shows the root URL configuration module.
    # This tells Django where to look for url patterns (e.g. "volunteerhub.urls").
    print("ROOT_URLCONF =", getattr(settings, "ROOT_URLCONF", "MISSING"))

    # settings.BASE_DIR → prints the base directory path of your Django project.
    print("BASE_DIR =", settings.BASE_DIR)

    # -----------------------------------------------------------
    # Display all URL patterns Django recognizes.
    # -----------------------------------------------------------
    # 'get_resolver()' gets the main URL resolver.
    # '.url_patterns' lists all the URL routes defined in your project.
    # This loop prints each one for inspection.
    print("URL PATTERNS:")
    for p in get_resolver().url_patterns:
        print("  -", p)

except Exception as e:
    # -----------------------------------------------------------
    # If anything goes wrong during setup (e.g., bad path, import error),
    # this prints the exception instead of crashing.
    # -----------------------------------------------------------
    print("Django setup failed:", e)
