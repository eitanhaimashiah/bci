![build status](https://travis-ci.org/eitanhaimashiah/bci.svg?branch=master)
![coverage](https://codecov.io/gh/eitanhaimashiah/bci/branch/master/graph/badge.svg)

# BCI

Brain Computer Interface (BCI) is a system that can read minds, and upload 
snapshots of cognitions. Our system includes a [client](#the-client), which 
streams cognition snapshots to a [server](#the-server), which then publishes 
them to a [message queue](#the-message-queue-and-the-parses), where multiple 
[parsers](#the-message-queue-and-the-parses) read the snapshot, parse various 
parts of it, and publish the parsed results, which are then saved to a 
[database](#the-database-and-the-savers). The results are then exposed via a 
RESTful [API](#the-api), which is consumed by a [CLI](#the-cli); there's also 
a [GUI](#the-guiE
), which visualizes the results in various ways.

See [full documentation](https://bci.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:eitanhaimashiah/bci.git
    ...
    $ cd bci/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [bci] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```   

## Running the whole pipeline

1. To start the container of each component in the pipeline one by one, 
    just run: 

    ```sh
    $ ./scripts/run-pipeline.sh
    ...
    ```

2. Once the above is done, run a client to upload a sample:
    
    ```sh
    $ python -m bci.client upload-sample 'test_sample.mind'
    ```
   
3. Check out the Web Server at `http://localhost:8080` to see the 
    uploaded sample.

4. To stop the whole pipeline, run:
    
    ```sh
    $ ./scripts/stop-pipeline.sh
    ```
    
## Usage

The `bci` package provides an application programming interface (API) 
alongside a command-line interface (CLI). The `bci`'s components are 
listed in the following sections.

To show the package version through CLI, run:

```sh
$ python -m bci --version
bci, version 0.1.0
```

All CLI commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).



### The client

### The server

### The message queue and the parses
<!-- TODO Provide documentation about how to add a new parser: 
what would I need to do to be able to have the parse command invoke 
my own code, and the run-parser command to run it as a service 
working with a message queue. -->

### The database and the savers

### The API
 
### The CLI

### The GUI
