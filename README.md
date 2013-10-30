# nepho
### Command line cross-cloud orchestration tool for constructing virtual datacenters

Nepho is a generic wrapper/CLI interface for spinning up complete working application stacks in virtual environments.  Nepho abstracts datacenter creation, instance configuration, and application deployment into portable "cloudlets" that can be shared between developers and teams.

Nepho is in active development, working towards a 1.0 release.  Currently there are two main code branches:
* **legacy** - legacy code for constructing CloudFormation stacks using Jinja2 templated JSON files
* **master** - refactoring into a generic _core_, vendor-specific _providers_, and _cloudlets_ for each individual application/service environment.

## Status

This project is very new, but we have some working code, and are building the framework.  We plan to soon have a working version available as a Python package along with example cloudlets that users can build upon.

## Installation

Follow the instructions in the wiki for [manual setup](https://github.com/huit/nepho/wiki/Manual-Setup) (until the package is on pypi) and/or [developer setup](https://github.com/huit/nepho/wiki/Development-environment-with-virtualenv) (with virtualenv).

## Configuration

All application (global) configuration and cloudlets are located under the `.nepho` directory in the user's home directory.

## Usage

Commands have been changing as we refactor, consult the built-in documentation (`nepho --help`) for the latest information about commands and arguments.
