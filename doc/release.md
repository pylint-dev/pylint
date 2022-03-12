# Releasing a pylint version

So, you want to release the `X.Y.Z` version of pylint ?

## Process

1. Check if the dependencies of the package are correct, make sure that astroid is
   pinned to the latest version.
2. Install the release dependencies `pip3 install pre-commit tbump tox`
3. Bump the version by using `tbump X.Y.Z --no-tag --no-push`
4. Check the result (Do `git diff vX.Y.Z-1 ChangeLog doc/whatsnew/` in particular).
5. Move back to a dev version for pylint with `tbump`:

```bash
tbump X.Y.Z+1-dev0 --no-tag --no-push # You can interrupt after the first step
git commit -am "Move back to a dev version following X.Y.Z release"
```

4. Check the result
5. Open a merge request with the two commits (no one can push directly on `main`)
6. After the merge recover the merged commits and tag the first one (the version should
   be `X.Y.Z`) as `vX.Y.Z`
7. Push the tag
8. Go to GitHub, click on "Releases" then on the `vX.Y.Z` tag, choose edit tag, and copy
   past the changelog in the description. This will trigger the release to pypi.

## Post release

### Merge tags in main for pre-commit

If the tag you just made is not part of the main branch, merge the tag `vX.Y.Z` in the
main branch by doing a history only merge. It's done in order to signal that this is an
official release tag, and for `pre-commit autoupdate` to works.

```bash
git checkout main
git merge --no-edit --strategy=ours vX.Y.Z
git push
```

### Milestone handling

We move issue that were not done in the next milestone and block release only if it's an
issue labelled as blocker.

- Close milestone `X.Y.Z`
- Create the milestones for `X.Y.Z+1`, (or `X.Y+1.0`, and `X+1.0.0` if applicable)

#### What's new

If it's a minor release, create a new `What's new in Pylint X.Y+1` document. Add it to
`doc/index.rst`. Take a look at the examples from `doc/whatsnew`.
