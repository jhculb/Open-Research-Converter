# GESIS adapted python base project
## Introduction
This project aims to
## Ideal/Intended Development Flow
This assumes usage of VSCode and Devcontainer, though configuration of the desired tools can equally be done on a host machine or VM.

Dev containers allow for shared development baselines, to minimise the chance that 'it works on my machine' is said during development, as the development container allows for (and should encourage) programmatically defined development infrastructure - and therefore should be the same between developers, and minimise issues in deployment or handover.
1. Setup:
	1. Initialise project from py-project-template !!!!!!!!!!!!!!!!!!!
	2. Enable CI/CD on the project
		1. Enable CI/CD via the radio switch toggle found at: Settings - General - Visivility, project features, permissions - CICD
	2. Clone repo to host machine
	3. First time configuration on host machine: (Not required for second instantiation of a dev container)
		2. Add SSH key to ssh-agent on host machine
		2. Install dev-container extension on vscode
			1. This should be prompted once the .devcontainer folder is found
			1. dev-container may require installation of docker desktop (recommended) or an alternative docker host (such as podman)
	4. Switch to !!!!!!!!!!!Dev Container Branch!!!!!!!!!!!!!!!!! (TODO Rename once confirmed)
	5. Start Dev Container
2. Configuration
	1. Development environment configuration
		1. Adjust code quality settings if desired in pyproject.toml
			* These are found under \[tool.*\]
		2. Adjust VSCode development settings in .vscode/settings.json
			* These configure the vscode environment in the project
		3. (TODO: Check whether necessary) Run `pre-commit install` to install pre-commit commands (to automate pre-commit checks and code quality tests)
	2. Project configuration
		1. Change project details in pyproject.toml, Important ones include
			* \[project\]
			* \[tool.flit.module\]
		2. Rename ./src/*python_package*/ to the title of your project
		3. Rename the test import on line 6 of ./tests/test_methods.py to the new name
		4. Edit the ./README.md for your project
	3. CI/CD Configuration
		* The CI/CD for GESIS' gitlab is defined in `.gitlab-ci.yml`
		1. If non-python packages are required in your base image, install them in the script of the base image
		2. !!!!!!!!!!!!!!!!TODO!!!!!!!!!!!!!! SonarQube config
		3. !!!!!!!!!!!!!!!!TODO!!!!!!!!!!!!!!
		4. Configure your automated deployment if desired
		5. Confi
3. Development (Including best practices)
	1. Coding
		1. Best practice - create issue/branch to develop
			1. (Optional) On Gitlab, Create an issue detailing the feature to be edited, or bug to be fixed
			2. (Optional) Create a branch from the issue, using the "create merge request"
			3. (Optional) Pull the changes from the repository with `git fetch --all`
			Switch to the branch locally, then either

				1. Manually, use `git switch *1-branch-name*` to switch to a branch named `1-branch-name`
				1. Using VSCode, switch to branch using the git menu on the bottom left
		2. Write your code
		3. Locally (on the dev container) manually lint, test, typecheck your code:
			* (The following assume you are running the following commands from the root directory of your project, e.g. /workspaces/py-project-template/, as this allows the commands to read the configurations in pyproject.toml)
			* Also note some commands are followed by a period
			3. Use `black .` to automatically format your code
			2. Use `pylint src/python_package` to lint your code
			1. Use `pytest` to test your code
			4. Use `flake8 .` to check your code complies to PEP8
			5. Use `coverage run -m pytest` to compile a report of the test coverage (and simultaneously run pytest)
			6. Use `bandit -r src` to test your source code for security vulnerabilities
			7. Use `pre-commit run` to check (and in some cases fix) staged files for multiple
			8. TODO: Figure out / configure tox, to automatically build and test locally
			9. TODO: Figure out package management with flit
		4. Stage and commit your code
			1. Pre-commit is a system which automatically tests (and in some cases fixes) commits to ensure good code quality on the repository. The configuration is defined in ´.pre-commit-config.yaml´, and if you have changed it, it must be 'reinstalled' through running `pre-commit install`
		5. Push your code to the repository
	2. (Optional) Versioning
		1. One may update the version of code from the top level `__init__.py` in the module, as well as in the `pyproject.toml`
	3. View CI/CD pipeline on project
		1. Once the code has been pushed to the repository, it will follow the pipeline you have configured
		2. The standard pipeline includes enforced linting, testing, typechecking and sonarqube requirements.
		3. One can view the output from these stages on the gitlab page, on CI/CD - Pipelines
			1. If one cannot see CI/CD (Which is in the same menu as "Repository" and "Settings"), one may have not enabled CI/CD in the settings, see the CI/CD configuration above for details
4. Deployment, Hosting and Publishing
	1. As the code is developed, one may wish to automate the following actions:
		* View the code running on a test server
		* Automatically deploy to a production server
		* Publish the module to a local or public PyPI repository
		* Publish the docker image to a local or public Docker repository

### Configuring ssh and git inside the dev container
If one opens the dev container and git diff reports most or all files changed this is likely due to line endings.
If one is unable to pull/push/interact with the remote (due to credentials, so one gets the header when pushing but then is rejected) this is likely because of the
* Ensure ssh key added to Host Environment
	* (e.g ssh-add -l, ensure not "No identities available")
*
https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
#### Known Bugs
* Occasionally when initialising a development container it may report an error
	* Temporary Fix: This error disappears when the development container is rerun
## Useful Commands

## Authors
* John Culbert (john.culbert@gesis.org)
	* Python template configuration
## Thanks
* Microsoft - Daniel Ciborowski
	* Template was adapted from https://github.com/microsoft/python-package-template
* Gitlab - Christian Clauss
	* Template was adapted from https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Python.gitlab-ci.yml
