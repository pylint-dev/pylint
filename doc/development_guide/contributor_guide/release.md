# Releasing a pylint version

So, you want to release the `X.Y.Z` version of pylint ?

## Releasing a major or minor version

**Before releasing a major or minor version check if there are any unreleased commits on
the maintenance branch. If so, release a last patch release first. See
`Releasing a patch version`.**

- Write the `Summary -- Release highlights` in `doc/whatsnew` and upgrade the release
  date.
- Install the release dependencies: `pip3 install -r requirements_test.txt`
- Bump the version and release by using `tbump X.Y.0 --no-push --no-tag`. (For example:
  `tbump 2.4.0 --no-push --no-tag`)
- Check the commit created with `git show` amend the commit if required.
- Create a new `What's new in Pylint X.Y+1` document. Add it to `doc/index.rst`. Take a
  look at the examples from `doc/whatsnew`. Commit that with `git commit -am "wip"`.
- Move the `main` branch up to a dev version with `tbump`:

```bash
tbump X.Y+1.0-dev0 --no-tag --no-push  # You can interrupt after the first step
git commit -am "Upgrade the version to x.y+1.0-dev0 following x.y.0 release"
```

For example:

```bash
tbump 2.5.0-dev0 --no-tag --no-push
git commit -am "Upgrade the version to 2.5.0-dev0 following 2.4.0 release"
```

Check the commit, fixup the 'wip' commit with the what's new then push to a release
branch

- Open a merge request with the two commits (no one can push directly on `main`)
- After the merge, recover the merged commits on `main` and tag the first one (the
  version should be `X.Y.Z`) as `vX.Y.Z` (For example: `v2.4.0`)
- Push the tag.
- Release the version on GitHub with the same name as the tag and copy and paste the
  appropriate changelog in the description. This triggers the PyPI release.
- Create a `maintenance/X.Y.x` (For example: `maintenance/2.4.x` from the `v2.4.0` tag.)
- Upgrade the pattern for the protected branches in the settings under `Branches` /
  `Branch protection rules`. (For example: `maintenance/2.4*` instead of
  `maintenance/2.3*`.). There's a lot of configuration done in these settings, do NOT
  recreate it from scratch.
- Delete the `maintenance/X.Y-1.x` branch. (For example: `maintenance/2.3.x`)
- Select all the issues labelled `backport maintenance/X.Y-1.x` and label them
  `backported`, then rename the `backport maintenance/X.Y-1.x` label to
  `backport maintenance/X.Y.x` (for example rename `backport maintenance/2.3.x` to
  `backport maintenance/2.4.x`)
- Close the current milestone and create the new ones (For example: close `2.4.0`,
  create `2.4.1` and `2.6.0`)
- Hide and deactivate all the patch releases for the previous minor release on
  [readthedoc](https://readthedocs.org/projects/pylint/versions/), except the last one.
  (For example: hide `v2.4.0`, `v2.4.1`, `v2.4.2` and keep only `v2.4.3`)

## Back-porting a fix from `main` to the maintenance branch

Whenever a PR on `main` should be released in a patch release on the current maintenance
branch:

- Label the PR with `backport maintenance/X.Y-1.x`. (For example
  `backport maintenance/2.3.x`)
- Squash the PR before merging (alternatively rebase if there's a single commit)
- (If the automated cherry-pick has conflicts)
  - Add a `Needs backport` label and do it manually.
  - You might alternatively also:
    - Cherry-pick the changes that create the conflict if it's not a new feature before
      doing the original PR cherry-pick manually.
    - Decide to wait for the next minor to release the PR
    - In any case upgrade the milestones in the original PR and newly cherry-picked PR
      to match reality.
- Release a patch version

## Releasing a patch version

We release patch versions when a crash or a bug is fixed on the main branch and has been
cherry-picked on the maintenance branch.

- Install the release dependencies: `pip3 install -r requirements_test.txt`
- Bump the version and release by using `tbump X.Y-1.Z --no-push`. (For example:
  `tbump 2.3.5 --no-push`)
- Check the result visually with `git show`.
- Open a merge request of `release-X.Y-1.Z'` in `maintenance/X.Y.x` (For example:
  `release-2.3.5-branch` in `maintenance/2.3.x`) to run the CI tests for this branch.
- Create and push the tag.
- Release the version on GitHub with the same name as the tag and copy and paste the
  changelog from the ReadtheDoc generated documentation from the pull request pipeline
  in the description. This triggers the PyPI release.
- Merge the `maintenance/X.Y.x` branch on the main branch. The main branch should have
  the changelog for `X.Y-1.Z+1` (For example `v2.3.6`). This merge is required so
  `pre-commit autoupdate` works for pylint.
- Fix version conflicts properly, or bump the version to `X.Y.0-devZ` (For example:
  `2.4.0-dev6`) before pushing on the main branch
- Close the current milestone and create the new one (For example: close `2.3.5`, create
  `2.3.6`)

## Milestone handling

We move issues that were not done to the next milestone and block releases only if there
are any open issues labelled as `blocker`.
