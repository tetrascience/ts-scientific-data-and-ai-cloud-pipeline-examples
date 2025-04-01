# Developing r-exec <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Directory structure](#directory-structure)
- [Running tests](#running-tests)
  - [Configuring Environment](#configuring-environment)

## Directory structure

The directory structure follows that of standard Python repositories using `poetry`.

Python code meant to be imported or otherwise used by this Task Script should only be added to the `ts_task_script_r_exec` directory. Tests should all be located in the `__tests__` directory.

## Running tests

Because this task script is just a wrapper to run the provided R script. No pytest is needed.

### Configuring Environment

Because this task script uses the `before_install` script, we need to run this in a Linux VM to enable local debugging.
But since the R script will only be provided as an input, it's better to run this test on TDP to save the hassle of setting up a VM.
