import unittest
import numpy as np
from app.matching import FingerprintMatcher

class TestMatching(unittest.TestCase):
    def setUp(self):
        self.matcher = FingerprintMatcher(threshold=0.8)
        
        # Sample templates
        self.template1 = {
            'endings': [(10, 20), (30, 40), (50, 60)],
            'bifurcations': [(15, 25), (35, 45)],
            'num_points': 5
        }
        
        self.template2 = {
            'endings': [(11, 21), (31, 41), (51, 61)],
            'bifurcations': [(16, 26), (36, 46)],
            'num_points': 5
        }
        
        self.template3 = {
            'endings': [(100, 200)],
            'bifurcations': [],
            'num_points': 1
        }
    
    def test_vectorize_template(self):
        vector = self.matcher.vectorize_template(self.template1)
        self.assertEqual(len(vector), 3)
        self.assertEqual(vector[0], 3)  # endings
        self.assertEqual(vector[1], 2)  # bifurcations
        self.assertEqual(vector[2], 5)  # total points
    
    def test_similarity_calculation(self):
        vec1 = self.matcher.vectorize_template(self.template1)
        vec2 = self.matcher.vectorize_template(self.template2)
        
        similarity = self.matcher.calculate_similarity(vec1, vec2)
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 1)
    
    def test_template_matching(self):
        result = self.matcher.match_templates(self.template1, self.template2)
        self.assertIn('similarity', result)
        self.assertIn('is_match', result)
        
        # Similar templates should match
        result_diff = self.matcher.match_templates(self.template1, self.template3)
        # Different templates should not match (or have low similarity)
        self.assertLess(result_diff['similarity'], result['similarity'])

if __name__ == '__main__':
    unittest.main()