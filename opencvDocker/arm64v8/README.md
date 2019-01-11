# Docker Container for Running OpenCv

## Description

This is a dockerfile that builds a container that will run on an arm64 or and aarch64 procesor. It can be built on any machine.
### Build Instructions

In terminal, run:

```bash
$ cd opencvDocker
$ docker run --rm --privileged multiarch/qemu-user-static:register
$ docker build -t opencv-arm64:4.0.0 .
```

If you need to build for another architecture, visit this website [https://lobradov.github.io/Building-docker-multiarch-images/](https://lobradov.github.io/Building-docker-multiarch-images/)

### Python3 with OpenCV 4.0.0 installed. This one is built for arm64v8

[http://www.hotblackrobotics.com/en/blog/2018/01/22/docker-images-arm/](http://www.hotblackrobotics.com/en/blog/2018/01/22/docker-images-arm/)


