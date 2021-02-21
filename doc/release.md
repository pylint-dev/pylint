# Releasing a pylint version

So, you want to release the ``X.Y.Z`` version of pylint ?

## Process

1. Preparation
   0. Run the acceptance tests to see if everything is alright with this release.
      We don't run them on CI: ``pytest -m acceptance``
   1. Check if the dependencies of the package are correct
   2. Update ``numversion`` in ``__pkginfo__``, ``dev_version`` should also be None when you tag.
   3. Put the version numbers, and the release date into the changelog
   4. Put the release date into the ``What's new`` section.
   5. Generate the new copyright notices for this release:

```bash
pip3 install copyrite
copyrite --contribution-threshold 1 --change-threshold 3 --backend-type
  git --aliases=.copyrite_aliases . --jobs=8
# During the commit pre-commit and pyupgrade will remove the encode utf8
# automatically
```

   6. Submit your changes in a merge request.

2. Make sure the tests are passing on Travis/GithubActions:
   https://travis-ci.org/PyCQA/pylint/

3. Do the actual release by tagging the master with ``pylint-X.Y.Z`` (ie  ``pylint-1.6.12``
   for example). Travis should deal with the release process once the tag is pushed
   with `git push origin --tags`

## Manual Release

Following the previous steps, for a manual release run the following commands:

```bash
git clean -fdx && find . -name '*.pyc' -delete
python setup.py sdist --formats=gztar bdist_wheel
twine upload dist/*
# don't forget to tag it as well
```

## Post release

### New branch to create for major releases

The master branch will have all the new features for the ``X.Y+1`` version

If you're doing a major release, you need to create the ``X.Y`` branch
where we will cherry-pick bugs to release the ``X.Y.Z+1`` minor versions

### Milestone handling

We move issue that were not done in the next milestone and block release only
if it's an issue labelled as blocker.

### Files to update after releases

#### Changelog
Create a new section, with the name of the release ``X.Y.Z+1`` (or ``X.Y+1.0`` for
major release) and the estimated date when it is going to be published. If
no date can be known at that time, we should use ``Undefined``.

#### Whatsnew

Only for major release, create a new ``What's new in Pylint X.Y+1`` document
Take a look at the examples from ``doc/whatsnew``.

### Versions

Update ``numversion`` to ``X.Y+1.0`` in ``__pkginfo__`` for ``master`` and to ``X.Y.Z+1`` for the ``X.Y`` branch.
``dev_version`` should also be back to an integer after the tag.
