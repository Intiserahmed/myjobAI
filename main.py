import subprocess
import requests
import json
import os

# ================
# Configuration
# ================
GEMINI_API_ENDPOINT = "https://your-gemini-api.endpoint"  # Replace with your actual endpoint
GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your API key if required

# ================
# API Call Function
# ================
def call_gemini_api(job_description: str, current_section: str) -> str:
    """
    Call Gemini API to update a LaTeX resume section based on the job description.
    
    Parameters:
        job_description (str): The job description text.
        current_section (str): The current LaTeX section content.
    
    Returns:
        str: The updated LaTeX content for that section.
    """

    # Construct the prompt for the Gemini API.
    prompt = (
        "You are a resume tailoring assistant. Given the following job description and the candidate's "
        "experience section, rewrite the section to emphasize the candidate's skills and experience relevant "
        "to the job. Return the text in valid LaTeX format.\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Current Experience Section:\n"
        f"{current_section}\n\n"
        "Rewrite the Experience Section:"
    )

    # Prepare the request payload
    payload = {
        "prompt": prompt,
        "max_tokens": 500,  # Adjust based on your expected output length
        # Add any other parameters required by the Gemini API
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"  # if using bearer token auth
    }

    try:
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        updated_text = response.json().get("updated_text")
        if not updated_text:
            print("Warning: No updated text found in API response. Using original section.")
            return current_section
        return updated_text
    except requests.exceptions.RequestException as e:
        print("API call failed:", e)
        # Fallback: return the original section in case of failure
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
    Compile the main LaTeX file into a PDF using latexmk.
    """
    try:
        subprocess.run(["latexmk", "-pdf", "main.tex"], check=True)
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

