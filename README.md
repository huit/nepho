# nepho [![PyPI version](https://badge.fury.io/py/nepho.png)](http://badge.fury.io/py/nepho) [![Build Status](https://travis-ci.org/huit/nepho.png?branch=master)](https://travis-ci.org/huit/nepho)
### Command line cross-cloud orchestration tool for constructing virtual datacenters

Nepho is a command-line tool that orchestrates the creation of complete working application stacks on virtual infrastructure.  Initially targeting Amazon Web Services as well as Vagrant, Nepho abstracts datacenter creation, instance configuration, and application deployment into portable "cloudlets" that can be shared between developers and teams.

With Nepho, DevOps engineers can construct complete infrastructure-as-code bundles ("cloudlets") that anyone can easily spin up with a single command.  Nepho is in active development.

To learn more about the key concepts and vocabulary of Nepho, please view the [structure of a cloudlet](https://github.com/huit/nepho/wiki/Structure-of-a-cloudlet) page.


## Status

This project is new but being actively developed by the Cloud Engineering team within Harvard University Information Technology.  We have released a stable 1.0 release that is being used by teams within Harvard.  We welcome your feedback and contributions!

Currently there are two main code branches:

* **master** - refactoring into a generic _core_, vendor-specific _providers_, and _cloudlets_ for each individual application/service environment.
* **legacy** - legacy code for constructing CloudFormation stacks using Jinja2 templated JSON files, slowly being merged into master.


## Installation
### Standard installation
View our [getting started guide](https://github.com/huit/nepho/wiki/Getting-Started) for complete instructions for setting up Nepho and its dependencies.

On Windows, you will need to [install Python](http://www.python.org/getit/windows/) in addition to the other requirements, more detailed instructions for Windows users are coming soon.

### Installation for developing Nepho
If you plan to develop on the Nepho codebase you will want to follow the instructions for [developer setup](https://github.com/huit/nepho/wiki/Development-environment-with-virtualenv) using virtualenv.


## Configuration

By default Nepho will create a hidden configuration directory in your home directory (`~/.nepho`) although you can specify a different location in the configuration file.  Running the `nepho scope` command will create a configuration file for you (`~/.nepho/config`) if one does not exist, but in general you will not need to modify any of the default configuration options.

Nepho passed configuration information into providers (i.e. AWS, Vagrant) through a parameter management system.  Each provider, cloudlet, and blueprint may specify required or optional parameters.  You can view and manipulate parameters using the `nepho parameter` subcommand.

Examples of some common parameters (which use the CamelCase format):

* AWSRegion: us-east-1
* VagrantBackend: virtualbox
* UpdatePackages: False


## Usage

Consult the built-in documentation (`nepho --help`) for the latest information about commands and arguments.  Nepho supports the following five subcommands:

* `nepho cloudlet` - find, download, and manage cloudlets
* `nepho blueprint` - list and view individual cloudlet deployment blueprints
* `nepho stack` - create, manage, and destroy stacks built from blueprints
* `nepho parameter` - list, view and modify parameter settings
* `nepho scope` - set a cloudlet (and optionally blueprint) scope for future commands

Find out more about each subcommand by running `nepho <subcommand> --help`
