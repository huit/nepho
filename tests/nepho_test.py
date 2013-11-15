from cement.core import handler, hook
from cement.utils import test
from nepho import cli
from nepho.cli.base import Nepho

class MyTestApp(Nepho):
    class Meta:
        argv = []
        config_files = []


class MyTestCase(test.CementTestCase):
    app_class = MyTestApp

    def test_nepho_default(self):
        self.app.setup()
        self.app.run()
        self.app.close()
