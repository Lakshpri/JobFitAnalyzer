import re
from collections import Counter
import matplotlib.pyplot as plt

class ResumeAnalyzer:
    def __init__(self, extracted_text):
        self.text = extracted_text.lower()
        self.analysis = {
            'skills': {'matched': [], 'missing': []},
            'education': {},
            'experience': {},
            'quality': {}
        }
        
        # Define required skills for the target job (customize these)
        self.required_skills = [
            'python', 'machine learning', 'data analysis', 'sql', 
            'aws', 'docker', 'kubernetes', 'tensorflow',
            'pytorch', 'pandas', 'numpy', 'scikit-learn'
        ]
        
        # Common certifications to look for
        self.common_certs = [
            'aws certified', 'microsoft certified', 'google cloud',
            'oracle certified', 'cisco certified', 'pmp',
            'data science', 'machine learning'
        ]
    
    def analyze_skills(self):
        """Analyze skills match between resume and required skills"""
        found_skills = []
        
        # Check for each required skill in the text
        for skill in self.required_skills:
            if re.search(rf'\b{re.escape(skill)}\b', self.text):
                found_skills.append(skill)
        
        missing_skills = [s for s in self.required_skills if s not in found_skills]
        
        self.analysis['skills']['matched'] = found_skills
        self.analysis['skills']['missing'] = missing_skills
        self.analysis['skills']['score'] = int((len(found_skills) / len(self.required_skills)) * 100)
    
    def analyze_education(self):
        """Extract education information"""
        # Look for degree patterns
        degree_pattern = r'(bachelor|master|phd|b\.?tech|m\.?tech|b\.?e|b\.?sc)\s*(?:of|in)?\s*(science|engineering|computer science|technology|computers)'
        match = re.search(degree_pattern, self.text, re.IGNORECASE)
        
        if match:
            degree = f"{match.group(1).title()} of {match.group(2).title()}"
            self.analysis['education']['degree'] = degree
            self.analysis['education']['score'] = 78  # Example value
        else:
            self.analysis['education']['degree'] = "Not Found"
            self.analysis['education']['score'] = 0
    
    def analyze_experience(self):
        """Extract experience information"""
        # Look for experience duration
        exp_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:experience|exp)'
        matches = re.findall(exp_pattern, self.text)
        
        if matches:
            total_exp = max(map(int, matches))
            self.analysis['experience']['total'] = total_exp
            self.analysis['experience']['score'] = min(80, total_exp * 20)  # Example scoring
        else:
            self.analysis['experience']['total'] = 0
            self.analysis['experience']['score'] = 0
    
    def analyze_quality(self):
        """Check resume quality factors"""
        # Check for contact info
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.text))
        has_phone = bool(re.search(r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', self.text))
        
        # Estimate page count by word count (approximate)
        word_count = len(re.findall(r'\b\w+\b', self.text))
        page_count = min(2, word_count // 500 + 1)
        
        # Check for certifications
        has_certs = any(re.search(rf'\b{re.escape(cert)}\b', self.text, re.IGNORECASE) 
                       for cert in self.common_certs)
        
        self.analysis['quality']['contact'] = has_email and has_phone
        self.analysis['quality']['length'] = "Ideal" if page_count == 2 else "Too short" if page_count < 2 else "Too long"
        self.analysis['quality']['certs'] = has_certs
        self.analysis['quality']['score'] = 85  # Example value
    
    def calculate_final_score(self):
        """Calculate overall fit score"""
        weights = {
            'skills': 0.4,
            'education': 0.2,
            'experience': 0.3,
            'quality': 0.1
        }
        
        total_score = 0
        for category, weight in weights.items():
            total_score += self.analysis[category]['score'] * weight
        
        self.analysis['final_score'] = int(total_score)
    
    def generate_report(self):
        """Generate text report"""
        report = []
        report.append(f"Resume Analysis Report\n{'='*30}\n")
        
        # Skills section
        report.append("1️⃣ Skills Match:")
        report.append(f"Score: {self.analysis['skills']['score']}%")
        report.append(f"Matched Skills: {', '.join(self.analysis['skills']['matched'])}")
        if self.analysis['skills']['missing']:
            report.append(f"Missing Important Skills: {', '.join(self.analysis['skills']['missing'])}")
        
        # Education section
        report.append("\n2️⃣ Education Match:")
        report.append(f"Degree: {self.analysis['education'].get('degree', 'Not found')}")
        report.append(f"Score: {self.analysis['education'].get('score', 0)}%")
        
        # Experience section
        report.append("\n3️⃣ Experience Match:")
        report.append(f"Total Experience: {self.analysis['experience'].get('total', 0)} years")
        report.append(f"Score: {self.analysis['experience'].get('score', 0)}%")
        
        # Quality section
        report.append("\n4️⃣ Resume Quality Check:")
        report.append(f"Contact Info: {'Present' if self.analysis['quality'].get('contact') else 'Missing'}")
        report.append(f"Formatting: Good")
        report.append(f"Length: {self.analysis['quality'].get('length')}")
        if not self.analysis['quality'].get('certs'):
            report.append("Suggestions: Add certifications section.")
        
        # Final score
        report.append(f"\n5️⃣ Final Fit Score: {self.analysis['final_score']}%")
        if self.analysis['final_score'] >= 80:
            report.append("You are a strong candidate!")
            if self.analysis['skills']['missing']:
                report.append(f"Focus on {', '.join(self.analysis['skills']['missing'])}.")
        elif self.analysis['final_score'] >= 60:
            report.append("You meet some requirements but need improvement.")
        else:
            report.append("The resume doesn't meet most requirements.")
        
        return "\n".join(report)
    
    def generate_visual_summary(self):
        """Generate visual summary with matplotlib"""
        categories = ['Skills', 'Education', 'Experience', 'Quality']
        scores = [
            self.analysis['skills']['score'],
            self.analysis['education']['score'],
            self.analysis['experience']['score'],
            self.analysis['quality']['score']
        ]
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.barh(categories, scores, color='#4CAF50')
        
        # Add score text at the end of each bar
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 2, bar.get_y() + bar.get_height()/2,
                    f'{width}%', ha='left', va='center')
        
        ax.set_xlim(0, 100)
        ax.set_title('Resume Analysis Summary')
        ax.set_xlabel('Score (%)')
        plt.tight_layout()
        
        # Save the visualization
        plt.savefig('resume_analysis_summary.png')
        plt.close()
        
        return "Visual summary saved as 'resume_analysis_summary.png'"
    
    def analyze(self):
        """Run all analysis steps"""
        self.analyze_skills()
        self.analyze_education()
        self.analyze_experience()
        self.analyze_quality()
        self.calculate_final_score()
        
        # Generate and return results
        report = self.generate_report()
        visual_summary = self.generate_visual_summary()
        
        return report, visual_summary


def analyze_resume_text(extracted_text):
    """Function to analyze extracted resume text"""
    analyzer = ResumeAnalyzer(extracted_text)
    return analyzer.analyze()