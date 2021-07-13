# Gab tidy data tool

This is a little Python script to take Gab data output from [Garc][garc] and ingest it 
into relational form in an SQLite database.

This tool is designed from an academic research viewpoint.

## Usage instructions

### Prerequisites

- Python 3.8
- Git

This tool requires Python 3.8 or later, the instructions assume you already have Python
installed. 

The instructions assume sufficient familiarity with using a command line to change
directories and execute commands.

The instructions assume you are working in a suitable environment (TODO: link to a nice
virtualenv guide)

### Download and Installation

1. In a command line, in the directory you wish the Gab Tidy Data code to sit within,
   clone the source code from [the Gab Tidy Data repository][github_repo]
    
2. Navigate into the root folder for Gab Tidy Data (the folder containing `setup.py` 
   and this readme file)
   
3. Ensure you are using an appropriate Python or Anaconda virtual environment

4. Install the requirements by running:

   `python -m pip install -r requirements.txt`

5. Run the following to check that your environment is ready to run Gab Tidy Data:
   
    `python gab_tidy_data --help`

### Usage

In your command line, ensuring you are using the Python or Anaconda virtual environment
you used to install Gab Tidy Data requirements, and that you are in the folder 
containing `setup.py` and this readme, you can run `python gab_tidy_data`:

```
python gab_tidy_data [data_file_1.jsonl] [data_file_2.jsonl] [database_name.db]
```

You may run the command with as many or as few JSON files (`.json` or `.jsonl`) as you
like, and they will all be loaded into the database specified. The database filename
must be the last argument provided to the `python gab_tidy_data` command.


[Garc]: https://github.com/ChrisStevens/garc
[github_repo]: https://github.com/QUT-Digital-Observatory/gab_tidy_data
