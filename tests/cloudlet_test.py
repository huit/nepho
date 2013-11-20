from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


# Test Cloudlet
class a_TestNephoCloudlet(test.CementTestCase):
    app_class = NephoTestApp

    def test_nepho_cloudlet_list(self):
        app = self.make_app(argv=['cloudlet', 'list'])
        app.setup()
        app.run()
        app.close()
