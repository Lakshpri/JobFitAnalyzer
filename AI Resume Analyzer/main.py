from resume_analyzer import analyze_resume_text
from extract_text_easyocr import extract_text_easyocr  

def main():
    # Path to resume image
    image_path = "resume.png"  # Change this to your resume file path
    
    # Step 1: Extract text using OCR
    print("Extracting text from resume...")
    extracted_text = extract_text_easyocr(image_path)
    
    if not extracted_text.strip():
        print("Error: No text was extracted from the resume image.")
        return
    
    # Save extracted text (optional)
    with open("extracted_resume_text.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    # Step 2: Analyze the extracted text
    print("\nAnalyzing resume...")
    report, visual_summary = analyze_resume_text(extracted_text)
    
    # Step 3: Display and save results
    print("\n" + report)
    print("\n" + visual_summary)
    
    # Save the report to a file
    with open("resume_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\nAnalysis complete! Results saved to:")
    print("- resume_analysis_report.txt")
    print("- resume_analysis_summary.png")

if __name__ == "__main__":
    main()