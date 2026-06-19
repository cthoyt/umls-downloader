<!--
<p align="center">
  <img src="https://github.com/cthoyt/umls-downloader/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  UMLS Downloader
</h1>

<p align="center">
    <a href="https://github.com/cthoyt/umls-downloader/actions/workflows/tests.yml">
        <img alt="Tests" src="https://github.com/cthoyt/umls-downloader/actions/workflows/tests.yml/badge.svg" /></a>
    <a href="https://pypi.org/project/umls-downloader">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/umls-downloader" /></a>
    <a href="https://pypi.org/project/umls-downloader">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/umls-downloader" /></a>
    <a href="https://github.com/cthoyt/umls-downloader/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/umls-downloader" /></a>
    <a href='https://umls_downloader.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/umls_downloader/badge/?version=latest' alt='Documentation Status' /></a>
    <a href="https://codecov.io/gh/cthoyt/umls-downloader/branch/main">
        <img src="https://codecov.io/gh/cthoyt/umls-downloader/branch/main/graph/badge.svg" alt="Codecov status" /></a>  
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-snekpack-blue" /></a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
    <a href="https://github.com/cthoyt/umls-downloader/blob/main/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Contributor Covenant"/></a>
    <!-- uncomment if you archive on zenodo
    <a href="https://doi.org/10.5281/zenodo.XXXXXX">
        <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg" alt="DOI"></a>
    -->
</p>

Don't worry about [UMLS Terminology Services (UTS)](https://uts.nlm.nih.gov/uts/)
licensing and distribution rules - just use
`umls_downloader` to write code that knows how to download content and use it
automatically from the following (non-exhaustive) list of resources:

