# 1/ Environment Setup

## 1.1/ Prerequisites
- VSCode with the "Jupyter" extension (Microsoft)
- Python 3.12
- Git

## 1.2/ Installation Steps

1/ **Clone the repository**
```bash
git clone https://github.com/Matthieu-BRANTHOME/Pyrates_LLM
cd Pyrates_LLM
```

2/ **Create a Python virtual environment**
```bash
python3.12 -m venv .venv
```

3/ **Activate the virtual environment**
```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

4/ **Install dependencies**
```bash
pip install -r requirements.txt
```

5/ **Configure VSCode**
- Open the project in VSCode
- Open any notebook (.ipynb file)
- Click on "Select Kernel" in the top right corner
- Choose the `.venv` interpreter

# 2/ Execution

Execute the notebooks sequentially in numerical order (i.e., `01_*.ipynb`, `02_*.ipynb`, etc.)

# 3/ Development Guidelines

## 3.1/ Adding Dependencies
When installing new packages (in venv):
```bash
pip install <package-name>
pip freeze > requirements.txt
```

## 3.2/ Before Committing

**Always perform these checks:**

1/ **Verify all notebooks run successfully**
   - Restart kernel and run all cells in each notebook
   - Ensure no errors occur

2/ **Clear all outputs and metadata**
   - In venv terminal type:
```bash
   nbstripout notebooks/*.ipynb
```

## 3.3/ Git Workflow
```bash
# Create a feature branch
git checkout -b feature/<your-feature-name>

# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Description of changes"

# Push to remote
git push origin feature/your-feature-name
```
Then create a Pull Request for review (via GitHub or VSCode "GitHub Pull Requests" extension)

# 4/ Project architecture

## 4.1/ Global

- `asset/*` > Graphic resources used for notebook presentation
- `data/cleaned/*` > Cleaned data usable for manual verification with a spreadsheet tool
- `data/raw/*` > Raw data from experiments
- `data/interim/*` > Cleaned data usable by analysis notebooks
- `debug/*` > Data files created during processing for debugging
- `notebooks/*` > Various notebooks constituting the project that must be executed sequentially in numerical order
- `outputs/*` > Graphs generated during analyses by the different notebooks
- `src/*` > Python files containing constants and functions shared by all notebooks
- `.gitignore` > Git exclusion management file
- `README.md` > Project documentation
- `requirements.txt` > File containing the project's Python dependencies

## 4.2/ Notebooks

- `notebooks/01_data_cleaning.ipynb` > Cleaning and filtering of raw data
- `notebooks/02_analysis_axis_1.ipynb` > Analyses related to axis 1: impact of the digital assistant on the learner
- `notebooks/03_analysis_axis_2.ipynb` > Analyses related to axis 2: usage of the digital assistant by learners
- `notebooks/04_analysis_axis_3.ipynb` > Analyses related to axis 3: evaluation of feedback content

## 4.3/ Constants

- `src/interaction_constants.py` > Constants defining column names and values for interaction trace data
- `src/session_date_constants.py` > Constants defining the dates of the different experimental sessions
- `src/students_constants.py` > Constants defining the students in the experiment
- `src/tests_constants.py` > Constants defining column names and values for pre-test and post-test data