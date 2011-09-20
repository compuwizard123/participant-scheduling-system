from django.core.management.base import BaseCommand

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = 'Installs the data from ...'
    args = 'loaddb'
    
    def handle(self, *args, **kwargs):
        app = 'pss.main'
        print 'Loading custom test data for %s...' % app
        try:
            mod = __import__('%s.test_data' % app, {}, {}, [''])
        except ImportError, exc:
            if str(exc) != 'No module named test_data':
                # It's something other than a missing tests module, probably a real
                # error, so show the user.
                import traceback
                traceback.print_exc()
        else:
            mod.run()
