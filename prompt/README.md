![Logo AIED26](../assets/logo_AIED26.png)

# System Prompt source code

The `prompt/` folder contains the source files that manage the system prompt:
- `prompt/main.py`: Flask server entry point, retrieves information from the client and triggers the generation of the system prompt based on the feedback modality assigned to the student.
- `prompt/system_prompt_modality_B.py`: generation of the system prompt for modality B (free-content).
- `prompt/system_prompt_modality_C.py`: generation of the system prompt for modality C (constrained-content).