# Recently Modified

Simple python script which checks for recently modified directories in Projects and adds them to the bookmarks (so they are visible in the Dolphin file manager in the left toolbaar).

## Usage

```
usage: bookmarks.py [-h] [--entries ENTRIES] [--bookmarks_path BOOKMARKS_PATH]
                    [--directory DIRECTORY] [--icon ICON]

optional arguments:
  -h, --help            show this help message and exit
  --entries ENTRIES     The number of recent entries to include. The default
                        is 5.
  --bookmarks_path BOOKMARKS_PATH
                        The path to bookmarks. Default is
                        "/home/dio/.local/share/user-places.xbel"
  --directory DIRECTORY
                        Directory to get the recent entries from. The default
                        is "~/Projects/*/"
  --icon ICON           The folder icon to use for the entries. The default is
                        blue-folder.
```