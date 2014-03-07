from unittest import TestCase
from httmock import urlmatch, HTTMock

import bernoulli, json

class TestClientAPI(TestCase):
    def test_thows_if_client_id_is_none(self):
        hit = False
        try:
            experiments = bernoulli.get_experiments()
        except:
            hit = True

        self.assertTrue(hit)

    def test_handles_failure(self):
        @urlmatch(netloc=r'(.*\.)?bernoulli.herokuapp.com$', path='/client/api/experiments/')
        def get_experiments_mock(url, request):
            self.assertEqual(url[3], 'experimentIds=1234&bucketIfNecessary=True&userId=s59&clientId=1')
            return {
                'status': 200,
                'content': json.dumps({
                    'status': 'error',
                    'message': 'invalid clientId',
                })
            }

        with HTTMock(get_experiments_mock):
            threw = False
            try:
                experiments = bernoulli.get_experiments(client_id="1", experiment_ids=["1234"], user_id="s59")
            except:
                threw = True

            self.assertTrue(threw)


    def test_handles_success(self):
        @urlmatch(netloc=r'(.*\.)?bernoulli.herokuapp.com$', path='/client/api/experiments/')
        def get_experiments_mock(url, request):
            return {
                'status': 200,
                'content': json.dumps({
                    'status': 'ok',
                    'value': [{ 'id': 32, }],
                })
            }

        with HTTMock(get_experiments_mock):
            experiments = bernoulli.get_experiments(client_id="1", experiment_ids=["1234"], user_id='s59')
            self.assertEqual(1, len(experiments))
            self.assertEqual(32, experiments[0]['id'])

    def test_goal_attained_makes_call(self):
        @urlmatch(netloc=r'(.*\.)?bernoulli.herokuapp.com$', path='/client/api/experiments/')
        def goal_attained_mock(url, request):
            return {
                'status': 200,
                'content': json.dumps({
                    'status': 'ok',
                    'value': True,
                })
            }

        with HTTMock(goal_attained_mock):
            result = bernoulli.record_goal_attained(client_id="1", experiment_id='1234', user_id="s59")
            self.assertTrue(result)