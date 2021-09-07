# Gab tidy data tool

This is a little Python script to take Gab data output from [Garc][garc] and ingest it 
into relational form in an SQLite database.

This tool is designed from an academic research viewpoint.

## Usage instructions

### Prerequisites

- Python 3.8+
- Git

This tool requires Python 3.8 or later, the instructions assume you already have Python
installed. If you haven't installed Python before, you might
find [Python for Beginners][python_beginners] helpful - note that Gab Tidy Data is a 
command line application, you don't need to write any Python code to use it (although
you can if you want to), you just need to be able to run Python code!

The instructions assume sufficient familiarity with using a command line to change
directories and execute commands. If you are new to the command line or want a 
refresher, there are some good lessons from [Software Carpentry][sc_unix_intro] and
the [Programming Historian][ph_bash_intro].

The instructions assume you are working in a suitable Python 
[virtual environment][py_venv]. RealPython has a relatively straightforward 
[primer on virtual environments][realpy_venv] if you are new to the concept. If you
installed Python with Anaconda/conda, you will want to manage your virtual environments
through [Anaconda][anaconda_venv]/[conda][conda_venv] as well.

### Download and Installation

1. Ensure you are using an appropriate Python or Anaconda virtual environment

2. Install Gab Tidy Data and its requirements by running:

   `python -m pip install gab_tidy_data`

3. Run the following to check that your environment is ready to run Gab Tidy Data:
   
    `gab_tidy_data --help`

### Usage

In your command line, ensuring you are using the Python or Anaconda virtual environment
you used to install Gab Tidy Data requirements, you can run the `gab_tidy_data` command:

```
gab_tidy_data [data_file_1.jsonl] [data_file_2.jsonl] [database_name.db]
```

You may run the command with as many or as few JSON files (`.json` or `.jsonl`) as you
like, and they will all be loaded into the database specified. The database filename
must be the last argument provided to the `gab_tidy_data` command.


[Garc]: https://github.com/ChrisStevens/garc
[github_repo]: https://github.com/QUT-Digital-Observatory/gab_tidy_data
[python_beginners]: https://www.python.org/about/gettingstarted/
[sc_unix_intro]: https://swcarpentry.github.io/shell-novice/
[ph_bash_intro]: https://programminghistorian.org/en/lessons/intro-to-bash
[py_venv]: https://docs.python.org/3/tutorial/venv.html
[realpy_venv]: https://realpython.com/python-virtual-environments-a-primer/
[conda_venv]: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
[anaconda_venv]: https://docs.anaconda.com/anaconda/navigator/getting-started/#navigator-managing-environments
