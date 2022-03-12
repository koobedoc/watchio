# Watchio

*WatchIO - Python package to watch process IO.*

The `watchio` package provides utilities to watch for IO activities of Unix processes. It
works by reading the Unix process information file `/proc/{pid}/io` periodically. You can
only use it on a system where `/proc` is mounted, and for processes that you have tracing
access to.

An example use case is a microserver displaying static web pages created by a separate
program that takes a moderate amount of resources. A sensible implementation updates the
static pages only when users are viewing the results. The `watchio` module helps to watch
for IO activities of the server when the server has no other convenient indications of
activities
(such as saving accesses to a log file).

Install the package from `pypi.org` by
``` python
pip install watchio
```


## Usage

In a polling loop in Python code:

```python
watcher = watchio.WatchIO([123, 456])

## Use in a polling loop to update static web pages
## poll() will return an integer
##    -1:  every 600 seconds, or
##    >0:  there are IO activities (checked every 10 seconds)
while True:
    if watcher.poll(timeout=600, step=10):
        ## main work
        ....
```


On the Unix command line

``` shell
watchio poll 1234 vim --timeout 600 --step 10
./update_script.csh
```
Only processes owned by you are allowed. You can supply a process name instead of a
numerical process ID and `watchio` will look up all processes owned by you having that
name.

## See Also

* [Unix /proc file system man page](https://man7.org/linux/man-pages/man5/proc.5.html)
* [iostat man page](https://linux.die.net/man/1/iostat)
* Code on github: [https://github.com/koobedoc/watchio](https://github.com/koobedoc/watchio)
* Package on PyPI: [https://pypi.org/project/watchio/](https://pypi.org/project/watchio/)

* Online documentation: [https://koobedoc.github.io/watchio/](https://koobedoc.github.io/watchio/)


## Project Information

    python-depends: psutil
    docs: mkdocs
    python-modules:  watchio
    python-packages: watchio


