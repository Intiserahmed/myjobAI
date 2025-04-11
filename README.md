# 🧠 AI-Powered LaTeX Resume Tailoring Tool

**Customize your LaTeX resume automatically for any job using Gemini AI.**  
This open-source Python project reads a job description, tailors your resume sections (like *Experience*), and compiles a clean, professional PDF using `latexmk`.

Perfect for developers, engineers, and researchers using LaTeX who want an intelligent, automated way to generate tailored resumes for every job application.

---

## 🚀 Features

- 🎯 **AI Resume Optimization** using Google Gemini API
- 📄 **LaTeX-based Resume System** for professional formatting
- 🧩 **Modular Resume Sections** (experience, skills, summary, etc.)
- ⚙️ **Makefile Integration** for consistent, clean PDF builds
- 🔐 **Secure via Environment Variables** – no hardcoded keys

---

## 📋 Prerequisites

### ✅ 1. LaTeX Distribution

Install one of the following:

- **macOS:** [BasicTeX](https://tug.org/mactex/morepackages.html) or [MacTeX](https://tug.org/mactex/)
- **Windows/Linux:** [TeX Live](https://tug.org/texlive/)

Also ensure:
```bash
sudo tlmgr install latexmk


