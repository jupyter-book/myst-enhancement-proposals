# MEP process overview

Below is an overview of the MEP process.
Each section below is a step that should be followed in order.

## Step 1: Open an issue in `myst-enhancement-proposals`

This should describe the enhancement you'd like to make.
The goal of the issue is to help others understand your idea and get informal alignment around it, and to decide if it is well-suited for the MEP process.
_MEPs should ideally have at least two, and ideally 3-4 co-authors from different organizations._

## Step 2: Make a proposal via a PR to `myst-enhancement-proposals`

Use a markdown template to structure your proposal. The `status` should initially be set to `Draft`. Here's a proposed template:

```
---
mep:
  id: <NNNN - Add when this MEP becomes Active>
  created: <yyyy-mm-dd - date MEP is active>
  authors:
    - <authors' real names, optional github handle>
  status: <Draft | Active | Accepted | Not Accepted>
  discussion: <URL of canonical location for discussion>
---
# <title here>

## Context

<!-- provide context needed to understand this proposal. Describe the problem with MyST's current syntax or behavior. -->

## Proposal

<!-- describe your proposed change to syntax in concrete terms. Include a layperson's description of this change if relevant. -->

## Examples

<!-- provide examples of what this change would look like in the real world (e.g., raw MyST and rendered output). -->

## UX implications & migration

<!-- describe how this would improve the UX or functionality of MyST markdown. Describe any deprecations or syntax migration steps that would be needed. -->

## Questions or objections

<!-- as conversation takes place, list anything that is needed to be resolved and provide links to the conversation where this happened. -->

## References

<!-- reference other examples you're using for inspiration or to help others learn and understand the proposal. -->
```
## Step 3: Discuss and iterate

Invite discussion from others in the community. Incorporate new ideas as individuals (particularly core team members) raise objections or make suggestions.
% TODO: Define guidelines for considerations to take during discussion, such as implementation feasibility.
% TODO: Define policy around what happens if an implementation _cannot_ implement something that has already been merge into the spec.
% one suggestion here: https://github.com/executablebooks/meta/pull/843#issuecomment-1274555428

## Step 4: Activate decision making

Once the proposal has stabilized and the author wishes to move forward, do the following:

- In the MEP frontmatter, set the status as `Active` and add an incremental MEP number (e.g. `id: 0002`). The MEP should no-longer change substantially.
- **The Core Team** should review the MEP and approve if they wish to accept it.
  - To approve, click `Approve` the GitHub Pull Request UI.
  - To request blocking changes, then click `Request Changes` in the GitHub UI. (see [](#appendix:blocking))
- A MEP may be accepted when all of the following conditions are met:
  - More than five (5) weekdays have passed since the proposal was marked as `Active`.
  - At least two `PR Approvals` from **core team members**.
  - No `Request Changes` from a core team member.
- If there are **unresolved objections** (via `Request Changes` to the PR)
  - The MEP author may restart the voting process after incorporating feedback to resolve the objection, **or** ask the Steering Council to follow the same {external:ref}`decision-making process used for team policy <governance:policy-decision>`.
- If there are no unresolved objections, the MEP is **accepted**:
  - Update its status metadata to `Accepted` and merge the PR.
  - Once a PR is merged, it closes the issue and a decision has been made.
  - Finally, follow [](process:implement).

(process:implement)=
## Step 5: Update `myst-spec`

When a MEP has been accepted, open a Pull Request to apply the necessary changes to https://github.com/executablebooks/myst-spec.
Merging this PR implements the MEP, and makes it a formal part of the spec.
Parsers may now implement this change as well. This MEP process is now finished.

```{admonition} Update the MyST documentation as well
While not formally part of the MyST spec, the MyST guide at [myst-tools.org](https://myst-tools.org) should also be updated as quickly as possible, so that users can more easily learn about the most up-to-date MyST specification.
```

## Appendix: When should I open a MEP?

The goal of Enhancement Proposals are to align the team on major strategic decisions about MyST Markdown, and to formally record a decision.
Consider whether the importance or complexity of the topic is worth the extra overhead of the MEP process.
Ultimately, the most important thing is that we follow principles of open and inclusive discussion, iteration and collaborative writing, and making decisions explicit.

As a guide, below are examples of topics that warrant a MEP:

- Changing or extending the syntax or major functionality of MyST.
- Defining high-level strategy and vision for the language
- Amending the MEP process itself

(appendix:blocking)=
## Appendix: When to ask for changes

When blocking any change or objecting to a proposal, provide a rationale for what must be changed and why you believe it is critically important. _Do not disapprove because of differences in opinion. Only disapprove if you have a major strategic concern_. See [Strategies for integrating objections](https://www.sociocracyforall.org/strategies-for-integrating-objections/) for what we are aiming for.