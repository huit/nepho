from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho
import nose


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


# Test Cloudlet
class a_TestNephoCloudlet(test.CementTestCase):
    app_class = NephoTestApp

    def setUp(self):
        super(a_TestNephoCloudlet, self).setUp()

        self.reset_backend()

        app = self.make_app(argv=['cloudlet', 'registry-update'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['cloudlet', '--quiet', 'uninstall', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['cloudlet', '--quiet', 'install', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_registry_update(self):
        app = self.make_app(argv=['cloudlet', 'registry-update'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_update_registry(self):
        app = self.make_app(argv=['cloudlet', 'update-registry'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_list(self):
        app = self.make_app(argv=['cloudlet', 'list'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_search(self):
        app = self.make_app(argv=['cloudlet', 'search', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_install(self):
        raise nose.SkipTest('skip this until #164 is implemented')
        app = self.make_app(argv=['cloudlet', 'install', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_describe(self):
        app = self.make_app(argv=['cloudlet', 'describe', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_update(self):
        app = self.make_app(argv=['cloudlet', 'update', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_upgrade(self):
        app = self.make_app(argv=['cloudlet', 'upgrade', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_uninstall(self):
        raise nose.SkipTest('skip this until #164 is implemented')
        app = self.make_app(argv=['cloudlet', 'uninstall', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_cloudlet_remove(self):
        raise nose.SkipTest('skip this until #164 is implemented')
        app = self.make_app(argv=['cloudlet', 'remove', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
