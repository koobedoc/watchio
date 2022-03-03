# API watchio 



<style>
h4.class-method + dl { /* Indent dl following class-method */
  margin-left: 2em;
  margin-top: -1em;
}
h4.class-method {
    margin-left: 2em;
}
</style>



### *class* WatchIO
:   Process IO watcher


####\_\_init\_\_ (self, pids: list = None, *, timeout: float = 600, step: float = 1) #### {: .anchor .class-method  data-toc-label='\_\_init\_\_' }
:   Constructor for WatchIO, call with keyword arguments.

    *pids* is a list of process PIDs to watch. Non-valid PIDs are silently
    ignored.

    *timeout* sets the default timeout value for the poll() methed.

    *step* sets the default step value, the interval we check
    the /proc/ file, in seconds for the poll() method.


####get\_io\_data (self, pid: int) -> dict #### {: .anchor .class-method  data-toc-label='get\_io\_data' }
:   Get IO data of the `pid` process. The method reads and parses the
    file "/proc/{pid}/io" and returns a dictionary with values in int.
    See  [https://man7.org/linux/man-pages/man5/proc.5.html](https://man7.org/linux/man-pages/man5/proc.5.html) for the definition
    of values.

    *pid* is the process ID to get the io data. The method returns None
    if the process does not exist. TODO: no read access.


####main\_cli () #### {: .anchor .class-method  data-toc-label='main\_cli' }
:   Unix command line interface


####parse\_cli (self) #### {: .anchor .class-method  data-toc-label='parse\_cli' }
:   Parse Unix command line arguments


####poll (self, timeout: float = None, step: float = None) -> int #### {: .anchor .class-method  data-toc-label='poll' }
:   Poll the IO activities. The method checks for IO activities every
    `step` seconds. It returns the number of processes with new IO
    activities since the last update() or poll(); or returns 0 if
    the wait time has exceeded `timeout` seconds.

    *timeout* defaults to instance value if not given.

    *step* defaults to instance value if not given.


####update (self) -> int #### {: .anchor .class-method  data-toc-label='update' }
:   Update IO activities. Returns the number of process with new IO activities
    since the last update() or poll().




