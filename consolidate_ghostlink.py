#!/usr/bin/env python3
"""
GhostLink Python Consolidator
==============================

This script consolidates all Python files in the GhostLink repository
into a single file that can be easily shared with ChatGPT.

Usage:
    python3 consolidate_ghostlink.py

Output:
    ghostlink_consolidated.py - Single file with all Python code
"""

import os
import datetime
import sys


def consolidate_python_files():
    """Consolidate all Python files into one single file"""
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', '.venv', 'node_modules']]
        for file in files:
            if file.endswith('.py') and file != 'consolidate_ghostlink.py':  # Skip this script
                filepath = os.path.join(root, file)
                python_files.append(filepath)
    
    python_files.sort()
    
    if not python_files:
        print("❌ No Python files found!")
        return None
    
    # Create consolidated file
    output_path = 'ghostlink_consolidated.py'
    
    # Collect all __future__ imports
    future_imports = set()
    
    # First pass: collect all future imports
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.strip().startswith('from __future__ import'):
                        future_imports.add(line.strip())
                    elif line.strip() and not line.strip().startswith('#'):
                        # Stop at first non-comment, non-future-import line
                        break
        except Exception as e:
            print(f'⚠️  Warning: Could not read {filepath}: {str(e)}')
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        # Write all future imports first
        if future_imports:
            outfile.write('# Consolidated future imports from all modules\n')
            for imp in sorted(future_imports):
                outfile.write(imp + '\n')
            outfile.write('\n')
        
        # Write header
        outfile.write('"""\n')
        outfile.write('GhostLink - Consolidated Python Repository\n')
        outfile.write('='*70 + '\n\n')
        outfile.write(f'Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        outfile.write(f'Total Files: {len(python_files)}\n\n')
        outfile.write('This file consolidates all Python code from the GhostLink repository\n')
        outfile.write('into a single file for easy access and sharing with ChatGPT.\n\n')
        outfile.write('USAGE:\n')
        outfile.write('  - Copy entire file and share with ChatGPT\n')
        outfile.write('  - Each section is clearly marked with file boundaries\n')
        outfile.write('  - Use Ctrl+F to find specific modules or functions\n\n')
        outfile.write('Table of Contents:\n')
        outfile.write('-'*70 + '\n')
        
        # Write table of contents
        for i, filepath in enumerate(python_files, 1):
            outfile.write(f'{i:3d}. {filepath}\n')
        
        outfile.write('\n' + '='*70 + '\n')
        outfile.write('"""\n\n')
        
        # Process each file
        errors = []
        for i, filepath in enumerate(python_files, 1):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                    content = infile.read()
                
                # Remove __future__ imports from individual files since we put them at top
                lines = content.split('\n')
                filtered_lines = []
                skip_next_blank = False
                
                for line in lines:
                    if line.strip().startswith('from __future__ import'):
                        skip_next_blank = True
                        continue
                    if skip_next_blank and not line.strip():
                        skip_next_blank = False
                        continue
                    filtered_lines.append(line)
                
                content = '\n'.join(filtered_lines)
                
                # Write file separator and header
                outfile.write('\n\n')
                outfile.write('#' + '='*69 + '\n')
                outfile.write(f'# FILE {i}/{len(python_files)}: {filepath}\n')
                outfile.write('#' + '='*69 + '\n\n')
                
                # Write file content
                outfile.write(content)
                
                # Ensure content ends with newline
                if content and not content.endswith('\n'):
                    outfile.write('\n')
                    
            except Exception as e:
                error_msg = f'ERROR reading {filepath}: {str(e)}'
                outfile.write(f'\n# {error_msg}\n')
                errors.append(error_msg)
        
        # Write footer
        outfile.write('\n\n')
        outfile.write('#' + '='*69 + '\n')
        outfile.write('# END OF CONSOLIDATED GHOSTLINK PYTHON REPOSITORY\n')
        outfile.write('#' + '='*69 + '\n')
    
    # Get file stats
    file_size = os.path.getsize(output_path)
    with open(output_path, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    
    print()
    print('✅ Successfully created: ghostlink_consolidated.py')
    print(f'   Files consolidated: {len(python_files)}')
    print(f'   Total lines: {line_count:,}')
    print(f'   File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')
    
    if errors:
        print(f'\n⚠️  {len(errors)} errors encountered:')
        for err in errors:
            print(f'   - {err}')
    
    # Verify syntax
    print('\n🔍 Verifying Python syntax...')
    import py_compile
    try:
        py_compile.compile(output_path, doraise=True)
        print('✅ Python syntax is valid!')
    except py_compile.PyCompileError as e:
        print(f'❌ Syntax error detected: {e}')
        return None
    
    print()
    print('📋 Next steps:')
    print('   1. Open ghostlink_consolidated.py')
    print('   2. Copy the entire file (Ctrl+A, Ctrl+C)')
    print('   3. Share with ChatGPT for analysis, review, or questions')
    print()
    
    return output_path


if __name__ == '__main__':
    result = consolidate_python_files()
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
