# Nepho: Harvard Cloud Deploy Tool
### Simplified cloud orchestration tool for constructing virtual data centers

This tool is meant to be a generic wrapper/CLI interface for spinning up complete working environments in an IaaS.  We are initially targeting CloudFormation for orchestration, but hope to expand to OpenStack Heat and other services as they become relevant.  The goal is to package CloudFormation and  similar template resources, configuration management code, and application code into a plugin-like format sothat developers and operations folks can quickly spin up complete environments from their desktops.

## Status

This project is very new, but we have some working code, and are building the framework.

## Installation

Follow the instructions in the wiki for [manual setup](https://github.com/huit/nepho/wiki/Manual-Setup) (until the package is on pypi) and/or [developer setup](https://github.com/huit/nepho/wiki/Development-environment-with-virtualenv) (with virtualenv).

## Configuration

Deployments are configured by using YAML files located in the `./nepho/data/deployments` directory. A sample deployment file that creates a standalone Wordpress site is below:

```yaml
---
development:
  pattern: single-host
  management: puppet
  packages: [php, openssl, telnet, netstat] 

  KeyName: parrott-ec2
  ConfigMgmtGitRepo: https://github.com/huit/wordpress-puppet-build.git
  ConfigMgmtGitRepoBranch: master
```

This deplyoment file specifies a single `environment` named "development" for deploying this app; you can imagine also creating a "staging" and "production" environment with different config values and design patterns involved.

Under the environment, we specify the `pattern` which indicates a design pattern to use
for deploying the application. In this case, we get a single host that's not in an autoscaling group
and that has an elastic IP for connectivity. By default this design pattern opens web-related ports, but
this can be manged via a parameter.

The configuration management methodology to use on the instance is specified via
the `management` parameter, which in this case is "puppet." For now this assumes that this
is via a standalone puppet manifest, which is sourced from a git repository somewhere,
specified in the `GitRepo` and `GitRepoBranch` parameters. This parameter will have more 
options in the future.

In addition, we specify a set of yum `packages` as a YAML list, and a `KeyName` which indicates
which SSH public key, registered with AWS, to use.

## Usage

We are working toward a plugin-oriented architecture for orchestration tools, but for now
the driver is specific to Amazon Web Services. (Note: in the following, we assume that the
`nepho` command is in your `PATH`, and that your `PYTHONPATH` is setup properly to include the `nepho/` directory.)

Given a working (1) design pattern, and (2) deployment file, the following commands are available:

Print out the generated template file as JSON:

    $ nepho -E [environment] show-template [deployment]
    
Validate the template file

    $ nepho -E [environment] validate-template [deployment]

Print out the template parameters that you can specify in the deployment file:

    $ nepho -E [environment] show-params [deployment]

Do the actual deploy of the application and pattern:

    $ nepho -E [environment] deploy [deployment]

Delete the deployment from the provider:

    $ nepho -E [environment] delete [deployment]


TBD: more detailed options, etc.

# Resources

## Functional Spec

Let's define how we expect this to work.

## Invocation

    $ nepho deploy -E devel drupal
    $ nepho show-template drupal
    $ nepho undeploy [stack ID]
    $ nepho deploy -E prod -hosted myapp
    $ nepho list -E devel
    $ nepho describe [stack ID]
    $ nepho delete [stack ID]
    
## Module syntax and layout

When you invoke a module by name and by "environment" (i.e. development, testing, production, etc.) as follows:

    $ nepho deploy -E development drupal
 
The deployment tool will search for a CloudFormation template file at the path 
`./modules/drupal/development.cf` and use this as the basis of the rendered CloudFormation template. 
In addition, the system looks for a YAML file at `./modules/drupal/development.yaml` which defines any
CloudFormation "parameters", values you would normally provide on the command line when using 
CloudFormation command line tools or APIs. This file lets you package a specific set of environments
along with the CloudFormation template, so that these values are prepackaged. In addition to this file, you can 
define a `./local.yaml` file which let's you specify and override your specific values for this session.

In addition to the CloudFormation templates in JSON, you can use the Jinja2 templating syntax to make these 
templates modular, to comment them, and to add additional logic within the templating syntax itself. This let's us
build a common library of boilerplate CloudFormation template snippets and simply include these snippets. 
This is a real help in creating easy-to-read modules, since the CloudFormation syntax is very verbose.

As an example ..... (TBD)

## Useful examples:

### Three-tier VPC

Deploy a 3 tier VPC that's bare (i.e. no application instances ot databases). Before you run, be sure to change the
relevant keypair in `modules/vpc-three-tier-bare/development.yaml` to reflect yours (see issue on implementing local 
overrides for parameters).

    $ ./bin/nepho validate-template -E development vpc-three-tier-bare
    $ ./bin/nepho deploy -E development vpc-three-tier-bare
    $ ./bin/nepho deploy -E development vpc-three-tier-bare
    $ aws cloudformation list-stacks
    $ ./bin/nepho destroy -E development vpc-three-tier-bare
    
There is also a "populated" application VPC module in progress.    
