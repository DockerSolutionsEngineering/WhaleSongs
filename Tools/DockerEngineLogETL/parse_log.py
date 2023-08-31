#!/usr/bin/env python3
import sys
import re
import argparse

"""
Docker Log Parser

This program is designed to parse Docker logs, specifically focusing on operations 
related to containers and images such as start, stop, create, and delete. The main 
goal is to extract and present relevant details from the logs in a structured format.

Key Features:
- Filters out irrelevant log lines, focusing only on operations that pertain to 
  containers and images.
- Extracts key details such as the datetime of the operation, the ID or name of 
  the container or image, the type of operation, and its duration.
- Provides two output formats: a default syslog-style format and a human-readable 
  format that can be activated with the '-r' or '--readable' flag.

Usage:
By default, the program reads log lines from standard input and writes the parsed 
details to standard output. For a more human-friendly output, use the '-r' flag.

Example:
cat docker.log | python3 parse_log.py -r

Note: This parser assumes that the Docker logs follow a specific structure and 
pattern. If the log format changes in future Docker versions, the parser may need 
to be updated accordingly.
"""

def is_relevant_log_line(line):
    if "proxy <<" not in line.lower():
        return False
    relevant_keywords = ["delete", "start", "stop", "image", "create"]
    return any(keyword in line.lower() for keyword in relevant_keywords)


def parse_container_start_or_restart_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << POST /containers/(?P<container_id>[a-f0-9]+)/(?P<operation>start|restart) \((?P<duration>.*?)\)'
    match = re.search(pattern, log_line)
    if match:
        operation = "Container " + match.group('operation').capitalize()
        return match.group('datetime'), match.group('container_id'), operation, match.group('duration'), ""
    return None, None, None, None, ""


def parse_container_stop_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << POST /containers/(?P<container_id>[a-f0-9]+)/stop.*?\((?P<duration>.*?)\)'

    match = re.search(pattern, log_line)
    if match:
        return match.group('datetime'), match.group('container_id'), "Container Stop", match.group('duration'),""
    return None, None, None, None, ""


def parse_image_create_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << POST /images/create.*?fromImage=(?P<image_name>\w+)&tag=(?P<version>\w+).*?\((?P<duration>.*?)\)'
    match = re.search(pattern, log_line)
    if match:
        return match.group('datetime'), match.group('image_name'), "Image Create", match.group('duration'), match.group('version')
    return None, None, None, None, ""


def parse_container_delete_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << DELETE /containers/(?P<container_id>[a-f0-9]+).*?\((?P<duration>.*?)\)'
    match = re.search(pattern, log_line)
    if match:
        return match.group('datetime'), match.group('container_id'), "Container Delete", match.group('duration'), ""
    return None, None, None, None, ""


def parse_image_delete_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << DELETE /images/(?P<image_name_with_version>[^ ]+).*?\((?P<duration>.*?)\)'
    match = re.search(pattern, log_line)
    if match:
        image_name_with_version = match.group('image_name_with_version')
        if ':' in image_name_with_version:
            image_name, version = image_name_with_version.rsplit(':', 1)
        else:
            image_name = image_name_with_version
            version = ""
        return match.group('datetime'), image_name, "Image Delete", match.group('duration'), version
    return None, None, None, None, ""


def main():
    parser = argparse.ArgumentParser(description="Parse docker logs.")
    parser.add_argument("-r", "--readable", action="store_true", help="Display output in a human-readable format.")
    args = parser.parse_args()

    parsed_lines = set()
    for line in sys.stdin:
        if line in parsed_lines:
            continue
        if not is_relevant_log_line(line):
            continue

        datetime, name, operation, duration, details = parse_container_start_or_restart_log(line)
        if datetime is None:
            datetime, name, operation, duration, details = parse_container_stop_log(line)
        if datetime is None:
            datetime, name, operation, duration, details = parse_image_create_log(line)
        if datetime is None:
            datetime, name, operation, duration, details = parse_container_delete_log(line)
        if datetime is None:
            datetime, name, operation, duration, details = parse_image_delete_log(line)

        if datetime:
            if args.readable:
                sys.stdout.write(
                    f"Date/Time: {datetime}\nName: {name}\nOperation: {operation}\nDuration: {duration}\nDetails: {details}\n\n")
            else:
                sys.stdout.write(f"{datetime} - {name} - {operation} - {duration} - {details}\n")
            parsed_lines.add(line)


if __name__ == "__main__":
    main()
