#!/usr/bin/env python3
""" Tests for watchio module """

import os
import time
import sys

import pytest

sys.path = ["../src"] + sys.path

import watchio


def test_constructor():
    """Tests for constructor"""

    ## Checks defaults
    iow = watchio.WatchIO([1])
    assert str(iow) == "<WatchIO pids=[1] timeout=600 step=1>"

    iow = watchio.WatchIO([2], timeout=3456, step=7)
    assert str(iow) == "<WatchIO pids=[2] timeout=3456 step=7>"


def test_delay():
    """Tests for delays in polling"""

    iow = watchio.WatchIO([os.getpid()])

    print("// First time calling, poll should exit immediately")
    start_time = time.time()
    ret = iow.poll(timeout=3)
    print(f"// Returned {ret}. Elapsed = {time.time() - start_time:.3f}s")
    assert (time.time() - start_time) < 0.1

    print("// Now we run again. It should timeout")
    iow.update()  ### To flush out changes print print statments
    start_time = time.time()
    ret = iow.poll(timeout=0.2, step=0.1)
    elapsed = time.time() - start_time
    print(f"// Returned {ret}. Elapsed = {elapsed:.3f}s")
    assert 0.2 < elapsed < 0.3


def test_misc():
    """Misc tests"""

    print("dir(watchio):", dir(watchio))

    print(watchio.__version__)

    iow = watchio.WatchIO([os.getpid()])
    data1 = iow.get_io_data(os.getpid())
    print(data1)


if __name__ == "__main__":

    pytest.main()
