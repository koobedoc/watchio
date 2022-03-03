# Watchio

!!! warning
    Work in progress. Have not reached the stable release 0.1.0


This package provides utilities to watch for IO activities of Unix processes. It works by
reading the Unix process information file `/proc/{pid}/io` periodically.

An example use case is a microserver that displays static web pages created by a different
program that takes a moderate amount of resources. A sensible implementation will be to
update the static pages only when users are viewing the results. The `watchio` module
helps to watch for IO activities of the server.

Install the package from `pypi.org` by
``` python
pip install watchio
```


## Usage

### In Python

Use in a polling loop in code:

```python
app_ios = watchio.WatchIO([123, 456])

## Use in a polling loop to update static web pages
## poll() will return an integer
##    -1:  every 600 seconds, or
##    >0:  there are IO activities (checked every 5 seconds)
while True:
    if app_ios.poll(timeout=600, step=5):
        ## main work
        ....
```


### On the command line

``` shell
watchio 1234 2234 --timeout 600 --step 10
./update_script.csh
```


The following kills a butch of processes that has no IO activities after 1 hour.
``` shell
watchio 1234 2234--timeout 3600 --kill
```



## Development


* On github: [https://github.com/koobedoc/watchio](https://github.com/koobedoc/watchio)
* On PyPI: [https://pypi.org/project/watchio/](https://pypi.org/project/watchio/)