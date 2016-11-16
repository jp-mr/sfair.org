import os
import sys


SRCDIR = os.environ['SRCDIR']
PROJECTNAME = os.environ['PROJECT_NAME']
<<<<<<< HEAD
VENV = os.environ['VENV']
INTERP = os.environ['INTERP']


=======
VENV = os.environ['VENV']  
INTERP = os.environ['INTERP']

>>>>>>> 330b3b6a91ccc86fa28d135f5ec8c9ad687d002d
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '{v}/lib/python3.4/site-packages'.format(v=VENV))
sys.path.insert(0, SRCDIR)

os.environ['DJANGO_SETTINGS_MODULE'] = '{p}.settings'.format(p=PROJECTNAME)


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
