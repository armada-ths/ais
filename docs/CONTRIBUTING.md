# Contributing to AIS

## Code of Conduct

By participating in this project, you agree to uphold the (Code of Conduct)[ais/.github/CODE_OF_CONDUCT.md]

## Pull Request (PR) Workflow

0. Read the [pull request merge checklist](#pull-request-merge-checklist) and
   plan your work around it.
1. Find an issue to work on and assign yourself to it. If an issue does not
   exist for what you want to work on, create the issue first.
2. Push your (unfinished) work early so others can see it. You need to create a
   branch in the following style: `<name>/<type>/<description>`, where `<name>` is your own surname, `<type>` is one of: `feat` for feature, `hot` for (hot)fix, `doc` for
   documentation, `chore` for chores, or `refactor` for refactor. E.g. `adam/f/add-fair-button-in-profile` for a PR that adds
   a fair button in the profile page.
3. Right away, open a PR on GitHub based on that branch. Assign yourself to the
   PR, and add a "draft" label to the PR if you don't think it's ready to be
   merged. Insert [the below checklist](#pull-request-merge-checklist) as the
   first comment on your PR. The title and description of the PR will be used
   for the final merge commit title and body, respectively. These can edited
   while developing your PR. [Link your pull
   request](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
   to the issue(s) that it will resolve.
4. If you think the PR is ready to be merged and have handled all checklist
   items, remove the "draft" label (if present) and ask for a review. The PR
   reviewer(s) should double check that all checklist items are taken care of
   before merging the PR. Failing to follow the checklist could lead to not
   meeting our project requirements.

## Pull Request Merge Checklist

- [ ] Feature/fix PRs should add one atomic (as small as possible) feature or fix.
- [ ] All code in your PR needs to have been formatted.
- [ ] The merge commit title should be prefixed with the type of the PR and a colon and a space, that is "feat", "fix", "doc", "chore", or "refactor", followed by a ": ".
- [ ] The merge commit body should reference at least one issue.
- [ ] The code compiles and all the tests pass.
