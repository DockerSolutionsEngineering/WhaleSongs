# Docker Desktop System Logs
An overview of where Docker Desktop logs are stored and how long they are retained

## Docker Desktop Logging:

### Docker Desktop logs are comprised of 3 components:

1. Docker Engine
2. Electron
3. Docker Desktop

### Docker Engine Logging

* Docker Engine logs are [configurable](https://docs.docker.com/config/daemon/logs/)

* The defaults for Docker Engine logging are as follows:
    * Max file size of 20MiB
    * Maxmium retained files of 5
    * Compressed rotated log files is enabled
---
#### Changing Docker Engine Defaults 

* Example change to daemon.json to deviate from default retention. For more options see [logging driver options](https://docs.docker.com/config/containers/logging/local/#options) and [daemon.json configuration](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)
    ```javascript
    {
        "log-driver": "local",
        "log-opts": {
            "max-size": "10m"
        }
    }
    ```

* Windows daemon.json path
    ```powershell
    %ProgramData%\docker\config\daemon.json
    ```

* macOS daemon.json path
    ```
    /System/Volumes/Data/Users/kiener/.docker/daemon.json
    ```

## Location of Log Files

* Windows
    ```
    %LOCALAPPDATA%\Docker\log\vm\
    %LOCALAPPDATA%\Docker\log\host\
    ```

* macOS
    ```
    ~/Library/Containers/com.docker.docker/Data/log/vm/
    ~/Library/Containers/com.docker.docker/Data/log/host/

    ```

## Docker Desktop Logging

* Docker Desktop logging is currently non-configurable

* The defaults for Docker Desktop logging are as follows 
    * Maximum single log file size of 1MiB per component
    * Maximum log file space per component of 10MiB
    * There are fifteen components in Docker Desktop

## Electron

* Electron logging is currently non-configurable

* The defaults for Electron logging are as follows
    * Maximum of 14 days of log files
    * Maximum single log file size of 20MiB

## Space Utilization in Aggregate

* Theoritical Maximum of 750MiB
* Real-world power users generally see 150MiB as a high water mark

### Citations and Helpful Files
* [Local Log File Driver](https://docs.docker.com/config/containers/logging/local/)
* [Daemon Logs](https://docs.docker.com/config/daemon/logs/)