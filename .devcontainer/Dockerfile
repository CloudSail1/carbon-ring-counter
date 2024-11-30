FROM python:3.12

## Pip dependencies
# Upgrade pip
RUN pip install --upgrade pip
RUN pip install ovito
RUN pip install scipy
RUN pip install pytest
RUN pip install matplotlib

## Fix "ImportError: libGL.so.1: cannot open shared object file: No such file or directory"
## Fix "ImportError: libEGL.so.1: cannot open shared object file: No such file or directory"
## Fix "ImportError: libOpenGL.so.0: cannot open shared object file: No such file or directory"
RUN apt-get update
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install libgl1 -y
RUN apt install libegl1 -y
RUN apt install libopengl0 -y