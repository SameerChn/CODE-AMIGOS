import utils
import sys

def test_gemini_functions():
    """Test if the Gemini analysis functions in utils.py are working correctly."""
    print("\n===== Testing Gemini Analysis Functions =====\n")
    
    # Test sample data
    sample_resume = """
    John Doe
    Software Engineer
    
    Experience:
    - Senior Developer at Tech Corp (2018-Present)
      * Developed web applications using React and Node.js
      * Led a team of 5 developers
    - Junior Developer at Startup Inc (2015-2018)
      * Built RESTful APIs using Python and Flask
    
    Skills:
    - Programming: Python, JavaScript, Java
    - Web: React, Node.js, HTML, CSS
    - Database: MongoDB, PostgreSQL
    - Tools: Git, Docker, AWS
    
    Education:
    - Bachelor of Science in Computer Science, University (2015)
    """
    
    sample_job = """
    Senior Software Engineer
    
    We are looking for a Senior Software Engineer with experience in web development.
    
    Requirements:
    - 5+ years of experience in software development
    - Strong knowledge of JavaScript and React
    - Experience with Node.js and RESTful APIs
    - Familiarity with cloud services (AWS/Azure/GCP)
    - Good communication skills
    
    Responsibilities:
    - Develop and maintain web applications
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Participate in code reviews
    """
    
    # Test resume analysis
    print("Testing analyze_resume_with_gemini()...")
    try:
        resume_analysis = utils.analyze_resume_with_gemini(sample_resume)
        if resume_analysis:
            print("✅ Resume analysis successful!")
            print("\nSample output (first 200 chars):")
            print(resume_analysis[:200] + "...")
        else:
            print("❌ Resume analysis failed - returned None")
    except Exception as e:
        print(f"❌ Resume analysis failed with error: {str(e)}")
    
    # Test job description analysis
    print("\nTesting analyze_job_description_with_gemini()...")
    try:
        job_analysis = utils.analyze_job_description_with_gemini(sample_job, sample_resume)
        if job_analysis:
            print("✅ Job description analysis successful!")
            print("\nSample output (first 200 chars):")
            print(job_analysis[:200] + "...")
        else:
            print("❌ Job description analysis failed - returned None")
    except Exception as e:
        print(f"❌ Job description analysis failed with error: {str(e)}")
    
    # Check if both functions worked
    if resume_analysis and job_analysis:
        return True
    else:
        return False

if __name__ == "__main__":
    success = test_gemini_functions()
    
    print("\n===== Summary =====")
    if success:
        print("✅ Gemini analysis functions are working correctly!")
        print("The application should be able to analyze resumes and job descriptions.")
    else:
        print("❌ Some Gemini analysis functions failed.")
        print("Possible issues:")
        print("1. API quota exceeded")
        print("2. Model availability issues")
        print("3. Implementation errors in the functions")
        print("\nCheck the specific error messages above for more details.")