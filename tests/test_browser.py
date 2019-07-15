from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserTests(StaticLiveServerTestCase):
    def setUp(self, *args, **kwargs):
        capabilities = DesiredCapabilities.CHROME
        capabilities['loggingPrefs'] = {'browser': 'ALL'}

        self.driver = webdriver.Chrome(
            service_args=["--verbose", "--log-path=selenium.log"],
            desired_capabilities=capabilities,
        )
        self.driver.set_page_load_timeout(15)

    def get(self, url):
        self.driver.get("%s%s" % (self.live_server_url, url))

    def test_page_loads(self):
        self.get("/")
        panel = self.driver.find_elements_by_css_selector(".panel")
        assert len(panel) > 0, "Should have at least one panel"

    def tearDown(self):
        self.driver.quit()
