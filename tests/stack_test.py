from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho
import nose


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


# Test Scope
class a_TestNephoStack(test.CementTestCase):
    app_class = NephoTestApp

    def setUp(self):
        super(a_TestNephoStack, self).setUp()

        self.reset_backend()

        app = self.make_app(argv=['cloudlet', '--quiet', 'uninstall', 'nepho-example'])
        app.setup()
        app.run()
        app.close()
        app = self.make_app(argv=['cloudlet', '--quiet', 'install', 'nepho-example'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_list(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'list'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_access(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'access', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_ssh(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'ssh', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_create(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'create', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_deploy(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'deploy', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_up(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'up', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_destroy(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'destroy', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_delete(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'delete', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_show_context(self):
        app = self.make_app(argv=['stack', 'show-context', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_validate(self):
        app = self.make_app(argv=['stack', 'validate', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()

    def test_nepho_stack_status(self):
        raise nose.SkipTest('skip this until #165 is resolved')
        app = self.make_app(argv=['stack', 'status', 'nepho-example', 'vagrant-single-host'])
        app.setup()
        app.run()
        app.close()
