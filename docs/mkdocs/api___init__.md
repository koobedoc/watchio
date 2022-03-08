# API watchio 



<style>
h4.class-method + dl { /* Indent dl following class-method */
  margin-left: 2em;
  margin-top: -1em;
}
h4.class-method {
    margin-left: 2em;
}
h4.class-method .highlight {
    font-weight: normal;
}
</style>



### *class* WatchIO
:   Process IO watcher.


#### \_\_init\_\_ <span class="highlight"><span></span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">pids</span><span class="p">:</span> <span class="nb">list</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span> <span class="o">*</span><span class="p">,</span> <span class="n">timeout</span><span class="p">:</span> <span class="nb">float</span> <span class="o">=</span> <span class="mi">600</span><span class="p">,</span> <span class="n">step</span><span class="p">:</span> <span class="nb">float</span> <span class="o">=</span> <span class="mi">1</span><span class="p">,</span> <span class="n">check</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span></span> #### {: .anchor .class-method  data-toc-label='\_\_init\_\_' }
:   Constructor for WatchIO, call with keyword arguments.

    *pids* is a list of process PIDs to watch. Non-valid PIDs are silently
    ignored unless `check` is enabled.

    *timeout* sets the default timeout value for the poll() method.

    *step* sets the default step value, the interval we check
    the /proc/{pid}/io file, in seconds for the poll() method.

    *check* raises exceptions (PermissionError if not accessible or FileNotFoundError for
    non-existent process) instead of silently ignoring bad pids by default.


#### get\_io\_data <span class="highlight"><span></span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">pid</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span></span> #### {: .anchor .class-method  data-toc-label='get\_io\_data' }
:   Get IO data of the `pid` process. The method reads and parses the
    file "/proc/{pid}/io" and returns a dictionary with values in int.
    See https://www.kernel.org/doc/html/latest/filesystems/proc.html#proc-pid-io-display-the-io-accounting-fields
    for a description of the fields.

    *pid* is the process ID to get the io data. The method returns None
    if the process does not exist. TODO: no read access.


#### main\_cli <span class="highlight"><span></span><span class="p">()</span></span> #### {: .anchor .class-method  data-toc-label='main\_cli' }
:   Unix command line interface


#### parse\_cli <span class="highlight"><span></span><span class="p">(</span><span class="bp">self</span><span class="p">)</span></span> #### {: .anchor .class-method  data-toc-label='parse\_cli' }
:   Parse Unix command line arguments


#### poll <span class="highlight"><span></span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">timeout</span><span class="p">:</span> <span class="nb">float</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span> <span class="n">step</span><span class="p">:</span> <span class="nb">float</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span> <span class="n">clear</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">int</span></span> #### {: .anchor .class-method  data-toc-label='poll' }
:   Poll the IO activities. The method checks for IO activities every
    `step` seconds. It returns the number of processes with new IO
    activities since the last update() or poll(); or returns 0 if
    the wait time has exceeded `timeout` seconds.

    *timeout* defaults to instance value if not given.

    *step* defaults to instance value if not given.

    *clear* (default is False) clears the IO counters so that polling uses
    only IO activities after this function has started.


#### update <span class="highlight"><span></span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">int</span></span> #### {: .anchor .class-method  data-toc-label='update' }
:   Update IO activities. Returns the number of process with new IO activities
    since the last update() or poll(). Returns -1 if no PID is valid.




