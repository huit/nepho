Harvard Cloud Deploy Tool
=========================

This tool is intended to be used to deploy applications
to a CloudFormation-compatible IaaS environment such as 
Amazon AWS. The goal is to package CloudFormation and 
similar template resources, configuration management code,
and application code into a plugin-like format. 

Status
------

This project is very new, but we have some working code, and are building the framework.


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





