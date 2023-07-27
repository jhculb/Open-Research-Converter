# GESIS Python Project Template
Version 0.1.0 - Beta Testing
# Table of Contents

- [GESIS Python Project Template](#gesis-python-project-template)
- [Table of Contents](#table-of-contents)
- [To-do and In development](#to-do-and-in-development)
  * [Known Bugs / Issues](#known-bugs---issues)
  * [Infrastructure & Integration](#infrastructure---integration)
- [Introduction](#introduction)
  * [Integration into preexisting project](#integration-into-preexisting-project)
  * [First Time Initialisation Runtime](#first-time-initialisation-runtime)
- [Ideal/Intended Development Flow](#ideal-intended-development-flow)
  * [Configuring ssh and git inside the dev container](#configuring-ssh-and-git-inside-the-dev-container)
- [Useful Commands and Information](#useful-commands-and-information)
  * [Badges](#badges)
  * [Template and GitLabs READMEs](#template-and-gitlabs-readmes)
- [Authors](#authors)
  * [Author](#author)
  * [Maintainer](#maintainer)
  * [Thanks](#thanks)
- [Feedback and contribution](#feedback-and-contribution)
- [Variables](#variables)
  * [List of Template Variables and Locations](#list-of-template-variables-and-locations)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# To-do and in-development
## Known Bugs / Issues
* ssh -T fails to authenticate git@git.gesis.org, even though ssh-add -L shows the key.
	* The Host's Windows default ssh client must be v8.9 or above, to see the current version run: `ssh -V`
	* To update openssh, in powershell run: `winget install "openssh beta"`
	* Reboot the host
	* Also detailed in [this section](#configuring-ssh-and-git-inside-the-dev-container)
## Infrastructure & Integration
* Configure for deployment to Gitlab Docker Repository
	1. Check whether this is desired
	2. Add repository to gitlab-ci.yml
	3. Add configuration for project template
* Configure template for SonarQube key and set stage as optional depending on presence of key

# Introduction
This project aims to provide a template for python module development which allows for quick configuration of good development practice and standard adherence at GESIS.

The project includes:
* A standard project structure and dependency & configuration management file
	* Following PEP 621
* Pre-configured CI/CD, which allows for
	* Automated code quality enforcement
	* Automated deployment, publishing, hosting, etc.
* Pre-configured tool settings
	* Development tools such as black, pylint and flake8 can often conflict with each other, requiring developers to discover and then sort out problems - leading to lost development time.
	* The pyproject.toml has (hopefully) all the conflicts
* An optional devcontainer environment intended for use with VSCode, which allows for
	* A standardised development environment between developers
	* Programmatic configuration of the development environment
	* Quick teardown/reinstantiation of development environments
	* Enforced code quality checks

## Integration into preexisting project
While awaiting the template format from the gitlab host - (bitbone), please follow the following:

It is recommended that the repository directory structure is formatted to mirror the template structure.

Run the following commands:
1. `git remote add py-template git@git.gesis.org:devops/project-templates/py-project-template.git`
2. `git fetch py-template --tags`
3. `git merge --allow-unrelated-histories py-template/release`
	* If a different branch is desired, change the branch name following `/` in the above command
## First Time Initialisation Runtime
When running for the first time, due to docker downloading all containers from docker-hub and poetry installing all packages, it may take around 5 minutes to open the development container, and 10 minutes for everything to install. Please be patient and let it run uninterrupted, future initalisations will be faster.

# Ideal/Intended Development Flow
This assumes usage of VSCode and optionally development containers (dev containers), though configuration of the desired tools can equally be done on a host machine or a virtual machine.

A less complete version of the template can be used directly on host machines or virtual machines by running `make install_locally`, and not following the instructions marked [Dev Container]. You may delete the `/.devcontainer/` folder if so.

Similarly the template can be used with any code editor but has been configured for VSCode, if you are not using VSCode you may delete the `/.vscode/` folder.

[BETA TESTERS]
The current release requires use of VSCode to use the development container. Please let the me know the demand for configuring a non-vscode development container.
[/BETA TESTERS]

Dev containers  allow for shared development baselines, to minimise the chance that 'it works on my machine' is uttered during development, as the development container allows for (and should encourage) programmatically defined development infrastructure - and therefore should be the same between developers, and minimise migration issues in deployment or handover.
## Installation and Configuration Instructions
1. Setup of host machine and gitlab project:
	1. Initialise project from py-project-template
		1. Currently awaiting GESIS' gitlab hosts to migrate the project to a template
		1. While awaiting migration, fork the repository
	2. Enable CI/CD on the project
		1. Enable CI/CD via the radio switch toggle found at: Settings - General - Visibility, project features, permissions - CICD
	2. Clone repo to host machine
	3. First time configuration on host machine: (Not required for second instantiation of a dev container)
		1. Add SSH key to ssh-agent on host machine
		2. [Dev Container] Install dev-container extension on vscode
			1. This should be prompted once the .devcontainer folder is found
			1. dev-container may require installation of docker desktop (recommended) or an alternative docker host (such as podman), or WSL2 (untested)
		3. Configure git on host machine to pass details onto
			1. Ensure that git.name and git.email are set on host machine
				1. If not please run the following commands replacing the placeholders with your details
					1. `git config --global user.name "Your Name"`
					2. `git config --global user.email "your.email@gesis.org"`
			2. Add your SSH key to the local SSH agent
				1. On Windows:
					1. Run `ssh-add $HOME/.ssh/github_rsa` (or replace destination or key format if keys are stored outside the home directory, or if using a RSA key respectively)
					2. If there is an error as the SSH agent is not running:
						1. Ensure sure you're running poweshell as an Administrator
						2. Run `Set-Service ssh-agent -StartupType Automatic`
						2. Run `Start-Service ssh-agent`
						2. Run `Get-Service ssh-agent`
						2. Then rerun the `ssh-add ...` command as above
			3. Further details (including Linux and MacOS startup details) can be found https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
	5. [Dev Container] Start the dev container
2. Configuration of Project
	1. Development environment configuration
		1. Adjust code quality settings in pyproject.toml if desired
			* These are found under \[tool.*\]
		2. Adjust VSCode development settings in .vscode/settings.json if desired
			* These configure the vscode environment in the project
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
			1. This can be done by editing the script section of an image in the `.gitlab-ci.yml`.

			It is recommended that the installations are made on the "Base" image in gitlab. However as the installation will be done each time the CI/CD is ran, this is recommended for lightweight non-python packages only. If a package takes a long time to install, it is worth reaching out to the maintainer of this project to configure a new base container which comes with the package already installed.

			If a python package takes a long time to install and is slowing CI/CD - e.g. Keras,TensorFlow, Spark, ..., please contact the maintainer to provide a base container with these preinstalled.
		2. SonarQube Configuration
			* *In development*
		3. Configure your automated deployment
		4. [Optional] Add/Configure relevant badges for your project.
			1. By editing `generate_badges.py`, one may add information to the project page about the health, quality or other relevant statistics.
				* The output is generated in the `generate-badges` stage of deployment and is manually activated by default. It can be configured to run only on a particular branch, such as main, or release.
				* The output from this stage is a svg file that is the badge, and will output this to the artifacts section.
				To add this to your project you can go in Gitlab to Settings - General - Badges. You must then provide the following information:
				*
					* A name for the badge
					* A URL to where clicking this badge will take you to
					* A URL to the svg generated by the stage. E.g.
						* https://git.gesis.org/%{project_path}/-/jobs/94239/artifacts/raw/badges/python_version.svg
						* This path can be configured with more wildcards. Please see the [gitlab documentation](https://git.gesis.org/help/user/project/badges) and [anybadge documentation](https://pypi.org/project/anybadge/1.2.0rc4/) for more information.
3. Intended Development Workflow (Including best practices)
	1. Coding
		1. Best practice - create issue/branch to develop
			1. (Optional) On Gitlab, Create an issue detailing the feature to be edited, or bug to be fixed
			2. (Optional) Create a branch from the issue, using the "create merge request"
			3. (Optional) Pull the changes from the repository with `git fetch --all`
			Switch to the branch locally, then either
				1. Manually, use `git switch *1-branch-name*` to switch to a branch named `1-branch-name`
				1. Using VSCode, switch to branch using the git menu on the bottom left
		2. Write your code
			1. To install packages run: `poetry install <package-name>`
		3. Locally (on the dev container) you may manually lint, test, typecheck your code:
			* The development container is automatically configured to assist your code by formatting automatically on save, and running a suite of code-quality commands at commit.
			* (The following instructions assume you are running the following commands from the root directory of your project, e.g. /workspaces/py-project-template/, as this allows the commands to read the configurations in pyproject.toml)
			* Also note some commands are followed by a period to denote the top level of the repository
			3. Use `black .` to automatically format your code
			2. Use `pylint src/python_package` to lint your code
			1. Use `pytest` to test your code
			4. Use `flake8 .` to check your code complies to PEP8
			5. Use `coverage run -m pytest` to compile a report of the test coverage (and simultaneously run pytest)
			6. Use `bandit -r src` to test your source code for security vulnerabilities
			7. Use `pre-commit run` to check (and in some cases fix) staged files for multiple
			8. TODO: Figure out / configure tox, to automatically build and test locally
		4. Stage and commit your code
			1. Pre-commit is a system which automatically tests (and in some cases fixes) commits to ensure good code quality on the repository. The configuration is defined in ´.pre-commit-config.yaml´, and if you have changed it, it must be 'reinstalled' through running `pre-commit install`, or rebuilding the development container
		5. Push your code to the repository
	2. (Optional) Versioning
		1. One may update the version of code from the top level `__init__.py` in the module, as well as in the `pyproject.toml`
		2. When publishing to the local repository a unique package name must be provided - therefore updating the `pyproject.toml` version is required to increment the version number provided to the package repository.
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

### Configuring SSH and Git inside the dev container
If one opens the dev container and `git diff` reports most or all files changed this is likely due to line endings.

If one is unable to pull/push/interact with the remote (due to credentials, so one gets the header when pushing but then is rejected) this is likely because of an outdated local git instance (this is not immediately evident, but sharing the credentials requires git to be fairly recent)
* Ensure the SSH key has been added to the Host Environment
	* (e.g `ssh-add -l`, ensure not "No identities available")

https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
## Configuring VSCode
VSCode extensions can be installed manually (as normal) from the host machine if working outside the dev container. If working inside the dev container, rebuilding the container will lose the extensions.
You can share make installed extensions persistent inside the dev container, or enable sharing the development environment with colleages, you can change the extensions in `/.devcontainer/devcontainer.json` inside `customizations - vscode - extensions` and add the identifier for the extension (found in 'more info', typically to the right hand side). Some optional extensions have been provided in the `devcontainer.json`.
# Useful Commands and Information
## Badges
One can add and configure badges with `anybadge`. More information can be found [here](https://github.com/jongracecox/anybadge)
## Template and GitLabs READMEs
The READMEs for gitlab and the microsoft template, from which this project is based, can be found in `./readme/`
# Authors
## Author
* Jack H. Culbert (jack.culbert@gesis.org)
## Maintainer
* Alex Mühlbauer (alexander.muehlbauer@gesis.org)
## Thanks
* Alex Mühlbauer for your excellent support and guidance
* Microsoft - Daniel Ciborowski
	* Template was adapted from https://github.com/microsoft/python-package-template
* Gitlab - Christian Clauss
	* Template was adapted from https://gitlab.com/gitlab-org/gitlab/-/blob/master/lib/gitlab/ci/templates/Python.gitlab-ci.yml
* Max Plank Institute
	* https://docs.mpcdf.mpg.de/doc/data/gitlab/devop-tutorial.html
* Sonarqube
	* https://docs.sonarsource.com/sonarqube/9.8/devops-platform-integration/gitlab-integration/
# Feedback and contribution
Feedback and contribution is welcomed. Please raise issues, thoughts or improvements on the gitlab repository [here](https://git.gesis.org/devops/project-templates/py-project-template/-/issues).
# Variables
## List of Template Variables and Locations
* ./
	* .devcontainer/
		* devcontainer.json
			* Line 44, pre-commit version, 3.3.2
		* Dockerfile
			* Node version (For Local Sonarlint), 18.x
			* Poetry version, 1.5.1
	* .vscode/
		* settings.json
			* Line length (rulers)
	* readme/
		* N/A
	* src/
		* Dockerfile
			* from python docker container version, latest
			* Poetry version, 1.5.1
			* Line 18: project name py_project_template
			* Line 22: Entrypoint "py_project_template/hello_world.py"
				* May be worth refactoring to a main.py pattern
		* py_project_template/
			* This folder name should be changed
			* \_\_init\_\_.py
				* package version
			* hello_world.py
				*
	* tests/
		* test_methods.py
			* from py_project_template.hello_world
	* .gitlab-ci.yml
		* variables:
			* VERSION - of Gitlab CI, Where is this parsed
			* PIP_CACHE_DIR, is this required`?
		* cache:
			* Is this required
		* Base:
			* image:
				* dc-python: DC_PY_VERSION
		* Typecheck:
			* image:
				* dc-npm: DC_NPM_VERSION
		* Sonarqube:
			* Inherit the sonarqube http via template, not token?
	* .pre-commit-config.yaml
		* revisions for all repos
	* .pypirc
		* Nexus if setup
		* pypirc optional credentials? How to setup?
		* Gitlab credentials inherited
	* docker-compose.yml
		* docker compose version
	* pyproject.toml
		* (This should be the authoritative version if possible)
		* Line 2: Poetry version
		* Line 6: Project name
		* Line 7: Project Version
		* Line 8: Authors
		* Line 12: maintainers
		* Line 14: Project Description
		* Line 16: include - project folder
		* Line 19: Minimum python version /
		* Lines 25-39: Versions for:
			* bandit
			* black
			* check-manifest
			* flake8
				* -bugbear
				* -docstrings
				* -formatter_junit_xml
				* -pyproject
			* pylint
			* pytest
				* -cov
				* -mock
				* -runner
			* shellcheck-py
			* coverage
		* Line 45: pyspark versioon
		* Line 54: Line length (black)
		* Line 62: Coverage fail under %
		* Line 65: Line length (flake8)
		* Line 66: Flake include warning types
		* Line 80: Flake ignor warnings
		* Line 98: Python Version
		* Line 99: Python Platform!!!
		* Line 106: TODO: incorporate --cov-fail-under Coverage fail under %
		* Line 186: Line length (pylint)
	* License - to be added
