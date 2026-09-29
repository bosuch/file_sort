# Sort Files by First Character

A small Python utility that organizes a Windows directory by moving each file into a subfolder named after the first letter or number of its file name.

```
Downloads\
├── apple.txt          →  A\apple.txt
├── Avocado.jpg        →  A\Avocado.jpg
├── 2024_notes.docx    →  2\2024_notes.docx
├── report.pdf         →  R\report.pdf
└── _scratch.log       →  _Other\_scratch.log
```

## Features

- Sorts files into subfolders by first letter or number
- Case-insensitive grouping (`apple.txt` and `Avocado.jpg` both go in `A`)
- Files starting with symbols (`_`, `-`, `.`, etc.) go into an `_Other` folder
- Never overwrites: name collisions become `name (1).ext`, `name (2).ext`, and so on
- `--dry-run` mode to preview changes before anything is moved
- Skips itself if the script is in the target directory
- Uses only the Python standard library, so there is nothing to install

## Requirements

- Python 3.6 or newer
- Windows (also works on macOS and Linux)

## Usage

```
python sort_files_by_first_char.py "C:\path\to\directory"
```

Preview first without moving anything:

```
python sort_files_by_first_char.py "C:\path\to\directory" --dry-run
```

### Options

| Argument     | Description                                              |
|--------------|----------------------------------------------------------|
| `directory`  | The directory to organize (required)                     |
| `--dry-run`  | Print what would be moved without changing any files     |

### Example output

```
$ python sort_files_by_first_char.py "C:\Users\Bill\Downloads" --dry-run
[dry run] 2024_notes.docx -> 2\2024_notes.docx
[dry run] apple.txt -> A\apple.txt
[dry run] report.pdf -> R\report.pdf

Would move 3 file(s). Skipped 0. Errors: 0.
```

## How it works

1. Lists the items directly inside the target directory
2. Ignores subfolders, so existing folders are never touched or re-sorted
3. Looks at the first character of each file name:
   - Letter or number: uses its uppercase form as the folder name
   - Anything else: uses `_Other`
4. Creates the subfolder if needed and moves the file into it, adding a numeric suffix if the name is already taken

## Notes

- Only files directly inside the target directory are processed. Subdirectories are **not** searched recursively.
- Moves are not tracked, so there is no built-in undo. Run with `--dry-run` first on anything important.
- Files that are open in another program may fail to move. These are reported as errors and the script continues with the rest.

## License

Released under the [MIT License](LICENSE). Add a `LICENSE` file to your repository if you want to use it.
