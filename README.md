Nepho: Harvard Cloud Deploy Tool
=========================

This tool is intended to be used to deploy an 
applications to a CloudFormation-compatible IaaS environment such as 
Amazon AWS, and in the future to any orchestratable 
IaaS environment, including OpenStack, Vagrant, VMware,
etc. The goal is to package CloudFormation and 
similar template resources, configuration management code,
and application code into a plugin-like format. 

The framewotk

Status
------

This project is very new, but we have some working code, and are building the framework.

Installation
------------

Requires:

- python 2.6 or newer
- boto
- awscli
- jinja2


Configuration
-------------

Deployments are configured by using YAML files located in the `./deployments` directory. A sample 
deployment file that creates a standalone Wordpress site is below:

    ---
    
    development:

      pattern: single-host
      management: puppet
      packages: [php, openssl] 
  
      KeyName: parrott-ec2
      GitRepo: https://github.com/huit/wordpress-puppet-build.git
      GitRepoBranch: master
      ExtraPackages: telnet netstat

This deplyoment file specifies a single `environment` named "development" for deploying this app;
you can imagine also creating a "testing" and "production" environment with different 
config values and design patterns involved.

Under the environment, we specify the `pattern` which indicates a design pattern to use
for deploying the application. In this case, we get a single host that's not in an autoscaling group
and that has an elastic IP for connectivity. By default this design pattern opens web-related ports, but
this can be manged via a parameter.

The configuration management methodology to use on the isntance is specified via
the `management` parameter, which in this case is "puppet." For now this assumes that this
is via a standalone puppet manifest, which is sourced from a git repository somewhere,
specified in the `GitRepo` and `GitRepoBranch` parameters. This parameter will have more 
options in the future.

In addition, we specify a set of yum `packages` as a YAML list, and a `KeyName` which indicates
which SSH public key, registered with AWS, to use.


Usage
-----

We are working toward a plugin-oriented architecture for orwechstration tools, but for now
you'll need to invoke the driver directly, in particular `./bin/hu-awd` for 
Amazon Web Services.

Given a working (1) design pattern, and (2) deployment file, the following commands are available:

Print out the generated template file as JSON:

    $ ./bin/hu -E [environment] show-template [deployment]
    
Validate the template file

    $ ./bin/hu -E [environment] validate-template [deployment]

Print out the template parameters that you can specify in the deployment file:

    $ ./bin/hu -E [environment] show-params [deployment]

Do the actual deploy of the application and pattern:

    $ ./bin/hu -E [environment] deploy [deployment]

Delete the deployment from the provider:

    $ ./bin/hu -E [environment] delete [deployment]


TBD: more detailed options, etc.

    
Examples
--------

Resources
---------
## Functional Spec

Let's define how we expect this to work.

### Invocation

    $ hu deploy -E devel drupal
    $ hu show-template drupal
    $ hu undeploy [stack ID]
    $ hu deploy -E prod -hosted myapp
    $ hu list -E devel
    $ hu describe [stack ID]
    $ hu delete [stack ID]
    
### Module syntax and layout

When you invoke a module by name and by "environment" (i.e. development, testing, production, etc.) as follows:

    $ hu deploy -E development drupal
 
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

    $ ./bin/hu-aws validate-template -E development vpc-three-tier-bare
    $ ./bin/hu-aws deploy -E development vpc-three-tier-bare
    $ ./bin/hu-aws deploy -E development vpc-three-tier-bare
    $ aws cloudformation list-stacks
    $ ./bin/hu-aws destroy -E development vpc-three-tier-bare
    
There is also a "populated" application VPC module in progress.    





