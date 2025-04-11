import subprocess
import requests
import json
import os
from google import generativeai as genai

# ================
# Configuration
# ================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Must be set, otherwise raise error

if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable is not set!")

# ================
# API Call Function
# ================

def call_gemini_api(job_description: str, current_section: str) -> str:
    """
    Call Gemini API (via google.generativeai) to update a LaTeX resume section based on the job description.
    
    Parameters:
        job_description (str): The job description text.
        current_section (str): The current LaTeX section content.
    
    Returns:
        str: The updated LaTeX content for that section.
    """
    # Construct the prompt(s) to send to Gemini.
    # Using multiple text parts for clarity (similar to your working Gemini code).
    contents = [
        {
            "role": "user",
            "parts": [
                {"text": "You are a resume tailoring assistant. Given the following job description and the candidate's experience section, "
                          "rewrite the section to emphasize the candidate's skills and experience relevant to the job. Return the text in valid LaTeX format."},
                {"text": "\nJob Description:"},
                {"text": job_description},
                {"text": "\nCurrent Experience Section:"},
                {"text": current_section},
                {"text": "\nRewrite the Experience Section:"}
            ]
        }
    ]
    
    try:
        # Configure the Gemini API with your API key.
        genai.configure(api_key=GEMINI_API_KEY)
        # Instantiate the model (you can replace "gemini-2.0-flash" with your desired model name)
        model = genai.GenerativeModel("gemini-2.0-flash")
        # Generate content using the constructed contents.
        response = model.generate_content(contents=contents)
        # Return the generated text.
        return response.text
    except Exception as e:
        print("❌ Error calling Gemini API:", e)
        # Return the original section as a fallback.
        return current_section

# ================
# Update LaTeX Section
# ================
def update_section(filepath: str, content: str) -> None:
    """
    Write content to the specified file.
    
    Parameters:
        filepath (str): Path to the LaTeX file to update.
        content (str): The new content to write.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath} successfully.")
    except IOError as e:
        print(f"Failed to update {filepath}: {e}")

# ================
# Compile LaTeX to PDF
# ================
def compile_resume() -> None:
    """
    Clean auxiliary files and compile the main LaTeX file into a PDF using latexmk.
    This forces a full rebuild so that new changes are always reflected.
    """
    try:
        # Clean auxiliary files
        subprocess.run(["latexmk", "-C", "main.tex"], check=True)
        # Force a full rebuild even if the files are "up-to-date"
        subprocess.run(["latexmk", "-pdf", "-g", "main.tex"], check=True)
        print("✅ Resume compiled successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ LaTeX compilation failed:", e)

# ================
# Main Automation Function
# ================
def main():
    # Ensure the working directory is set to your LaTeX project folder if needed
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # 1. Get job description input from the user.
    print("Enter the job description (finish input with an empty line):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    job_description = "\n".join(lines)

    # 2. Read your current experience section from LaTeX.
    experience_path = os.path.join("sections", "experience.tex")
    try:
        with open(experience_path, 'r', encoding='utf-8') as f:
            current_experience = f.read()
    except IOError as e:
        print(f"Error reading {experience_path}: {e}")
        return

    # 3. Get updated content from the Gemini API.
    print("Contacting Gemini API to update your resume section...")
    updated_experience = call_gemini_api(job_description, current_experience)

    # 4. Write the updated content back to the LaTeX file.
    update_section(experience_path, updated_experience)

    # 5. Compile the LaTeX resume to generate a PDF.
    print("Compiling the updated LaTeX resume to PDF...")
    compile_resume()

if __name__ == "__main__":
    main()
