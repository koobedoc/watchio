# Watchio

!!! warning
    Not developed or released. No commitment to complete :)


This package provides utilities to watch for IO activities of Unix processes. Applications
can use it to reduce updating website static pages.

An example use case is a microserver that displays a list of recently modified files that
have not been checked into a revision control system. A sensible implementation will be to
update static pages when people are viewing the results. The `watchio` module helps to
implement the viewing part when the creation process involves a separate program.


## Installation


Install the package from `pypi.org` by
``` python
pip install watchio
```


## Usage

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


On the command line:

``` shell
watchio 123 456 --timeout 600 --step 10
./update_script.csh
```

