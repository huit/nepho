from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho


class NephoTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


class BasicNephoTests(test.CementTestCase):
    app_class = NephoTestApp

    def test_nepho_default(self):
        self.app.setup()
        self.app.run()
        self.app.close()
