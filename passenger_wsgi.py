import sys, os

HOME = os.environ.get('HOME')
SRCDIR = HOME + '/new.sfair.org/source'
PROJECTNAME = 'sfair'
VENV = HOME + '/sfair_venv'
INTERP = VENV + '/bin/python3'

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '{v}/lib/python3.4/site-packages'.format(v=VENV))
sys.path.insert(0, SRCDIR)

os.environ['DJANGO_SETTINGS_MODULE'] = '{p}.settings.production'.format(p=PROJECTNAME)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
