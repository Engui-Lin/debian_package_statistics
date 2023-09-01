# Debian Package Analyzer

**Time Spent:** 6 hours

## Description

This script allows you to analyze package statistics for a specified architecture by fetching package information from a Debian mirror repository. It provides insights into packages with the highest number of files. The script offers the following functionalities:

- Fetches package contents from the specified mirror URL. (http://ftp.uk.debian.org/debian/dists/stable/main/)
- Parses the contents to count the number of files per package.
- Prints the top 10 packages with the most files for the given architecture.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Dependencies](#dependencies)

## Installation

1. Ensure that Python 3.11.4 is installed on your system.
2. Create a Python virtual environment using Python version 3.11.4:

   ```
   $ python -m venv .venv
   ```

3. Activate the virtual environment:

   - macOS:

     ```
     $ source .venv/bin/activate
     ```

4. Install the required dependencies:

   ```
   $ pip install -r requirements.txt
   ```

5. Run the command to analyze package statistics. For example:

   ```
   $ python package_statistics.py arm64
   ```

## Usage

The script provides a command-line interface for interacting with Debian package data. It supports the following options:

```
$ python debian_package_analyzer.py [-h] [architecture] [-list]
```

### Options

- `-h`, `--help`: Display the help message.
- `architecture`: Specify the desired architecture (e.g., amd64, arm64, i386) for which you want to analyze package statistics. If not provided, an error will be displayed.
- `-list`: List all available architectures in the mirror.

## Examples

### List Available Architectures

To see the list of available architectures in the Debian mirror:

```
$ python debian_package_analyzer.py -list
```

### Analyze Package Statistics

To analyze package statistics for a specific architecture:

```
$ python debian_package_analyzer.py amd64
```

Replace `amd64` with the desired architecture.

The script will display the top 10 packages for the specified architecture based on the number of files they contain.

## Dependencies

This script relies on the following Python libraries:

- `argparse`: Used for command-line argument parsing.
- `collections.defaultdict`: Efficiently handles counting package statistics.
- `re`: Enables regular expression operations for parsing content URLs.
- `requests`: Provides an HTTP requests library to fetch package contents.
- `gzip`: Allows for Gzip compression and decompression for package content files.
