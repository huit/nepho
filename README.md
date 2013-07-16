Harvard Cloud Deploy Tool
=========================

This tool is intended to be used to deploy applications
to a CloudFormation-compatible IaaS environment such as 
Amazon AWS. The goal is to package CloudFormation and 
similar template resources, configuration management code,
and application code into a plugin-like format. 

This project is very new ....

Functional Spec
---------------

In lieu of actual code, let's define how we expect this to work.

Invocation

    $ hu deploy -E devel drupal
    $ hu undeploy [stack ID]
    $ hu deploy -E prod -hosted myapp
    $ hu list -E devel
    $ hu describe [stack ID]
    
Plugin syntax

(TBD)

- https://github.com/openshift/puppet-openshift_origin


