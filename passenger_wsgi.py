import os
import sys


SRCDIR = os.environ['SRCDIR']
PROJECTNAME = os.environ['PROJECT_NAME']
VENV = os.environ['VENV']  
INTERP = os.environ['INTERP']

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '{v}/lib/python3.4/site-packages'.format(v=VENV))
sys.path.insert(0, SRCDIR)

os.environ['DJANGO_SETTINGS_MODULE'] = '{p}.settings'.format(p=PROJECTNAME)


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
