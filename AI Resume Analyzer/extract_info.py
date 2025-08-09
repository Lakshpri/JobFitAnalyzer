import re
import easyocr

def extract_contact_info(text):
    email = re.findall(r'\b[\w.-]+@[\w.-]+\.\w{2,4}\b', text)
    phone = re.findall(r'\b\d{10,15}\b', text)  # Simple phone number (10-15 digits)
    return email, phone

def extract_skills(text):
    skills = []
    skill_section = re.search(r'(Skills|Technical Skills|Key Skills)(.*?)(Education|Experience|$)', text, re.DOTALL | re.IGNORECASE)
    if skill_section:
        skills_text = skill_section.group(2)
        skills = [skill.strip() for skill in re.split(r'[,;\n]', skills_text) if skill.strip()]
    return skills

def extract_education(text):
    education = []
    edu_section = re.search(r'(Education)(.*?)(Experience|Skills|$)', text, re.DOTALL | re.IGNORECASE)
    if edu_section:
        edu_text = edu_section.group(2)
        lines = [line.strip() for line in edu_text.split('\n') if line.strip()]
        education.extend(lines)
    return education

def extract_experience(text):
    experience = []
    exp_section = re.search(r'(Experience|Work Experience)(.*?)(Education|Skills|$)', text, re.DOTALL | re.IGNORECASE)
    if exp_section:
        exp_text = exp_section.group(2)
        lines = [line.strip() for line in exp_text.split('\n') if line.strip()]
        experience.extend(lines)
    return experience

if __name__ == "__main__":
    print("Starting extraction...")

    try:
        with open("resume_text.txt", "r", encoding="utf-8") as f:
            resume_text = f.read()
    except FileNotFoundError:
        print("ERROR: resume_text.txt not found! Make sure it's in the same folder.")
        exit()

    print(f"Read resume_text.txt, length: {len(resume_text)} characters")

    emails, phones = extract_contact_info(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    experience = extract_experience(resume_text)

    print("\n=== Extracted Info ===")
    print("Emails found:", emails)
    print("Phones found:", phones)
    print("Skills:", skills)
    print("Education:", education)
    print("Experience:", experience)

