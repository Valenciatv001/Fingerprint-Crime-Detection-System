# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from scipy.spatial.distance import euclidean

# class FingerprintMatcher:
#     def __init__(self, threshold=0.85):
#         self.threshold = threshold
    
#     def vectorize_template(self, template):
#         """Convert template to feature vector"""
#         endings = len(template['endings'])
#         bifurcations = len(template['bifurcations'])
#         total_points = template['num_points']
        
#         # Additional features could be added here
#         return np.array([endings, bifurcations, total_points])
    
#     def calculate_similarity(self, vec1, vec2):
#         """Calculate combined similarity score"""
#         # Cosine similarity
#         cos_sim = cosine_similarity([vec1], [vec2])[0][0]
        
#         # Normalized Euclidean distance (inverse)
#         max_val = max(np.linalg.norm(vec1), np.linalg.norm(vec2)) or 1
#         euc_dist = euclidean(vec1, vec2) / max_val
#         euc_sim = 1 - min(euc_dist, 1)
        
#         # Combined score (weighted average)
#         combined_score = 0.7 * cos_sim + 0.3 * euc_sim
        
#         return combined_score
    
#     # def match_templates(self, template1, template2):
#     #     """Match two fingerprint templates"""
#     #     vec1 = self.vectorize_template(template1)
#     #     vec2 = self.vectorize_template(template2)
        
#     #     similarity = self.calculate_similarity(vec1, vec2)
#     #     is_match = similarity >= self.threshold
        
#     #     return {
#     #         'similarity': similarity,
#     #         'is_match': is_match,
#     #         'threshold': self.threshold
#     #     }

#     def match_templates(self, template1, template2):
#           """Match two fingerprint templates"""
#           vec1 = self.vectorize_template(template1)
#           vec2 = self.vectorize_template(template2)
    
#           similarity = self.calculate_similarity(vec1, vec2)
#           is_match = bool(similarity >= self.threshold)  # Convert to bool
    
#           return {
#         'similarity': float(similarity),  # Convert to float
#         'is_match': is_match,
#         'threshold': float(self.threshold)  # Convert to float
#     }
    
#     # def find_best_match(self, query_template, database_templates):
#     #     """Find best match from database templates"""
#     #     best_match = None
#     #     best_score = 0
#     #     matches = []
        
#     #     for template_id, template_data in database_templates.items():
#     #         result = self.match_templates(query_template, template_data)
#     #         matches.append({
#     #             'template_id': template_id,
#     #             'similarity': result['similarity'],
#     #             'is_match': result['is_match']
#     #         })
            
#     #         if result['similarity'] > best_score:
#     #             best_score = result['similarity']
#     #             best_match = template_id
        
#     #     return {
#     #         'best_match': best_match,
#     #         'best_score': best_score,
#     #         'all_matches': sorted(matches, key=lambda x: x['similarity'], reverse=True)
#     #     }



# # In app/matching.py, update the find_best_match method:

# def find_best_match(self, query_template, database_templates):
#     """Find best match from database templates"""
#     best_match = None
#     best_score = 0
#     matches = []
    
#     for template_id, template_data in database_templates.items():
#         result = self.match_templates(query_template, template_data)
        
#         # Convert numpy types to Python native types for JSON serialization
#         matches.append({
#             'template_id': template_id,
#             'similarity': float(result['similarity']),  # Convert to float
#             'is_match': bool(result['is_match'])        # Convert to bool
#         })
        
#         if result['similarity'] > best_score:
#             best_score = result['similarity']
#             best_match = template_id
    
#     # Convert best_score to float for JSON serialization
#     best_score = float(best_score)
    
#     response = {
#         'best_match': best_match,
#         'best_score': best_score,
#         'matches_found': len([m for m in matches if m['is_match']]),
#         'all_matches': sorted(matches, key=lambda x: x['similarity'], reverse=True)[:10]
#     }
    
#     if best_match:
#         response['matched_user_id'] = database_templates[best_match]['user_id']
    
#     return response



import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean

class FingerprintMatcher:
    def __init__(self, threshold=0.85):
        self.threshold = threshold
    
    def vectorize_template(self, template):
        """Convert template to feature vector"""
        endings = len(template['endings'])
        bifurcations = len(template['bifurcations'])
        total_points = template['num_points']
        
        # Additional features could be added here
        return np.array([endings, bifurcations, total_points])
    
    def calculate_similarity(self, vec1, vec2):
        """Calculate combined similarity score"""
        # Cosine similarity
        cos_sim = cosine_similarity([vec1], [vec2])[0][0]
        
        # Normalized Euclidean distance (inverse)
        max_val = max(np.linalg.norm(vec1), np.linalg.norm(vec2)) or 1
        euc_dist = euclidean(vec1, vec2) / max_val
        euc_sim = 1 - min(euc_dist, 1)
        
        # Combined score (weighted average)
        combined_score = 0.7 * cos_sim + 0.3 * euc_sim
        
        return combined_score
    
    def match_templates(self, template1, template2):
        """Match two fingerprint templates"""
        vec1 = self.vectorize_template(template1)
        vec2 = self.vectorize_template(template2)
        
        similarity = self.calculate_similarity(vec1, vec2)
        is_match = bool(similarity >= self.threshold)
        
        return {
            'similarity': float(similarity),
            'is_match': is_match,
            'threshold': float(self.threshold)
        }
    
    def find_best_match(self, query_template, database_templates):
        """Find best match from database templates"""
        best_match = None
        best_score = 0
        matches = []
        
        for template_id, template_data in database_templates.items():
            result = self.match_templates(query_template, template_data)
            
            # Convert numpy types to Python native types for JSON serialization
            matches.append({
                'template_id': template_id,
                'similarity': float(result['similarity']),
                'is_match': bool(result['is_match'])
            })
            
            if result['similarity'] > best_score:
                best_score = result['similarity']
                best_match = template_id
        
        response = {
            'best_match': best_match,
            'best_score': float(best_score),
            'matches_found': len([m for m in matches if m['is_match']]),
            'all_matches': sorted(matches, key=lambda x: x['similarity'], reverse=True)[:10]
        }
        
        if best_match and best_match in database_templates:
            response['matched_user_id'] = database_templates[best_match].get('user_id')
        
        return response