.. _upgrading_pylint:

Upgrading pylint
================

You should probably set the version of pylint in your development environment in order to
choose when you actually upgrade pylint's warnings. pylint is following semver versioning.
But we can't guarantee that the output between version will stays the same. What this means
is that:

.. include:: ../../development_guide/contributor_guide/patch_release.rst

You can expect less messages if you set the minor and upgrade to a new patch version.
But still, if you enable ``useless-suppression`` it still means you can get a new
``useless-suppression`` when a false positive that you disabled is now fixed. Also,
if a library you're using was upgraded and is understood better or worse than the
previous one, you could get new messages too.

.. include:: ../../development_guide/contributor_guide/minor_release.rst

You can expect a lot more change in output, the main one being new checks.

.. include:: ../../development_guide/contributor_guide/major_release.rst

You could have to change the command you're launching or the plugin and
editor integration you're using.
