"""WSGI config for partmart_cards project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'partmart_cards.settings')
application = get_wsgi_application()
