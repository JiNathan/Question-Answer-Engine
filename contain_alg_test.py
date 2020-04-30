import unittest
import QuestionAnswerEngineTask

class TestStringMethods(unittest.TestCase):

    def test_contains(self):
        self.assertEqual(QuestionAnswerEngineTask.contains('the coronavirus', 'coronavirus'), True)
        self.assertEqual(QuestionAnswerEngineTask.contains('the coronavirus', 'coronavirus time'), True)
        self.assertEqual(QuestionAnswerEngineTask.contains('the coronavirus', 'time'), False)

if __name__ == '__main__':
    unittest.main()