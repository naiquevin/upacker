Welcome to upacker or more precisely Upload packer. 
This tool is meant to be used for copying or packing
only a few files from a project to a directory while
preserving the original directory structure.
Thus making it convenient to upload all of them to
the server at once

Usage: python pack.py <path_to_file>

path_to_file = path to the file in which which files
to copy is specified

sample file contents:
<<
basepath=/home/vineet/public_html/
basedir=blog

index.php
wp-cron.php
wp-content/index.php
wp-content/themes/index.php
wp-includes/**
>>
