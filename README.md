![build status](https://travis-ci.org/eitanhaimashiah/bci.svg?branch=master)
![coverage](https://codecov.io/gh/eitanhaimashiah/bci/branch/master/graph/badge.svg)

# BCI

See [full documentation](https://advanced-system-design-foobar.readthedocs.io/en/latest/).

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

## Usage

The `bci` package provides a command-line interface:

```sh
$ python -m bci --version
bci, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `run_server`, `upload_thought` and `run_webserver` commands:

```sh
$ python -m bci run_server "127.0.0.1:5000" data/
```
```sh
$ python -m bci upload_thought "127.0.0.1:5000" 1 "I'm sleepy"
done
```
```sh
$ python -m bci run_webserver "127.0.0.1:8000" data/
 * Serving Flask app "project.web" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 199-477-134
127.0.0.1 - - [12/Dec/2019 20:15:37] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [12/Dec/2019 20:15:39] "GET /users/3 HTTP/1.1" 200 -
....
```
Do note that each command's options should be passed to *that* command, so for 
example the `-q` and `-t` options should be passed to `project`, not `run_server`, 
`upload_thought` or `run_webserver`.

```sh
$ python -m bci run_server -q "127.0.0.1:5000" data/ # this doesn't work
ERROR: no such option: -q
$ python -m bci -q run_server "127.0.0.1:5000" data/ # this does work
```
