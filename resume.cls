\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2025/04/11 Custom Resume Class]

\LoadClass[12pt]{article}

% Load required packages
\RequirePackage[margin=1in]{geometry}
\RequirePackage{enumitem}
\RequirePackage{titlesec}
\RequirePackage{hyperref}

% Custom command for resume items
\newcommand{\resumeItem}[2]{%
  \item \textbf{#1} --- #2%
}

% Environment for resume sections
\newenvironment{resumesection}[1]{%
   \section*{#1}%
   \begin{itemize}[leftmargin=*]%
}{%
   \end{itemize}%
}

\endinput
