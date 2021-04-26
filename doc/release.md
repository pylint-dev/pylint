# Releasing a pylint version

So, you want to release the `X.Y.Z` version of pylint ?

## Process

1. Run the acceptance tests to see if everything is alright with this release. We don't
   run them on CI: `pytest -m acceptance`
2. Check if the dependencies of the package are correct
3. Put the release date into `Changelog` (and `What's new` if it's a major).
4. Generate the new copyright notices for this release:

```bash
pip3 install copyrite
copyrite --contribution-threshold 1 --change-threshold 3 --backend-type \
git --aliases=.copyrite_aliases . --jobs=8
# During the commit pre-commit and pyupgrade will remove the encode utf8
# automatically
```

5. Submit your changes in a merge request.

6. Make sure the tests are passing on Travis/GithubActions:
   https://travis-ci.org/PyCQA/pylint/

7. Do the actual release by tagging the master with `vX.Y.Z` (ie `v1.6.12` or `v2.5.3a1`
   for example). Travis should deal with the release process once the tag is pushed with
   `git push origin --tags`

8. Go to github, click on "Releases" then on the `vX.Y.Z` tag, choose edit tag, and copy
   past the changelog in the description.

## Manual Release

Following the previous steps, for a manual release run the following commands:

```bash
git clean -fdx && find . -name '*.pyc' -delete
python setup.py sdist --formats=gztar bdist_wheel
twine upload dist/*
# don't forget to tag it as well
```

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

### Files to update after releases

#### Changelog

- Create a new section, with the name of the release `X.Y.Z+1` or `X.Y+1.0` on the
  master branch.

You need to add the estimated date when it is going to be published. If no date can be
known at that time, we should use `Undefined`.

#### Whatsnew

If it's a major release, create a new `What's new in Pylint X.Y+1` document Take a look
at the examples from `doc/whatsnew`.
