sample_data = {
    "start_or_restart": [
        'time="2023-08-31T13:30:17Z" level="info" msg="GoBackend: [2023-08-31T13:30:17.253279000Z][com.docker.backend.apiproxy][I] proxy << POST /containers/7c34e2e05feb57c9c3f0f7692913dee27c15facce2d3e8a83cac8a479810916a/start (111.718708ms)"',
        'time="2023-08-31T13:30:18Z" level="info" msg="GoBackend: [2023-08-31T13:30:18.253279000Z][com.docker.backend.apiproxy][I] proxy << POST /containers/8c35e3f05feb57c9c3f0f7692913dee27c15facce2d3e8a83cac8a479810917b/restart (112.718708ms)"'
    ],
    "stop": [
        'time="2023-08-31T13:30:18Z" level="info" msg="GoBackend: [2023-08-31T13:30:18.253279000Z][com.docker.backend.apiproxy][I] proxy << POST /containers/8c35e3f05feb57c9c3f0f7692913dee27c15facce2d3e8a83cac8a479810917b/stop (112.718708ms)"'
    ],
    "image_create": [
        'time="2023-08-31T13:30:20Z" level="info" msg="GoBackend: [2023-08-31T13:30:20.253279000Z][com.docker.backend.apiproxy][I] proxy << POST /images/create?fromImage=postgres&tag=latest (114.718708ms)"'
    ],
    "container_delete": [
        'time="2023-08-31T13:30:21Z" level="info" msg="GoBackend: [2023-08-31T13:30:21.253279000Z][com.docker.backend.apiproxy][I] proxy << DELETE /containers/ac37e5h05feb57c9c3f0f7692913dee27c15facce2d3e8a83cac8a479810919d (115.718708ms)"'
    ],
    "image_delete": [
        'time="2023-08-31T13:30:22Z" level="info" msg="GoBackend: [2023-08-31T13:30:22.253279000Z][com.docker.backend.apiproxy][I] proxy << DELETE /images/docker.io/library/postgres:latest (116.718708ms)"'
    ]
}
