(governance:meps)=
# MyST Enhancement Proposals

A formal process for changing [the MyST Markdown Specification](https://myst-tools.org/docs/spec) and an archive of present and past proposals.

Because the MyST specification has many interior and exterior stakeholders, we use a more formal and structured process around changing the specification[^gov].
These are called **MyST Enhancement Proposals (MEPs)**.

[^gov]: See [our Team Compass](https://compass.executablebooks.org) for other governance and decision-making processes in the Executable Books community.

This process is encoded in https://github.com/executablebooks/myst-enhancement-proposals and in this documentation.
The sections below describe the process, and the [MEP index](meps/index) is where you can find all of our MEPs.

```{toctree}
:maxdepth: 1
overview
strategy
```

% Hidden because we'll include the table in the index page so this avoids confusion

```{toctree}
:hidden:
meps/index
```

```{admonition} Work in progress!
This process is relatively new.
Bear with us, and please provide feedback if you think the process can be improved!
```

## MyST Specification

The MyST specification is at [`spec.myst-tools.org`](https://spec.myst-tools.org) (repository: https://github.com/executablebooks/myst-spec).
It is the source of truth for MyST Markdown syntax.

When a MEP is accepted, it is generally implemented by modifying the specification and the documentation around it.
MyST parsers may then choose to implement these changes on their own.

```{toctree}
:hidden:
MyST specification <https://spec.myst-tools.org>
```

## List of MEPs

Below is a list of all past and current MEPs, you can also find this table at [](meps/index).

```{include} _build/dirhtml/meps.txt
```