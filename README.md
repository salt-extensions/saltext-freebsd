# Salt Extension for FreeBSD

Salt Extension for FreeBSD-specific commands

## Security

If you discover a security vulnerability, please refer to
[Salt's security guide][security].

## User Documentation

For setup and usage instructions, please refer to the
[User Documentation][docs].

## Contributing

The saltext-freebsd project welcomes contributions from anyone!

The [Salt Extensions guide][salt-extensions-guide] provides
comprehensive instructions on all aspects of Salt extension
development, including [writing tests][writing-tests],
[running tests][running-tests], [writing documentation][writing-docs]
and [rendering the docs][rendering-docs].

### Quickstart

To get started contributing, first clone this repository (or your
fork):

```bash
# Clone the repo
git clone --origin upstream git@github.com:salt-extensions/saltext-freebsd.git

# Change to the repo dir
cd saltext-freebsd
```

#### Automatic

If you have installed [direnv], copying the included `.envrc.example`
to `.envrc` and allowing it to run ensures a proper development
environment is present and the virtual environment is active.

Without `direnv`, you can still run the automation explicitly:

> [!NOTE]
>
> By default, `make dev` installs the latest Salt release from PyPI,
> which requires compiling those of its dependencies that don't
> provide pre-built wheels for FreeBSD.
>
> To avoid this, set the environment variable
> `VENV_SYSTEM_SITE_PACKAGES` to `1` **before** running `make dev` (or
> any `nox` session, including those invoked by the pre-commit hooks).
> This disables `uv` and creates a venv that falls back to the system
> Python's packages, so you can run against OS-packaged Salt (if
> installed). Even without OS-packaged Salt, system packages that
> satisfy Salt's requirements are reused instead of being compiled.
> For the latter route, consider installing:
>
> - `py312-sqlite3`
> - `py312-maturin`
> - `py312-markupsafe`
>
> If some pre-commit hooks fail to run, you can skip them by setting
> the `SKIP` environment variable to a comma-separated list of hook
> IDs/aliases.

```bash
sudo pkg install uv py312-uv  # only when running without VENV_SYSTEM_SITE_PACKAGES
make dev  # or python3 tools/initialize.py
source .venv/bin/activate
```

#### Manual

Please follow the [first steps][first-steps], skipping the repository
initialization and first commit.

### Pull request

Always make changes in a feature branch:

```bash
git switch -c my-feature-branch
```

Please ensure you include a
[news fragment](https://salt-extensions.github.io/salt-extension-copier/topics/documenting/changelog.html#procedure)
describing your changes. This is a requirement for all user-facing
changes (bug fixes, new features), with the exception of documentation
changes.

To [submit a Pull Request][submitting-pr], you'll need a fork of this
repository in your own GitHub account. If you followed the
instructions above, set your fork as the `origin` remote now:

```bash
git remote add origin git@github.com:<your_fork>.git
```

Ensure you followed the [first steps][first-steps] and commit your
changes, fixing any failing `pre-commit` hooks. Then push the feature
branch to your fork and submit a PR.

### Ways to contribute

Contributions come in many forms, and they’re all valuable! Here are
some ways you can help without writing code:

- **Documentation**: Especially examples showing how to use this
  project to solve specific problems.
- **Triaging issues**: Help manage [issues] and participate in
  [discussions].
- **Reviewing [Pull Requests][prs]**: We especially appreciate reviews
  using [Conventional Comments][comments].

You can also contribute by:

- Writing blog posts
- Sharing your experiences using Salt + FreeBSD on social media
- Giving talks at conferences
- Publishing videos
- Engaging in IRC, Discord or email groups

Any of these things are super valuable to our community, and we
sincerely appreciate every contribution!

[comments]: https://conventionalcomments.org/
[direnv]: https://direnv.net
[discussions]: https://github.com/salt-extensions/saltext-freebsd/discussions
[docs]: https://salt-extensions.github.io/saltext-freebsd/
[first-steps]: https://salt-extensions.github.io/salt-extension-copier/topics/creation.html#initialize-the-python-virtual-environment
[issues]: https://github.com/salt-extensions/saltext-freebsd/issues
[prs]: https://github.com/salt-extensions/saltext-freebsd/pulls
[rendering-docs]: https://salt-extensions.github.io/salt-extension-copier/topics/documenting/building.html
[running-tests]: https://salt-extensions.github.io/salt-extension-copier/topics/testing/running.html
[salt-extensions-guide]: https://salt-extensions.github.io/salt-extension-copier/
[security]: https://github.com/saltstack/salt/blob/master/SECURITY.md
[submitting-pr]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork
[writing-docs]: https://salt-extensions.github.io/salt-extension-copier/topics/documenting/writing.html
[writing-tests]: https://salt-extensions.github.io/salt-extension-copier/topics/testing/writing.html
