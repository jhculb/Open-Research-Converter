# GESIS adapted python base project
## Introduction
This project aims to
## Setup
### Configuration
To Change - all references to python_project
### VSCode Development Environment
Following Microsoft, the use of VSCode Development containers allows for an automated initialisation of a reproducible environment. This can be configured and shared via editing the dockerfile and
#### Configuring ssh
This worked for me:
* Ensure ssh key added to Host Environment
	* (e.g ssh-add -l, ensure not "No identities available")
*
https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
#### Known Bugs
* Occasionally when initialising a development container it may report an error
	* Temporary Fix: This error disappears when the development container is rerun
## Usage - Development

### Useful Commands
## Information
### Default CI/CD
## Publishing
## Deployment

## Authors
* John Culbert (john.culbert@gesis.org)
	* Python template configuration
* Alexander Mühlbauer
	* Deployment configuration
## Thanks
* Microsoft - Daniel Ciborowski
	* Template was adapted from https://github.com/microsoft/python-package-template
* Gitlab - Christian Clauss
	* Template was adapted from https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Python.gitlab-ci.yml
