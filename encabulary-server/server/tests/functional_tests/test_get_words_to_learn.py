from server.tests.functional_tests.base_learn import BaseLearnTestCase


class TestGetWordsToLearn(BaseLearnTestCase):

    def test_get_learn_words(self):
        response = self._api_get_words_to_learn()

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data'].get('learn'))
        self.assertIsNotNone(response['data'].get('repeat'))
        self.assertEqual(len(response['data']['learn']), 1)
        self.assertEqual(len(response['data']['repeat']), 0)

        data_learn = response['data']['learn'][0]
        self.assertEqual(data_learn['id_word'], self.id_word)
        data_translations = data_learn['translations']

        for tr in self.db_translations:
            self.assertTrue(any([item for item in data_translations if item == tr]))
