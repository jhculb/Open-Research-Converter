# Python Project Template
## Important
* Poetry has replaced Flit and tox

## Introduction
This project is a template for creating Python projects that follows the Python Standards declared in PEP 621. It uses a pyproject.yaml file to configure the project and Poetry to simplify the build process and publish to PyPI. Poetry simplifies the build and packaging process for Python projects by eliminating the need for separate setup.py and setup.cfg files. With poetry, you can manage all relevant configurations within the pyproject.toml file, streamlining development and promoting maintainability by centralizing project metadata, dependencies, and build specifications in one place. You can also compare and share current versioning through the generated poetry.lock file.

## Project Organization

- `.devcontainer/Dockerfile`: Contains Dockerfile to build a development container for VSCode with all the necessary extensions for Python development installed.
- `.devcontainer/devcontainer.json`: Contains the configuration for the development container for VSCode, including the Docker image to use, any additional VSCode extensions to install, and whether or not to mount the project directory into the container.
- `.vscode/settings.json`: Contains VSCode settings specific to the project, such as the Python interpreter to use and the maximum line length for auto-formatting.
- `src`: Place new source code here.
- `tests`: Contains Python-based test cases to validate source code.
- `pyproject.toml`: Contains metadata about the project and configurations for additional tools used to format, lint, type-check, and analyze Python code.

### `pyproject.toml`

The pyproject.toml file is a centralized configuration file for modern Python projects. It streamlines the development process by managing project metadata, dependencies, and development tool configurations in a single, structured file. This approach ensures consistency and maintainability, simplifying project setup and enabling developers to focus on writing quality code. Key components include project metadata, required and optional dependencies, development tool configurations (e.g., linters, formatters, and test runners), and build system specifications.

In this particular pyproject.toml file, the [build-system] section specifies that the Flit package should be used to build the project. The [project] section provides metadata about the project, such as the name, description, authors, and classifiers. The [project.optional-dependencies] section lists optional dependencies, like pyspark, while the [project.urls] section supplies URLs for project documentation, source code, and issue tracking.

The file also contains various configuration sections for different tools, including bandit, black, coverage, flake8, pyright, pytest, tox, and pylint. These sections specify settings for each tool, such as the maximum line length for flake8 and the minimum code coverage percentage for coverage.

#### Tool Sections

##### black

Black is a Python code formatter that automatically reformats Python code to conform to the PEP 8 style guide. It is used to maintain a consistent code style throughout the project.

The pyproject.toml file specifies the maximum line length and whether or not to use a "fast" mode for formatting. Black also allows for a pyproject.toml configuration file to be included in the project directory to customize its behavior.

##### coverage

Coverage is a tool for measuring code coverage during testing. It generates a report of which lines of code were executed during testing and which were not.

The pyproject.toml file specifies that branch coverage should be measured and that the tests should fail if the coverage falls below 100%. Coverage can be integrated with a variety of test frameworks, including pytest.

##### pytest

Pytest is a versatile testing framework for Python projects that simplifies test case creation and execution. It supports both pytest-style and unittest-style tests, offering flexibility in testing approaches. Key features include fixture support for clean test environments, parameterized tests to reduce code duplication, and extensibility through plugins for customization. Adopt pytest to streamline testing and tailor the framework to your project's specific needs.

The pyproject.toml file plays an essential role in configuring pytest for your project. It includes various test markers, such as integration, notebooks, gpu, spark, slow, and unit, which are used during testing. It also specifies options for generating test coverage reports, setting the Python path, and outputting test results in the xunit2 format. You can easily modify the pyproject.toml file to customize pytest for your project's specific needs.

##### pylint
Pylint is a versatile Python linter and static analysis tool that identifies errors and style issues in your code. It generates an in-depth report, presenting errors, warnings, and conventions found in the codebase. Pylint configurations are centralized in the pyproject.toml file, covering extension management, warning suppression, output formatting, and code style settings such as maximum function arguments and class attributes. The unique scoring system provided by Pylint helps developers assess and maintain code quality, ensuring a focus on readability and maintainability throughout the project's development.

##### pyright
Pyright is a static type checker for Python that uses type annotations to analyze your code and catch type-related errors. It is capable of analyzing Python code that uses type annotations as well as code that uses docstrings to specify types.

The pyproject.toml file contains configurations for Pyright, such as the directories to include or exclude from analysis, the virtual environment to use, and various settings for reporting missing imports and type stubs. By using Pyright, you can catch errors related to type mismatches before they even occur, which can save you time and improve the quality of your code.

##### flake8
Flake8 is a code linter for Python that checks your code for style and syntax issues. It checks your code for PEP 8 style guide violations, syntax errors, and more.

The pyproject.toml file contains configurations for Flake8, such as the maximum line length, which errors to ignore, and which style guide to follow. By using Flake8, you can ensure that your code follows the recommended style guide and catch syntax errors before they cause problems.

##### poetry
In this template, we use Poetry to manage package versions, dependency conflict, and publishing our package. Configured through the pyproject.toml file, Poetry is set up with global and group dependencies: global, dev and spark, other groups can be added at will. Each group in the .toml is a collection of packages and minimum and maximum versions, if required for packages not to conflict, these groups can be optional.

