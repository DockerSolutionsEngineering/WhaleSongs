import sys
import re

def parse_container_start_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << POST /v1\.\d+/exec/(?P<container_id>[a-f0-9]+)/start \((?P<duration>.*?)\)'
    match = re.search(pattern, log_line)
    if match:
        return match.group('datetime'), match.group('container_id'), "Container Start", match.group('duration')
    return None, None, None, None

def parse_container_stop_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << POST /containers/(?P<container_id>[a-f0-9]+)/stop \((?P<duration>.*?)\)'
    match = re.search(pattern, log_line)
    if match:
        return match.group('datetime'), match.group('container_id'), "Container Stop", match.group('duration')
    return None, None, None, None

def parse_image_create_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << POST /images/create.*?fromImage=(?P<image_name>[^&]+)&tag=(?P<version>.*?) '
    match = re.search(pattern, log_line)
    if match:
        return match.group('datetime'), match.group('image_name'), "Image Create", match.group('version')
    return None, None, None, None

def parse_image_delete_log(log_line):
    pattern = r'time="(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)".*?proxy << DELETE /images/(?P<image_name_with_version>[^ ]+) '
    match = re.search(pattern, log_line)
    if match:
        image_name_with_version = match.group('image_name_with_version')
        if ':' in image_name_with_version:
            image_name, version = image_name_with_version.rsplit(':', 1)
        else:
            image_name = image_name_with_version
            version = None
        return match.group('datetime'), image_name, "Image Delete", version
    return None, None, None, None

def main():
    for line in sys.stdin:
        datetime, name, operation, detail = (parse_container_start_log(line) or 
                                             parse_container_stop_log(line) or 
                                             parse_image_create_log(line) or 
                                             parse_image_delete_log(line))
        if datetime:
            sys.stdout.write(f"Date/Time: {datetime}\nName: {name}\nOperation: {operation}\nDetail: {detail}\n\n")

if __name__ == "__main__":
    main()