# Virtual Environment Analyzer

A Python script that analyzes directories to find virtual environment (venv) folders and displays information about their size and count. **Now with cleanup functionality to delete large venv folders and automatically clean unused venvs based on access time!**

## Features

- **Comprehensive Detection**: Identifies various types of virtual environment folders including:

  - `venv`, `env`, `.venv`, `.env`
  - `virtualenv`, `virtual_env`, `python_env`, `pyenv`
  - Folders containing `Scripts/`, `bin/`, `pyvenv.cfg`, or activation scripts

- **Size Analysis**: Calculates and displays the total size of each venv folder
- **Human-readable Output**: Sizes are displayed in human-readable format (KB, MB, GB, etc.)
- **Flexible Search**: Supports custom directory paths and search depth limits
- **Error Handling**: Gracefully handles permission errors and inaccessible directories
- **Verbose Mode**: Option to show detailed information about each venv folder
- **🆕 Cleanup Mode**: Option to delete the top 5 largest venv folders to free up disk space
- **🆕 Unused Venv Detection**: Automatically identifies and cleans venv folders that haven't been accessed recently

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze the current directory:

```bash
python venv_analyzer.py
```

Analyze a specific directory:

```bash
python venv_analyzer.py /path/to/your/directory
```

### Advanced Options

**Verbose output** - Show detailed information about each venv folder:

```bash
python venv_analyzer.py -v
```

**Limit search depth** - Only search up to 3 levels deep:

```bash
python venv_analyzer.py --max-depth 3
```

**🆕 Auto-delete mode** - Offer to delete the top 5 largest venv folders:

```bash
python venv_analyzer.py --auto-delete
```

**🆕 Clean unused venvs** - Clean venv folders that haven't been accessed in 30+ days:

```bash
python venv_analyzer.py --clean-unused 30
```

**Combine options** - Verbose output with depth limit and unused cleanup:

```bash
python venv_analyzer.py /path/to/dir -v --max-depth 5 --clean-unused 60
```

### Command Line Arguments

- `directory`: Directory to analyze (default: current directory)
- `-v, --verbose`: Show detailed information about each venv folder
- `--max-depth`: Maximum depth to search (default: unlimited)
- `--auto-delete`: Offer to delete the top 5 largest venv folders after analysis
- `--clean-unused DAYS`: Clean venv folders that have not been accessed in DAYS or more
- `-h, --help`: Show help message

## Example Output

### Standard Analysis

```
Searching for virtual environment folders in: C:\Users\username\Projects
This may take a moment for large directories...

============================================================
Virtual Environment Analysis Results
============================================================
Root Directory: C:\Users\username\Projects
Total venv folders found: 5
Total size: 3.2 GB
============================================================

Top 5 largest venv folders:
------------------------------------------------------------
1. project1/venv (UNUSED) - 1.2 GB
   Last accessed: 2024-01-15 10:30:45
2. project2/.venv - 567.3 MB
   Last accessed: 2024-03-20 14:22:10
3. project3/env (UNUSED) - 234.1 MB
   Last accessed: 2024-02-10 09:15:30
```

### With Unused Venv Cleanup

```
============================================================
Virtual Environment Analysis Results
============================================================
Root Directory: C:\Users\username\Projects
Total venv folders found: 5
Total size: 3.2 GB
Unused venv folders (>=30 days): 2
Unused venv size: 1.4 GB
============================================================

============================================================
Unused Virtual Environment Cleanup
============================================================
Found 2 unused venv folders (not accessed in 30+ days)
This would free up 1.4 GB of disk space.

Unused venv folders (sorted by last access time):
1. project1/venv (1.2 GB) - 45 days ago
2. project3/env (234.1 MB) - 35 days ago

Delete these unused venv folders? (y/N): y

⚠️  WARNING: This action cannot be undone!
Type 'DELETE' to confirm deletion: DELETE

Deleting 2 venv folders...
------------------------------------------------------------
✓ Deleted: project1/venv (1.2 GB)
✓ Deleted: project3/env (234.1 MB)

============================================================
Deletion Summary
============================================================
Successfully deleted: 2 folders
Failed to delete: 0 folders
Space freed: 1.4 GB
============================================================
```

