import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/runner/work/yemek_tarifleri/yemek_tarifleri')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yemek_tarifleri.settings')

application = get_wsgi_application()
