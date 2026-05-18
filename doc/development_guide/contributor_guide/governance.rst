============
 Governance
============

How to become part of the project ?
-----------------------------------

How to become a contributor ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Follow the code of conduct
- Search by yourself before asking for help
- Open an issue
- Investigate an issue and report your finding
- Open a merge request directly if you feel it's a consensual change

Reporting a bug is being a contributor already.

How to become a triager ?
^^^^^^^^^^^^^^^^^^^^^^^^^

- Create a pylint plugin, then migrate it to the 'pylint-dev' github organization.

Or:

- Contribute for more than 3 releases consistently.
- Do not be too opinionated, follow the code of conduct without requiring emotional
  works from the maintainers. It does not mean that disagreements are impossible,
  only that arguments should stay technical and reasonable so the conversation
  is civil and productive.
- Have a maintainer suggest that you become triager, without you asking
- Get unanimous approval or neutral agreement from current maintainers.

How to become a maintainer ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


- Take ownership of a part of the code that is not maintained well at the moment
  or that you contributed personally (if we feel we can't merge something without
  your review, you're going to be able to merge those yourself soon).

Or:

- Contribute two big code merge requests over multiple releases (for example
  one checker in 2.13 and the following bug after release and one complicated
  bug fixes in 2.14). Otherwise contributing for more than 3 releases consistently
  with great technical and interpersonal skills.
- Triage for multiple months (close duplicate, clean up issues, answer questions...)
- Have an admin suggest that you become maintainer, without you asking
- Get unanimous approval or neutral agreement from current maintainers.


How to become an admin ?
^^^^^^^^^^^^^^^^^^^^^^^^

- Contribute for several hundreds of commits over a long period of time
  with excellent interpersonal skills and code quality.
- Maintain pylint for multiple years (code review, triaging and maintenance tasks).
- At this point probably have another admin leave the project or
  become inactive for years.
- Have an admin suggest that you become an admin, without you asking.
- Get unanimous approval or neutral agreement from current admins.


How are decisions made ?
------------------------

Everyone is expected to follow the code of conduct. pylint is a do-ocracy / democracy.
You're not allowed to behave poorly because you contributed a lot. But if
you're not going to do the future maintenance work, your valid opinions might not be
taken into account by those that will be affected by it.

What are the fundamental tenets of pylint development?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

General:

- We favor correctness over performance, because pylint is not used primarily
  for its performance. Performance is still important and needs to be taken into
  account from the get go.

- We then favor false negatives over false positives if correctness is
  impossible to achieve.

- We try to keep the configuration sane, but if there's a hard decision to take we
  add an option so that pylint is multiple sizes fit all (after configuration)

Where to add a new checker or message:

- Error messages (things that will result in an error if run) should be builtin
  checks, activated by default

- Messages that are opinionated, even slightly, should be opt-in (added as :ref:`an extension<plugins>`)

- We don't shy away from opinionated checks (like the while checker), but there's such a
  thing as too opinionated, if something is too opinionated it should be an external
  :ref:`pylint plugin<plugins>`.

How are disagreements handled ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When something is not consensual users, maintainers, and admins discuss until an
agreement is reached.

Depending on the difficulty of the discussion and the importance of a fast resolution,
a decision can be taken:

- Unanimously between discussion participants, contributors and maintainers (preferably)

- By asking discussion participants for their opinions with an emoji survey in the
  issue and then using the majority if no maintainers feel strongly about the issue.

- By majority of admins if no admins feel strongly about the issue.

- By asking all users for their opinions in a new issue that will be pinned for
  multiple months before taking the decision if two admins feel strongly on an
  opposite side of the issue. Once the result is obvious the majority decision
  is not up for discussion anymore.