## How Unused Detection Works

The script determines if a venv is unused by checking the access times of key files and directories:

1. **Access Time Tracking**: Monitors access times of:

   - The venv folder itself
   - `Scripts/` or `bin/` directories
   - `pyvenv.cfg` configuration file
   - Activation scripts (`activate`, `activate.bat`, `activate.ps1`)
   - Python executables (`python.exe`, `bin/python`)

2. **Threshold-based Detection**: A venv is considered unused if:

   - None of its key files have been accessed within the specified number of days
   - The threshold is configurable (e.g., 30, 60, 90 days)

3. **Smart Sorting**: Unused venvs are sorted by access time (oldest first) for prioritized cleanup

## Safety Features

The cleanup functionality includes several safety measures:

1. **Double Confirmation**: Requires both 'y' and typing 'DELETE' to proceed
2. **Preview**: Shows exactly which folders will be deleted and how much space will be freed
3. **Access Time Display**: Shows when each venv was last accessed
4. **Error Handling**: Gracefully handles permission errors during deletion
5. **Summary Report**: Shows deletion results including any failures
6. **Mutual Exclusion**: Cannot use both `--auto-delete` and `--clean-unused` simultaneously

## Use Cases

### Regular Maintenance

```bash
# Clean venvs unused for 30+ days
python venv_analyzer.py --clean-unused 30
```

### Deep Cleanup

```bash
# Clean venvs unused for 90+ days (more aggressive)
python venv_analyzer.py --clean-unused 90
```

### Analysis Only

```bash
# Just analyze without cleanup
python venv_analyzer.py -v
```

### Project-Specific Cleanup

```bash
# Clean unused venvs in a specific project directory
python venv_analyzer.py /path/to/projects --clean-unused 60
```

## How It Works

1. **Detection**: The script identifies venv folders by:

   - Checking folder names against common venv naming patterns
   - Looking for venv-specific files and directories (Scripts/, bin/, pyvenv.cfg, etc.)

2. **Size Calculation**: For each found venv folder, it:

   - Recursively traverses all subdirectories
   - Sums up the size of all files
   - Handles permission errors gracefully

3. **Access Time Analysis**: When unused detection is enabled:

   - Checks access times of key venv files and directories
   - Compares against the specified threshold
   - Identifies venvs that haven't been accessed recently

4. **Analysis**: The script provides:

   - Total count of venv folders found
   - Total combined size
   - Individual folder sizes sorted by size (largest first)
   - Access time information for each venv
   - Unused venv statistics

5. **Cleanup Options**:
   - **Auto-delete**: Offers to delete the top 5 largest venv folders
   - **Unused cleanup**: Offers to delete venvs based on access time
   - Shows preview of what will be deleted
   - Requires double confirmation for safety
   - Provides detailed deletion results

## Supported Virtual Environment Types

The script can detect various virtual environment implementations:

- **venv** (Python 3.3+ built-in)
- **virtualenv** (third-party tool)
- **conda** environments (basic detection)
- **pipenv** environments
- **poetry** environments
- Custom named environments

## Error Handling

The script handles various error scenarios:

- **Permission Errors**: Skips directories/files that can't be accessed
- **Invalid Paths**: Validates input directories before processing
- **Keyboard Interrupt**: Gracefully exits when interrupted (Ctrl+C)
- **Large Directories**: Provides progress feedback for long-running scans
- **Deletion Failures**: Reports any folders that couldn't be deleted
- **Access Time Errors**: Handles cases where access times can't be read

## Performance Considerations

- For very large directories, the script may take some time to complete
- Use the `--max-depth` option to limit search scope if needed
- The script skips inaccessible directories to avoid permission issues
- Deletion operations are performed with proper error handling
- Access time checking adds minimal overhead to the analysis

## Requirements

- Python 3.6 or higher
- `humanize` library (for human-readable file sizes)

## License

This script is provided as-is for educational and utility purposes.
