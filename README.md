# Narakeet Presentation to Video example in Python

This repository provides a quick example demonstrating how to access the Narakeet presentation to video API from Python.

The example sends a request to generate a video from a local powerpoint file, then downloads the resulting video into a temporary local file. 

## Prerequisites

This example works with Python 3.7 and later. You can run it inside Docker (then it does not require a local Python installation), or on a system with a Python 3.7 or later.

## Running the example

### run inside docker

1. Copy the powerpoint file you want to convert into the directory with the example (so Docker can see it)
2. Execute `make run NARAKEET_API_KEY=(YOUR API KEY) PPTX_FILE=(PPTX_FILE_TO_CONVERT)`

### run outside docker, on a system with `python` command line, 

1. set the environment variables NARAKEET_API_KEY and PPTX_FILE
2. download dependencies using `pip install -r requirements.txt`
2. execute `python main.py`

### example presentation

You can use the `demo.pptx` file in this directory as a quick example. Execute 

```
make run NARAKEET_API_KEY=(YOUR API KEY) PPTX_FILE=demo.pptx
```


