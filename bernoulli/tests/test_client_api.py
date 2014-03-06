from unittest import TestCase

import bernoulli

class TestClientAPI(TestCase):
    def test_thows_if_client_id_is_none(self):
        hit = False
        try:
            experiments = bernoulli.get_experiments()
        except:
            hit = True

        self.assertTrue(hit)