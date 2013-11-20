class BasicNephoTests(test.CementTestCase):
    app_class = NephoTestApp

    def test_nepho_default(self):
        self.app.setup()
        self.app.run()
        self.app.close()
