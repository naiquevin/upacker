General Information
-------------------
Upacker is simple tool/utility that can be used to "pack" a set of files 
across various directories of a project for uploading.
The original directory structure of the project in preserved thus making 
it very convenient to upload the files at once.

It can pack files under a Git working tree from the commit hash(es).
There is also a file mode in which it reads a manifest file that contains a 
list of the files to be packed.
The file mode can be very useful if there are deleted/files between two commits
and the Git archive command fails.

Note:
----
But this is my first python code and it was written mainly for learning purpose.
I use it myself but have a feeling that its a very silly app and what it 
does can already be handled by Git!

Usage
-----
# file mode
python pack.py --file <path_to_file>

# git mode
python pack.py --git <git_wt_source> <SHA1> <SHA1 optional>
