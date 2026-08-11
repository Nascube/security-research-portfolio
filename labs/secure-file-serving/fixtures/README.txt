Secure File Serving Lab - Sample Files

This directory contains sample files used for testing the secure file
serving implementation. These files are:

1. hello.txt - A simple text file used in tests
2. README.txt - This file

These are the ONLY files that should be accessible through the file
serving endpoints. Any attempt to access files outside this directory
(like ../../../etc/passwd) should be blocked by the secure implementation.
