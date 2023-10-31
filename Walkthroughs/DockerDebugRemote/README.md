# Using Docker Debug with Remote Contexts
### This walkthrough explains how to use the Docker Debug extension with a remote Docker context.

## Overview
This walkthrough explains how to use the [
Docker Debug Extension](https://hub.docker.com/extensions/docker/labs-debug-tools-extension) with a remote container.
This enables you to connect to a container running in a given remote context from a system with Docker Desktop 
installed. This example leverages the power of 
[Docker Contexts](https://docs.docker.com/engine/context/working-with-contexts/)

## Steps

### 1. Connect to the remote system and verify the Docker version; this needs to be 19.03 or greater.

```shell
# uname -a
Linux dock01 5.15.111-1-pve #1 SMP PVE 5.15.111-1 (2023-08-18T08:57Z) x86_64 x86_64 x86_64 GNU/Linux
# docker version
Client: Docker Engine - Community
 Version:           24.0.7
 API version:       1.43
 Go version:        go1.20.10
 Git commit:        afdd53b
 Built:             Thu Oct 26 09:07:51 2023
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          24.0.7
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.20.10
  Git commit:       311b9ff
  Built:            Thu Oct 26 09:07:51 2023
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.24
  GitCommit:        61f9fd88f79f081d64d6fa3bb1a0dc71ec870523
 runc:
  Version:          1.1.9
  GitCommit:        v1.1.9-0-gccaecfc
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

### 2. Add a new docker context for that system.

```shell
$ uname -a
Darwin TDRYQ6WR2R 22.6.0 Darwin Kernel Version 22.6.0: Fri Sep 15 13:41:28 PDT 2023; root:xnu-8796.141.3.700.8~1/RELEASE_ARM64_T6020 arm64

$ docker context create dock01 --docker "host=ssh://root@192.168.212.57"

dock01
Successfully created context "dock01"
```

### 3. Select the context; note that you can switch contexts back to your default if you no longer want to be administering the remote machine.

```shell
$ docker context use dock01
dock01
Current context is now "dock01"
```

### 4. Validate the context.

```shell
$ docker context ls
NAME                TYPE                DESCRIPTION                               DOCKER ENDPOINT                                  KUBERNETES ENDPOINT   ORCHESTRATOR
default             moby                Current DOCKER_HOST based configuration   unix:///var/run/docker.sock        
desktop-linux       moby                Docker Desktop                            unix:///Users/jschmidt/.docker/run/docker.sock
dock01 *            moby                                                          ssh://root@192.168.212.57          
```

### 5. Check the context; you can see that we are using the remote docker installation (note the difference in arch between the client and server).

```shell
$ docker version
Client:
 Cloud integration: v1.0.35+desktop.5
 Version:           24.0.6
 API version:       1.43
 Go version:        go1.20.7
 Git commit:        ed223bc
 Built:             Mon Sep  4 12:28:49 2023
 OS/Arch:           darwin/arm64
 Context:           dock01

Server: Docker Engine - Community
 Engine:
  Version:          24.0.7
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.20.10
  Git commit:       311b9ff
  Built:            Thu Oct 26 09:07:51 2023
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.24
  GitCommit:        61f9fd88f79f081d64d6fa3bb1a0dc71ec870523
 runc:
  Version:          1.1.9
  GitCommit:        v1.1.9-0-gccaecfc
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
  ```
  
 ### 6. Run an image on the remote system.
 
 ```shell
 $ docker run -d nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
a378f10b3218: Pull complete
5b5e4b85559a: Pull complete
508092f60780: Pull complete
59c24706ed13: Pull complete
1a8747e4a8f8: Pull complete
ad85f053b4ed: Pull complete
3000e3c97745: Pull complete
Digest: sha256:add4792d930c25dd2abf2ef9ea79de578097a1c175a16ab25814332fe33622de
Status: Downloaded newer image for nginx:latest
f83360ec77a6debae88eb132b7d72d34dac73cbb9f5eb445b7becf28302a4db5
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS          PORTS     NAMES
f83360ec77a6   nginx     "/docker-entrypoint.…"   About a minute ago   Up 57 seconds   80/tcp    goofy_curie
```


### 7. Attach the debugger; note that the first time it runs it will need to pull the image down.

```shell
$ dld attach goofy_curie
          #         .      ________                    __
      # # #        ==      \______ \    ____    ____  |  | __  ____  _______
    # # # # #    ===        |    |  \  /  _ \ _/ ___\ |  |/ /_/ __ \ \_  __ \
 /""""""""""""\__/ ===      |    `   \(  <_> )\  \___ |    < \  ___/  |  | \/
{                 /   ==   /_______  / \____/  \___  >|__|_ \ \___  > |__|
 \             __/                 \/              \/      \/     \/
  \___________/

Builtin commands:
- install [tool1] [tool2] ...    Add Nix packages from: https://search.nixos.org/packages
- uninstall [tool1] [tool2] ...  Uninstall NixOS package(s).
- entrypoint                     Print/lint/run the entrypoint.
- builtins                       Show builtin commands.

Checks:
✓ entrypoint linter: no errors (run 'entrypoint' for details)

This is an attach shell, i.e.:
- Any changes to the container filesystem are visible to the container directly.
- The /nix directory is invisible to the actual container.

Feature requests and feedback: https://github.com/docker/roadmap/issues/524
Bug reports: https://github.com/docker/roadmap/issues/523

root@f83360ec77a6 / [goofy_curie]
docker > uname -a
Linux f83360ec77a6 5.19.0-46-generic #47-Ubuntu SMP PREEMPT_DYNAMIC Fri Jun 16 13:30:11 UTC 2023 x86_64 GNU/Linux
root@f83360ec77a6 / [goofy_curie]
docker >
$ dld attach goofy_curie
Pulling image, this might take a moment...
0.0.43: Pulling from docker/labs-debug-tools-service
```


### 8. Other commands can be used; for example to start a remote debugging session use the following.

```
$ dld
A docker debugging toolbox.

Usage:
  dld COMMAND [ARG...]
  dld [command]

Available Commands:
  attach      Attach a shell to a running container
  help        Help about any command
  rdb         Attach a remote debugger to a running container
  shell       Get a shell into any container or image.
  version     Print version of dld

Use "dld [command] --help" for more information about a command.
```

### Citations and Helpful Information
- Note that the Docker Debug extension is under heavy development.
- Documentation is available both on the website and under the extension landing page once you have installed the extension.
- The docker debug container continues to run after you have disconnected; that is, it extends past the lifetime of your session unless you go through and clean things up. This allows packages installed in the debugging session to be persisted.
- The user on the remote side needs to be part of the `docker` group.
- The remote user needs to have passwordless SSH enabled.
- Issues have been encountered running Docker Debug against servers that utilize LXC.
- [Docker Extensions](https://www.docker.com/products/extensions/)
- [Docker Contexts](https://docs.docker.com/engine/context/working-with-contexts/)
- [Docker Contexts and Compose](https://www.docker.com/blog/how-to-deploy-on-remote-docker-hosts-with-docker-compose/)
- [Docker Debug Extension](https://hub.docker.com/extensions/docker/labs-debug-tools-extension)
