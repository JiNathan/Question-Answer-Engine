import unittest
import QuestionAnswerEngineTask

class TestStringMethods(unittest.TestCase):

    def test_contains(self):
        self.assertEqual(QuestionAnswerEngineTask.contains('the coronavirus', 'coronavirus'), True)
        self.assertEqual(QuestionAnswerEngineTask.contains('the coronavirus', 'coronavirus time'), True)
        self.assertEqual(QuestionAnswerEngineTask.contains('the coronavirus', 'time'), False)
        self.assertEqual(QuestionAnswerEngineTask.contains('about 21 percent', 'what percent'), True)
        self.assertEqual(QuestionAnswerEngineTask.contains('test', 'has'), False)
        self.assertEqual(QuestionAnswerEngineTask.contains('coronavirus antibodies', 'the coronavirus'), True)
        self.assertEqual(QuestionAnswerEngineTask.contains('the states wadsworth facility', 'the coronavirus'), False)
if __name__ == '__main__':
    unittest.main()