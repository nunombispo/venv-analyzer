#!/usr/bin/env python3
"""
Virtual Environment Analyzer

This script analyzes a directory to find virtual environment (venv) folders
and displays information about their size and count.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import humanize


def is_venv_folder(path: Path) -> bool:
    """
    Check if a directory is a virtual environment folder.
    
    Args:
        path: Path to the directory to check
        
    Returns:
        bool: True if it's a venv folder, False otherwise
    """
    # Common venv folder names
    venv_names = {
        'venv', 'env', '.venv', '.env', 'virtualenv', 
        'virtual_env', 'python_env', 'pyenv'
    }
    
    # Check if the folder name matches common venv patterns
    if path.name in venv_names:
        return True
    
    # Check for common venv indicators
    venv_indicators = [
        'Scripts',  # Windows
        'bin',      # Unix/Linux
        'pyvenv.cfg',
        'activate',
        'activate.bat',
        'activate.ps1'
    ]
    
    for indicator in venv_indicators:
        if (path / indicator).exists():
            return True
    
    return False


def get_directory_size(path: Path) -> int:
    """
    Calculate the total size of a directory in bytes.
    
    Args:
        path: Path to the directory
        
    Returns:
        int: Size in bytes
    """
    total_size = 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                try:
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
                except (OSError, PermissionError):
                    # Skip files we can't access
                    continue
    except (OSError, PermissionError):
        # Skip directories we can't access
        pass
    
    return total_size


def find_venv_folders(root_path: Path, max_depth: int = None) -> List[Path]:
    """
    Recursively find all virtual environment folders in the given directory.
    
    Args:
        root_path: Root directory to search
        max_depth: Maximum depth to search (None for unlimited)
        
    Returns:
        List[Path]: List of venv folder paths
    """
    venv_folders = []
    
    def search_recursive(path: Path, current_depth: int = 0):
        if max_depth is not None and current_depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                if item.is_dir():
                    # Check if this is a venv folder
                    if is_venv_folder(item):
                        venv_folders.append(item)
                    else:
                        # Continue searching in subdirectories
                        search_recursive(item, current_depth + 1)
        except (OSError, PermissionError):
            # Skip directories we can't access
            pass
    
    search_recursive(root_path)
    return venv_folders


def analyze_venv_folders(venv_folders: List[Path]) -> Dict:
    """
    Analyze the found venv folders and return statistics.
    
    Args:
        venv_folders: List of venv folder paths
        
    Returns:
        Dict: Analysis results
    """
    total_size = 0
    folder_sizes = []
    
    for folder in venv_folders:
        try:
            size = get_directory_size(folder)
            total_size += size
            folder_sizes.append((folder, size))
        except (OSError, PermissionError):
            # Skip folders we can't access
            continue
    
    # Sort by size (largest first)
    folder_sizes.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'count': len(venv_folders),
        'total_size': total_size,
        'folder_sizes': folder_sizes
    }


def delete_venv_folders(folders_to_delete: List[Tuple[Path, int]], root_path: Path) -> Dict:
    """
    Delete the specified venv folders and return deletion results.
    
    Args:
        folders_to_delete: List of (folder_path, size) tuples to delete
        root_path: Root directory for relative path display
        
    Returns:
        Dict: Deletion results with success/failure counts and freed space
    """
    deleted_count = 0
    failed_count = 0
    freed_space = 0
    
    print(f"\nDeleting {len(folders_to_delete)} venv folders...")
    print("-" * 60)
    
    for folder, size in folders_to_delete:
        relative_path = folder.relative_to(root_path)
        try:
            # Use shutil.rmtree for recursive deletion
            shutil.rmtree(folder)
            deleted_count += 1
            freed_space += size
            print(f"✓ Deleted: {relative_path} ({humanize.naturalsize(size)})")
        except (OSError, PermissionError) as e:
            failed_count += 1
            print(f"✗ Failed to delete: {relative_path} - {e}")
    
    return {
        'deleted_count': deleted_count,
        'failed_count': failed_count,
        'freed_space': freed_space
    }


def display_results(analysis: Dict, root_path: Path, verbose: bool = False, auto_delete: bool = False):
    """
    Display the analysis results in a formatted way.
    
    Args:
        analysis: Analysis results dictionary
        root_path: Root directory that was analyzed
        verbose: Whether to show detailed information
        auto_delete: Whether to automatically offer deletion
    """
    print(f"\n{'='*60}")
    print(f"Virtual Environment Analysis Results")
    print(f"{'='*60}")
    print(f"Root Directory: {root_path.absolute()}")
    print(f"Total venv folders found: {analysis['count']}")
    print(f"Total size: {humanize.naturalsize(analysis['total_size'])}")
    print(f"{'='*60}")
    
    if analysis['count'] == 0:
        print("No virtual environment folders found.")
        return
    
    if verbose:
        print("\nDetailed breakdown:")
        print("-" * 60)
        for i, (folder, size) in enumerate(analysis['folder_sizes'], 1):
            relative_path = folder.relative_to(root_path)
            print(f"{i:2d}. {relative_path}")
            print(f"    Size: {humanize.naturalsize(size)}")
            print()
    else:
        print("\nTop 5 largest venv folders:")
        print("-" * 60)
        for i, (folder, size) in enumerate(analysis['folder_sizes'][:5], 1):
            relative_path = folder.relative_to(root_path)
            print(f"{i}. {relative_path} - {humanize.naturalsize(size)}")
    
    # Offer deletion option
    if auto_delete and analysis['count'] > 0:
        top_5_folders = analysis['folder_sizes'][:5]
        total_size_top_5 = sum(size for _, size in top_5_folders)
        
        print(f"\n{'='*60}")
        print(f"Cleanup Option")
        print(f"{'='*60}")
        print(f"Would you like to delete the top {len(top_5_folders)} largest venv folders?")
        print(f"This would free up {humanize.naturalsize(total_size_top_5)} of disk space.")
        print()
        
        for i, (folder, size) in enumerate(top_5_folders, 1):
            relative_path = folder.relative_to(root_path)
            print(f"{i}. {relative_path} ({humanize.naturalsize(size)})")
        
        print()
        response = input("Delete these folders? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            # Double confirmation for safety
            print("\n⚠️  WARNING: This action cannot be undone!")
            confirm = input("Type 'DELETE' to confirm deletion: ").strip()
            
            if confirm == 'DELETE':
                deletion_results = delete_venv_folders(top_5_folders, root_path)
                
                print(f"\n{'='*60}")
                print(f"Deletion Summary")
                print(f"{'='*60}")
                print(f"Successfully deleted: {deletion_results['deleted_count']} folders")
                print(f"Failed to delete: {deletion_results['failed_count']} folders")
                print(f"Space freed: {humanize.naturalsize(deletion_results['freed_space'])}")
                print(f"{'='*60}")
            else:
                print("Deletion cancelled.")
        else:
            print("No folders were deleted.")


def main():
    """Main function to run the venv analyzer."""
    parser = argparse.ArgumentParser(
        description="Analyze directories for virtual environment folders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python venv_analyzer.py                    # Analyze current directory
  python venv_analyzer.py /path/to/dir       # Analyze specific directory
  python venv_analyzer.py -v                 # Verbose output
  python venv_analyzer.py --max-depth 3      # Limit search depth
  python venv_analyzer.py --auto-delete      # Offer to delete top 5 largest
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to analyze (default: current directory)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed information about each venv folder'
    )
    
    parser.add_argument(
        '--max-depth',
        type=int,
        help='Maximum depth to search (default: unlimited)'
    )
    
    parser.add_argument(
        '--auto-delete',
        action='store_true',
        help='Offer to delete the top 5 largest venv folders after analysis'
    )
    
    args = parser.parse_args()
    
    # Convert to Path object
    root_path = Path(args.directory)
    
    # Validate the directory exists
    if not root_path.exists():
        print(f"Error: Directory '{root_path}' does not exist.")
        sys.exit(1)
    
    if not root_path.is_dir():
        print(f"Error: '{root_path}' is not a directory.")
        sys.exit(1)
    
    print(f"Searching for virtual environment folders in: {root_path.absolute()}")
    print("This may take a moment for large directories...")
    
    try:
        # Find venv folders
        venv_folders = find_venv_folders(root_path, args.max_depth)
        
        # Analyze the results
        analysis = analyze_venv_folders(venv_folders)
        
        # Display results
        display_results(analysis, root_path, args.verbose, args.auto_delete)
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 