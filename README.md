# SimplePythonTemplate

## To Run
1. Install MiniConda environment on your platform and create a new virtual environment
2. Create the virtual environment from the supplied environment.yml file `conda env create -f environment.yml`
3. Run the main.py script through your virtual environment

*Optionally* For visualization of TriMesh geometry you may need to add an additional dependency as a binary to your
$PATH environment variable. Download at
https://www.patrickmin.com/binvox/

## File and Folder Structure
```
├── main.py
├── requirements.txt
├── res/
└── src/
    ├── interfaces/
    └── SP/
```
`main.py` is the main entry point of the software \
`requirements.txt` specifies all the 3rd party dependencies that this project relies on \
`res/` short for *resources*; contains any additional binaries that are necessary for temporary, local storage, i.e. scene description, etc. \
`permRes/` short for *permanent resources*; contains any additional resources that should come with the project, i.e. models or dummy-data \
`src/` short for *source*; location of the source code modules \
