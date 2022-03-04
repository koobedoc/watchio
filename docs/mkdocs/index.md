# Watchio


<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-BNH3BTJ9ME"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-BNH3BTJ9ME');
</script>


!!! warning
    Work in progress. Have not reached the stable release 0.1.0


This package provides utilities to watch for IO activities of Unix processes. It works by
reading the Unix process information file `/proc/{pid}/io` periodically. Therefore, you
can only use it on a system where `/proc` is mounted, and for processes you have tracing
access to.

An example use case is a microserver displaying static web pages created by a separate
program that takes a moderate amount of resources. A sensible implementation is to update
the static pages only when users are viewing the results. The `watchio` module helps to
watch for IO activities of the server.

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
watchio poll 1234 2234 --timeout 600 --step 10
./update_script.csh
```

<!-
The following kills a butch of processes that has no IO activities after 1 hour.
``` shell
watchio poll 1234 2234 --timeout 3600 --kill
```
->

## See Also

* [proc file system man page](https://man7.org/linux/man-pages/man5/proc.5.html)
* [iostat man page](https://linux.die.net/man/1/iostat)
* Code on github: [https://github.com/koobedoc/watchio](https://github.com/koobedoc/watchio)
* Package on PyPI: [https://pypi.org/project/watchio/](https://pypi.org/project/watchio/)