# Releasing a pylint version

So, you want to release the `X.Y.Z` version of pylint ?

## Process

1. Check if the dependencies of the package are correct, make sure that astroid is
   pinned to the latest version.
2. Install the release dependencies `pip3 install pre-commit tbump`
3. Bump the version and release by using `tbump X.Y.Z --no-push`.
4. Check the result.
5. Push the tag.
6. Go to GitHub, click on "Releases" then on the `vX.Y.Z` tag, choose edit tag, and copy
   past the changelog in the description. This will trigger the release to pypi.

## Post release

### Merge tags in master for pre-commit

If the tag you just made is not part of the main branch, merge the tag `vX.Y.Z` in the
main branch by doing a history only merge. It's done in order to signal that this is an
official release tag, and for `pre-commit autoupdate` to works.

```bash
git checkout master
git merge --no-edit --strategy=ours vX.Y.Z
git push
```

### Milestone handling

We move issue that were not done in the next milestone and block release only if it's an
issue labelled as blocker.

### Back to a dev version

1. Unpin the version of astroid, so it's possible to install a dev version during
   development
2. Move back to a dev version for pylint with `tbump`:

```bash
tbump X.Y.Z-dev0 --no-tag --no-push # You can interrupt during copyrite
```

Check the result and then upgrade the master branch

#### Whatsnew

If it's a minor release, create a new `What's new in Pylint X.Y+1` document. Take a look
at the examples from `doc/whatsnew`.
