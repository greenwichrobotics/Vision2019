# Docker Container for Running OpenCv

## Description

This is a dockerfile that builds a container that will run on any platform the build command is run on. If you need to run this on an arm processor, it needs to be built on an arm processor. If you are running this on an x86 proccessor, it needs to be built on an x86 processor.

### Build Instructions

In terminal, run:

```bash
$ cd opencvDocker
$ docker build -t opencv:4.0.0 .
```
