![Logo AIED26](../assets/logo_AIED26.png)

This repository contains supplementary materials accompanying the paper  
**“Embedding Pedagogical Principles into LLMs: A Field Study of AI-Generated Feedback in a Programming Serious Game.”**

# System Prompt source code

The `prompt/` folder contains the source files that manage the system prompt:
- `prompt/main.py`: Flask server entry point, retrieves information from the client and triggers the generation of the system prompt based on the feedback modality assigned to the student.
- `prompt/system_prompt_modality_B.py`: generation of the system prompt for modality B (free-content).
- `prompt/system_prompt_modality_C.py`: generation of the system prompt for modality C (constrained-content).