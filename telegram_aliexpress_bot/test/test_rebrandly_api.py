import unittest

from telegram_aliexpress_bot.rebrandly_api import RebrandlyApi


class TestRebrandlyApi(unittest.TestCase):
    def setUp(self):
        self.cut = RebrandlyApi()

    def test_get_short_url(self):
        long_url = "http://gw.api.alibaba.com/openapi/param2/2/portals.open/api.getPromotionLinks/15984?trackingId=Al" \
                   "phaExpress&urls=https://www.aliexpress.com/item/Bastec-Ultra-Durable-Nylon-Braided-Wire-Metal-Plu" \
                   "g-Data-Sync-Charging-Data-Phone-Micro-USB-Cable/32794663842.html"
        url, self._url_id = self.cut.get_short_url(long_url, "UnitTest_")
        self.assertTrue("rebrand.ly/UnitTest_" in url)

    # TODO: Test link delete and delete created link


if __name__ == '__main__':
    unittest.main()
