from typing import Dict, Any
import logging

class ProfileAnalyzer:
    def __init__(self, target_criteria: Dict[str, Any] = None):
        """Initialize ProfileAnalyzer with target criteria
        
        Args:
            target_criteria: Optional dictionary to override default criteria
        """
        self.witch_companies = {
            'wipro': ['wipro limited', 'wipro technologies'],
            'infosys': ['infosys limited', 'infosys technologies'],
            'tcs': ['tata consultancy services', 'tcs'],
            'cognizant': ['cognizant technology solutions', 'cts'],
            'hcl': ['hcl technologies', 'hcl tech']
        }
        
        self.default_criteria = {
            'min_experience': 0,
            'max_experience': 5,
            'target_companies': [comp for sublist in self.witch_companies.values() for comp in sublist]
        }
        
        self.criteria = self.default_criteria
        if target_criteria:
            self.criteria.update(target_criteria)
    
    def analyze_profile(self, profile_data: Dict) -> Dict:
        """Analyze a profile and return scoring results
        
        Args:
            profile_data: Dictionary containing profile information
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            experience_fit = self._check_experience_fit(profile_data.get('experience', 0))
            company_fit = self._check_company_fit(profile_data.get('company', ''))
            
            # We care more about company (0.6) than experience (0.4)
            total_score = (company_fit * 0.6 + experience_fit * 0.4)
            
            return {
                'is_target': total_score > 0.7,
                'total_score': round(total_score, 2),
                'experience_fit': round(experience_fit, 2),
                'company_fit': round(company_fit, 2),
                'company_name': self._get_company_name(profile_data.get('company', '')),
                'recommended_template': self._get_template_type(profile_data)
            }
            
        except Exception as e:
            logging.error(f"Error analyzing profile: {str(e)}")
            return {
                'is_target': False,
                'error': str(e)
            }
    
    def _check_experience_fit(self, experience: Any) -> float:
        """Check if experience level fits target criteria (0-5 years)
        
        Returns:
            Float between 0 and 1 indicating experience fit
        """
        try:
            if isinstance(experience, str):
                if experience.isdigit():
                    experience = int(experience)
                else:
                    return 0.0  # If we can't determine experience, don't target
            
            if not isinstance(experience, (int, float)):
                return 0.0
                
            min_exp = self.criteria['min_experience']
            max_exp = self.criteria['max_experience']
            
            if min_exp <= experience <= max_exp:
                return 1.0
            elif experience < min_exp:
                return 0.5  # Fresh graduates might be good targets
            else:
                return 0.0  # Don't target those with more experience
                
        except Exception as e:
            logging.warning(f"Error checking experience fit: {str(e)}")
            return 0.0
    
    def _check_company_fit(self, company: str) -> float:
        """Check if current company is a WITCH company
        
        Returns:
            Float between 0 and 1 indicating company fit
        """
        if not company:
            return 0.0
            
        company = company.lower()
        
        # Check for exact matches with WITCH companies
        for company_variants in self.witch_companies.values():
            if any(variant in company for variant in company_variants):
                return 1.0
                
        return 0.0  # Not a WITCH company
    
    def _get_company_name(self, company: str) -> str:
        """Get standardized company name if it's a WITCH company"""
        if not company:
            return "Unknown"
            
        company = company.lower()
        
        for name, variants in self.witch_companies.items():
            if any(variant in company for variant in variants):
                return name.upper()
                
        return "Other"
    
    def _get_template_type(self, profile_data: Dict) -> str:
        """Determine the best message template type based on profile data"""
        experience = profile_data.get('experience', 0)
        company = profile_data.get('company', '').lower()
        
        if isinstance(experience, (int, float)):
            if experience < 1:
                return "fresher"
            elif experience < 3:
                return "early_career"
            else:
                return "experienced"
        
        return "standard"