The [build-system] section in the pyproject.toml file contains the poetry version and backend requirements, the [tool.poetry] section contains the minimum configuration details about the project, including the project name, version, authors, description, readme and packages. These can be complimented with [further details](https://python-poetry.org/docs/pyproject/) to further specify package details. The [tool.poetry.dependencies] section contains the dependencies for the package itself: to add to the dependencies of the project run `poetry install <package-name>`, to then install this locally run `poetry install`.

The [tool.poetry.group.dev] section contains configuration options for the `dev` group, and the [tool.poetry.group.dev.dependencies] section contains the list of development dependencies. These are used in the development container, gitlab and locally. To add to this group run `poetry add <package-name> --group dev` then run `poetry install --only dev` to install the development dependencies. This applies also to the spark group and other groups you may wish to define, and can be run through changing `--only dev` to `--only <other-group>`.

Poetry manages the exact versions installed through the poetry.lock file. This file should not be manually edited, and can be passed to other developers or included in the repository to ensure identical distributions.

Poetry helps us efficiently manage packages and prevent dependency errors, automates building and maintains the reliability and functionality in our Python package across a wide range of environments and versions. By identifying potential compatibility issues  early in the development process, we improve the quality and usability of our package. Our Poetry configuration streamlines the development workflow, promoting code quality and consistency throughout the project.

### Development
#### Devcontainer
Dev Containers in Visual Studio Code allows you to use a Docker container as a complete development environment, opening any folder or repository inside a container and taking advantage of all of VS Code's features. A devcontainer.json file in your project describes how VS Code should access or create a development container with a well-defined tool and runtime stack. You can use an image as a starting point for your devcontainer.json. An image is like a mini-disk drive with various tools and an operating system pre-installed. You can pull images from a container registry, which is a collection of repositories that store images.

Creating a dev container in VS Code involves creating a devcontainer.json file that specifies how VS Code should start the container and what actions to take after it connects. You can customize the dev container by using a Dockerfile to install new software or make other changes that persist across sessions. Additional dev container configuration is also possible, including installing additional tools, automatically installing extensions, forwarding or publishing additional ports, setting runtime arguments, reusing or extending your existing Docker Compose setup, and adding more advanced container configuration.

After any changes are made, you must build your dev container to ensure changes take effect. Once your dev container is functional, you can connect to and start developing within it. If the predefined container configuration does not meet your needs, you can also attach to an already running container instead. If you want to install additional software in your dev container, you can use the integrated terminal in VS Code and execute any command against the OS inside the container.

When editing the contents of the .devcontainer folder, you'll need to rebuild for changes to take effect. You can use the Dev Containers: Rebuild Container command for your container to update. However, if you rebuild the container, you will have to reinstall anything you've installed manually. To avoid this problem, you can use the postCreateCommand property in devcontainer.json. There is also a postStartCommand that executes every time the container starts.

You can also use a Dockerfile to automate dev container creation. In your Dockerfile, use FROM to designate the image, and the RUN instruction to install any software. You can use && to string together multiple commands. If you don't want to create a devcontainer.json by hand, you can select the Dev Containers: Add Dev Container Configuration Files... command from the Command Palette (F1) to add the needed files to your project as a starting point, which you can further customize for your needs.

#### Setup
This project includes three files in the .devcontainer and .vscode directories that enable you to use Docker and VSCode locally to set up an environment that includes all the necessary extensions and tools for Python development.

The Dockerfile specifies the base image and dependencies needed for the development container. The Dockerfile installs the necessary dependencies for the development container, including Python 3 and flit, a tool used to build and publish Python packages. It sets an environment variable to indicate that flit should be installed globally. It then copies the pyproject.toml file into the container and creates an empty README.md file. It creates a directory src/py_project_template and installs only the development dependencies using flit. Finally, it removes unnecessary files, including the pyproject.toml, README.md, and src directory.

The devcontainer.json file is a configuration file that defines the development container's settings, including the Docker image to use, any additional VSCode extensions to install, and whether or not to mount the project directory into the container. It uses the python-3-miniconda container as its base, which is provided by Microsoft, and also includes customizations for VSCode, such as recommended extensions for Python development and specific settings for those extensions. In addition to the above, the settings.json file also contains a handy command that can automatically install pre-commit hooks. These hooks can help ensure the quality of the code before it's committed to the repository, improving the overall codebase and making collaboration easier.

The settings.json file is where we can customize various project-specific settings within VSCode. These settings can include auto-formatting options, auto-trimming of trailing whitespace, Git auto-fetching, and much more. By modifying this file, you can tailor the VSCode environment to your specific preferences and workflow. It also contains specific settings for Python, such as the default interpreter to use, the formatting provider, and whether to enable unittest or pytest. Additionally, it includes arguments for various tools such as Pylint, Black, Flake8, and Isort, which are specified in the pyproject.toml file.

## Getting Started
To check: this is the case with
To get started with this template, simply 'Use This Template' to create a new repository and start building your project within the `src` directory. One mayrun the unit tests using the VS Code Test extension.
