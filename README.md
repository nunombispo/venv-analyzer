# Virtual Environment Analyzer

A Python script that analyzes directories to find virtual environment (venv) folders and displays information about their size and count. **Now with cleanup functionality to delete large venv folders!**

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

**Combine options** - Verbose output with depth limit and cleanup:

```bash
python venv_analyzer.py /path/to/dir -v --max-depth 5 --auto-delete
```

### Command Line Arguments

- `directory`: Directory to analyze (default: current directory)
- `-v, --verbose`: Show detailed information about each venv folder
- `--max-depth`: Maximum depth to search (default: unlimited)
- `--auto-delete`: Offer to delete the top 5 largest venv folders after analysis
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
Total venv folders found: 3
Total size: 2.1 GB
============================================================

Top 5 largest venv folders:
------------------------------------------------------------
1. project1/venv - 1.2 GB
2. project2/.venv - 567.3 MB
3. project3/env - 234.1 MB
```

### With Cleanup Mode

```
============================================================
Cleanup Option
============================================================
Would you like to delete the top 3 largest venv folders?
This would free up 2.0 GB of disk space.

1. project1/venv (1.2 GB)
2. project2/.venv (567.3 MB)
3. project3/env (234.1 MB)

Delete these folders? (y/N): y

⚠️  WARNING: This action cannot be undone!
Type 'DELETE' to confirm deletion: DELETE

Deleting 3 venv folders...
------------------------------------------------------------
✓ Deleted: project1/venv (1.2 GB)
✓ Deleted: project2/.venv (567.3 MB)
✓ Deleted: project3/env (234.1 MB)

============================================================
Deletion Summary
============================================================
Successfully deleted: 3 folders
Failed to delete: 0 folders
Space freed: 2.0 GB
============================================================
```

## Safety Features

The cleanup functionality includes several safety measures:

1. **Double Confirmation**: Requires both 'y' and typing 'DELETE' to proceed
2. **Preview**: Shows exactly which folders will be deleted and how much space will be freed
3. **Error Handling**: Gracefully handles permission errors during deletion
4. **Summary Report**: Shows deletion results including any failures

## How It Works

1. **Detection**: The script identifies venv folders by:

   - Checking folder names against common venv naming patterns
   - Looking for venv-specific files and directories (Scripts/, bin/, pyvenv.cfg, etc.)

2. **Size Calculation**: For each found venv folder, it:

   - Recursively traverses all subdirectories
   - Sums up the size of all files
   - Handles permission errors gracefully

3. **Analysis**: The script provides:

   - Total count of venv folders found
   - Total combined size
   - Individual folder sizes sorted by size (largest first)

4. **🆕 Cleanup**: When auto-delete is enabled:
   - Offers to delete the top 5 largest venv folders
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

## Performance Considerations

- For very large directories, the script may take some time to complete
- Use the `--max-depth` option to limit search scope if needed
- The script skips inaccessible directories to avoid permission issues
- Deletion operations are performed with proper error handling

## Requirements

- Python 3.6 or higher
- `humanize` library (for human-readable file sizes)

## License

This script is provided as-is for educational and utility purposes.
