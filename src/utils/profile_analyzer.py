class ProfileAnalyzer:
    def __init__(self, target_criteria):
        self.criteria = target_criteria
    
    def analyze_profile(self, profile_data):
        activity_score = self._score_activity(profile_data['activity'])
        experience_fit = self._check_experience_fit(profile_data['experience'])
        company_fit = self._check_company_fit(profile_data['company'])
        
        return {
            'is_target': all([activity_score > 0.7, experience_fit, company_fit]),
            'activity_score': activity_score,
            'recommended_template': self._get_template_type(profile_data)
        }
    
    def _get_template_type(self, profile_data):
        if "new role" in profile_data['activity'].lower():
            return "new_joiner"
        elif "posted" in profile_data['activity'].lower():
            return "content_creator"
        return "experienced"
