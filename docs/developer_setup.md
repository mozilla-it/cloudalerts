# Developer Setup
Technologies used: pipenv, pre-commit, ...

## Pipenv Setup

Install all regular env dependencies of the Pipfile in the current directory:
* `pipenv install`

Opens shell with corresponding dependencies to the pipfile(.lock) in the directory that you make the call.
* `pipenv shell`


### Install Pre-commit

Using Pipenv (pre-commit is located in the [Pipfile](./Pipfile))
```
pipenv shell
pre-commit install
```

You should get the following response after installing pre-commit:

>`pre-commit installed at .git/hooks/pre-commit`

### Pre-commit, Run on the Entire Codebase

Run the following command where you installed pre-commit.
* `pre-commit run --all-files`

### Exiting Pipenv Shell

Run the following command to exit `pipenv shell` while in a shell.
* `exit`

The command `deactivate` will not work to full disengage the pipenv shell as it does with `venv`.

## Required Environment Variables
These environmental variables must be set.
* GOOGLE_APPLICATION_CREDENTIALS
* GCP_PROJECT