- [UMLS](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)
- [RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html)
- [SemMedDB](https://lhncbc.nlm.nih.gov/ii/tools/SemRep_SemMedDB_SKR/SemMedDB_download.html)
- [SNOMED-CT](https://www.nlm.nih.gov/healthit/snomedct/international.html)
- potentially more in the future

or any content that can be downloaded through
the [UTS ticket granting](https://documentation.uts.nlm.nih.gov/automating-downloads.html)
system. There's no centralized list of content available through the UTS so
suggestions for additional resources are welcome through
the [issue tracker](https://github.com/cthoyt/umls_downloader/issues).

Full documentation are available at [umls-downloader.readthedocs.io](https://umls-downloader.readthedocs.io).

## 💪 Getting Started

### Download A Specific Version of UMLS

```python
import os
from umls_downloader import download_umls

# Get this from https://uts.nlm.nih.gov/uts/edit-profile
api_key = ...

path = download_umls(version="2021AB", api_key=api_key)

# This is where it gets downloaded: ~/.data/bio/umls/2021AB/umls-2021AB-mrconso.zip
expected_path = os.path.join(
    os.path.expanduser("~"), ".data", "umls", "2021AB",
    "umls-2021AB-mrconso.zip",
)
assert expected_path == path.as_posix()
```

After it's been downloaded once, it's smart and doesn't need to download again.
It gets stored using [`pystow`](https://github.com/cthoyt/pystow) automatically
in the `~/.data/bio/umls` directory.

A full list of functions is available in the
[documentation](https://umls-downloader.readthedocs.io).

### Automating Configuration of UTS Credentials

There are two ways to automatically set the username and password so you don't
have to worry about getting it and passing it around in your python code:

1. Set `UMLS_API_KEY` in the environment
2. Create `~/.config/umls.ini` and set in the `[umls]` section a `api_key` key.

```python
from umls_downloader import download_umls

# Same path as before
path = download_umls(version="2021AB")
```

### Download the Latest Version

First, you'll have to
install [`bioversions`](https://github.com/cthoyt/bioversions)
with `pip install bioversions`, whose job it is to look up the latest version of
many databases. Then, you can modify the previous code slightly by omitting
the `version` keyword argument:

```python
from umls_downloader import download_umls

# Same path as before (as of November 21st, 2021)
path = download_umls()
```

### Download and open the file

The UMLS file is zipped, so it's usually accompanied by the following
boilerplate code:

```python
import zipfile
from umls_downloader import download_umls

path = download_umls()
with zipfile.ZipFile(path) as zip_file:
    with zip_file.open("MRCONSO.RRF", mode="r") as file:
        for line in file:
            ...
```

This exact code is wrapped with the `open_umls()` using Python's context manager
so it can more simply be written as:

```python
from umls_downloader import open_umls

with open_umls() as file:
    for line in file:
        ...
```

The `version` and `api_key` arguments also apply here.

### Command Line Interface

The `umls-downloader` command line tool is automatically installed. It can be
used from the console with the `--help` flag to show all subcommands:

```console
$ umls-downloader --help
```

> TODO show the most useful thing the CLI does! The CLI will have documentation
> auto-generated by `sphinx`.

## Why not an API?

The UMLS provides an [API](https://documentation.uts.nlm.nih.gov/rest/home.html)
for access to tiny bits of data at a time. There are even two recent (last 5
years) packages [`umls-api`](https://pypi.org/project/umls-api)
[`connect-umls`](https://pypi.org/project/connect-umls) that provide a wrapper
around them. However, API access is generally rate limited, difficult to use in
bulk, and slow. For working with UMLS (or any other database, for that matter)in
bulk, it's necessary to download full database dumps.


## 🚀 Installation

The most recent release can be installed from
[PyPI](https://pypi.org/project/umls-downloader/) with uv:

```console
$ uv pip install umls-downloader
```

or with pip:

```console
$ python3 -m pip install umls-downloader
```

The most recent code and data can be installed directly from GitHub with uv:

```console
$ uv pip install git+https://github.com/cthoyt/umls-downloader.git
```

or with pip:

```console
$ python3 -m pip install git+https://github.com/cthoyt/umls-downloader.git
```

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are
appreciated. See
[CONTRIBUTING.md](https://github.com/cthoyt/umls-downloader/blob/main/.github/CONTRIBUTING.md)
for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

- [Biopragmatics Lab](https://biopragmatics.github.io)

-->

<!--
### 💰 Funding

This project has been supported by the following grants:

| Funding Body  | Program                                                      | Grant Number |
|---------------|--------------------------------------------------------------|--------------|
| Funder        | [Grant Name (GRANT-ACRONYM)](https://example.com/grant-link) | ABCXYZ       |
-->

### 🍪 Cookiecutter

This package was created with
[@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using
[@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack)
template.

## 🛠️ For Developers

<details>
  <summary>See developer instructions</summary>

The final section of the README is for if you want to get involved by making a
code contribution.

### Development Installation

To install in development mode, use the following:

```console
$ git clone git+https://github.com/cthoyt/umls-downloader.git
$ cd umls-downloader
$ uv pip install -e .
```

Alternatively, install using pip:

```console
$ python3 -m pip install -e .
```

### Pre-commit

You can optionally use [pre-commit](https://pre-commit.com) to automate running
key code quality checks on each commit. Enable it with:

```console
$ uvx pre-commit install
```

Or using `pip`:

```console
$ pip install pre-commit
$ pre-commit install
```

### 🥼 Testing

After cloning the repository and installing `tox` with
`uv tool install tox --with tox-uv` or `python3 -m pip install tox tox-uv`, the
unit tests in the `tests/` folder can be run reproducibly with:

```console
$ tox -e py
```

Additionally, these tests are automatically re-run with each commit in a
[GitHub Action](https://github.com/cthoyt/umls-downloader/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```console
$ git clone git+https://github.com/cthoyt/umls-downloader.git
$ cd umls-downloader
$ tox -e docs
$ open docs/build/html/index.html
```

The documentation automatically installs the package as well as the `docs` extra
specified in the [`pyproject.toml`](pyproject.toml). `sphinx` plugins like
`texext` can be added there. Additionally, they need to be added to the
`extensions` list in [`docs/source/conf.py`](docs/source/conf.py).

The documentation can be deployed to [ReadTheDocs](https://readthedocs.io) using
[this guide](https://docs.readthedocs.io/en/stable/intro/import-guide.html). The
[`.readthedocs.yml`](.readthedocs.yml) YAML file contains all the configuration
you'll need. You can also set up continuous integration on GitHub to check not
only that Sphinx can build the documentation in an isolated environment (i.e.,
with `tox -e docs-test`) but also that
[ReadTheDocs can build it too](https://docs.readthedocs.io/en/stable/pull-requests.html).

</details>

## 🧑‍💻 For Maintainers

<details>
  <summary>See maintainer instructions</summary>

### Initial Configuration

#### Configuring ReadTheDocs

[ReadTheDocs](https://readthedocs.org) is an external documentation hosting
service that integrates with GitHub's CI/CD. Do the following for each
repository:

1. Log in to ReadTheDocs with your GitHub account to install the integration at
   https://readthedocs.org/accounts/login/?next=/dashboard/
2. Import your project by navigating to https://readthedocs.org/dashboard/import
   then clicking the plus icon next to your repository
3. You can rename the repository on the next screen using a more stylized name
   (i.e., with spaces and capital letters)
4. Click next, and you're good to go!

#### Configuring Archival on Zenodo

[Zenodo](https://zenodo.org) is a long-term archival system that assigns a DOI
to each release of your package. Do the following for each repository:

1. Log in to Zenodo via GitHub with this link:
   https://zenodo.org/oauth/login/github/?next=%2F. This brings you to a page
   that lists all of your organizations and asks you to approve installing the
   Zenodo app on GitHub. Click "grant" next to any organizations you want to
   enable the integration for, then click the big green "approve" button. This
   step only needs to be done once.
2. Navigate to https://zenodo.org/account/settings/github/, which lists all of
   your GitHub repositories (both in your username and any organizations you
   enabled). Click the on/off toggle for any relevant repositories. When you
   make a new repository, you'll have to come back to this

After these steps, you're ready to go! After you make "release" on GitHub (steps
for this are below), you can navigate to
https://zenodo.org/account/settings/github/repository/cthoyt/umls-downloader to
see the DOI for the release and link to the Zenodo record for it.

#### Registering with the Python Package Index (PyPI)

The [Python Package Index (PyPI)](https://pypi.org) hosts packages so they can
be easily installed with `pip`, `uv`, and equivalent tools.

1. Register for an account [here](https://pypi.org/account/register)
2. Navigate to https://pypi.org/manage/account and make sure you have verified
   your email address. A verification email might not have been sent by default,
   so you might have to click the "options" dropdown next to your address to get
   to the "re-send verification email" button
3. 2-Factor authentication is required for PyPI since the end of 2023 (see this
   [blog post from PyPI](https://blog.pypi.org/posts/2023-05-25-securing-pypi-with-2fa/)).
   This means you have to first issue account recovery codes, then set up
   2-factor authentication
4. Issue an API token from https://pypi.org/manage/account/token

This only needs to be done once per developer.

#### Configuring your machine's connection to PyPI

This needs to be done once per machine.

```console
$ uv tool install keyring
$ keyring set https://upload.pypi.org/legacy/ __token__
$ keyring set https://test.pypi.org/legacy/ __token__
```

Note that this deprecates previous workflows using `.pypirc`.

### 📦 Making a Release

#### Uploading to PyPI

After installing the package in development mode and installing `tox` with
`uv tool install tox --with tox-uv` or `python3 -m pip install tox tox-uv`, run
the following from the console:

```console
$ tox -e finish
```

This script does the following:

1. Uses [bump-my-version](https://github.com/callowayproject/bump-my-version) to
   switch the version number in the `pyproject.toml`,
   `src/umls_downloader/version.py`, and
   [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using
   [`uv build`](https://docs.astral.sh/uv/guides/publish/#building-your-package)
3. Uploads to PyPI using
   [`uv publish`](https://docs.astral.sh/uv/guides/publish/#publishing-your-package).
4. Push to GitHub. You'll need to make a release going with the commit where the
   version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump
   the version by minor, you can use `tox -e bumpversion -- minor` after.

#### Releasing on GitHub

1. Navigate to https://github.com/cthoyt/umls-downloader/releases/new to draft a
   new release
2. Click the "Choose a Tag" dropdown and select the tag corresponding to the
   release you just made
3. Click the "Generate Release Notes" button to get a quick outline of recent
   changes. Modify the title and description as you see fit
4. Click the big green "Publish Release" button

This will trigger Zenodo to assign a DOI to your release as well.

### Updating Package Boilerplate

This project uses `cruft` to keep boilerplate (i.e., configuration, contribution
guidelines, documentation configuration) up-to-date with the upstream
cookiecutter package. Install cruft with either `uv tool install cruft` or
`python3 -m pip install cruft` then run:

```console
$ cruft update
```

More info on Cruft's update command is available
[here](https://github.com/cruft/cruft?tab=readme-ov-file#updating-a-project).

</details>
