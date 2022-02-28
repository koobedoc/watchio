
PYTHON_SRC := $(wildcard *.py)
PYTHON_PYLINT := $(patsubst %,.tmp/%.pylint,$(PYTHON_SRC))
PYTHON_BLACK := $(patsubst %,.tmp/%.black,$(PYTHON_SRC))
PYTHON_PYTYPE := $(patsubst %,.tmp/%.pytype,$(PYTHON_SRC))


top:
	@echo $(PYTHON_SRC)
	@echo $(PYTHON_PYLINT)

all: fmt pylint


fmt: $(PYTHON_BLACK)

pylint: $(PYTHON_PYLINT)

pytype: $(PYTHON_PYTYPE)

.tmp/%.black: %
	@mkdir -p .tmp
	black -l 120 $< | tee $@

.tmp/%.pytype: %
	@mkdir -p .tmp
	pytype $< | tee $@

.tmp/%.pylint: %
	@mkdir -p .tmp
	@pylint --extension-pkg-whitelist='pydantic' \
        --init-hook='import sys; sys.path.append(".")' -d bad-continuation -d line-too-long $< | tee $@

serve:
	uvicorn server:app --reload --port 5000



