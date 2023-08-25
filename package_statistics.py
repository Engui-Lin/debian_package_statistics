import argparse
import gzip
import re
from collections import defaultdict

import requests


def download_content(mirror_url: str, architecture: str):
    """Return the response content in bytes."""
    content_url = f"{mirror_url}/Contents-{architecture}.gz"

    try:
        response = requests.get(content_url)
        response.raise_for_status()  # Raise HTTPError for non-2xx responses
        print("Request was successful")

        return response.content

    except requests.exceptions.HTTPError as e:
        print(f"Error downloading content for architecture: {architecture}")
        raise


def parse_contents(contents):
    """Count the number of files per package."""
    package_stats = defaultdict(int)

    # decompress the .gz file and decode the content
    debian_contents = gzip.decompress(contents).decode("utf-8").split("\n")

    for line in debian_contents:
        # remove leading and trailing whitespace, then split into file_name and package_name
        parts = line.strip().split()
        if len(parts) != 2:  # Do not consider file names with whitespaces
            continue
        _, package_name = parts[0], parts[1]
        package_stats[package_name] += 1

    return package_stats


def print_top_10_packages(architecture: str, package_stats: dict):
    """Print the top 10 packages with the most files."""
    top_10_packages = sorted(
        package_stats.items(), key=lambda item: item[1], reverse=True
    )[:10]

    dash = "-" * 80
    print(dash)
    print(f"Top packages for {architecture} architecture")
    print(dash)
    for i, (package_name, num_of_files) in enumerate(top_10_packages, start=1):
        print(f"{i:<2}.    {package_name:<60} {num_of_files:<6} files")
    print(dash)


def list_available_architectures(mirror_url):
    """Print all the available architectures."""
    response = requests.get(mirror_url)
    response.raise_for_status()
    data = response.text.splitlines()
    filtered_data = [line for line in data if "Contents-" in line and ".gz" in line]
    pattern = r"Contents-(.*?)\.gz"
    architectures = []
    for line in filtered_data:
        match = re.search(pattern, line)
        if match:
            architectures.append(match.group(1))

    print(f"Available architectures: {architectures}")


def main():
    parser = argparse.ArgumentParser(
        description="Get statistics of debian packages with most files."
    )
    parser.add_argument(
        "architecture",
        nargs="?",
        type=str,
        help="enter the desired architecture (e.g., amd64, arm64, i386) -list to see available architectures",
    )
    parser.add_argument(
        "-list", action="store_true", help="List available architectures"
    )

    args = parser.parse_args()

    mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"

    if args.list:
        list_available_architectures(mirror_url)
    elif args.architecture:
        try:
            contents = download_content(mirror_url, architecture := args.architecture)
            package_stats = parse_contents(contents)
            print_top_10_packages(architecture, package_stats)
        except Exception as e:
            print(e)
            exit()
    else:
        parser.error("At least one argument (-list or architecture) is required.")


if __name__ == "__main__":
    main()
