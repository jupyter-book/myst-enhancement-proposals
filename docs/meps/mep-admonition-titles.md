---
title: Simplify Named Admonition Syntax
mep:
  id: <NNNN - Add when this MEP becomes Active>
  created: <yyyy-mm-dd - date MEP is active>
  authors:
    - Rowan Cockett @rowanc1
    - Matt McKay @mmcky
  status: Draft
  discussion: https://github.com/executablebooks/myst-enhancement-proposals/pull/12
---

# Simplify Named Admonition Syntax

We propose a simplified syntax to allow arguments for all named admonitions. The syntax allows an argument for any title of a named admonition like `{tip}` or `{note}`, to allow users to easily set the color and icon of an admonition while also having a custom title. The proposed syntax is:

````markdown
```{note} Custom Note Title
Body of the styled admonition.
```
````

## Context

The original RST directives for named admonitions [attention](https://docutils.sourceforge.io/docs/ref/doctree.html#attention), [caution](https://docutils.sourceforge.io/docs/ref/doctree.html#caution), [danger](https://docutils.sourceforge.io/docs/ref/doctree.html#danger), [error](https://docutils.sourceforge.io/docs/ref/doctree.html#error), [hint](https://docutils.sourceforge.io/docs/ref/doctree.html#hint), [important](https://docutils.sourceforge.io/docs/ref/doctree.html#important), [note](https://docutils.sourceforge.io/docs/ref/doctree.html#note), [tip](https://docutils.sourceforge.io/docs/ref/doctree.html#tip), and [warning](https://docutils.sourceforge.io/docs/ref/doctree.html#warning) are designed for a single line, and allow you have the entire named admonition in a compact form.

> Any text immediately following the directive indicator (on the same line and/or indented on following lines) is interpreted as a directive block and is parsed for normal body elements.
>
> - See [docutils](https://docutils.sourceforge.io/docs/ref/rst/directives.html#specific-admonitions)

For example, the `{note}` directive argument will be treated as body text:

```rst
.. note:: This is the body of the admonition
   Which continues here.
```

There is a [general admonition](https://docutils.sourceforge.io/docs/ref/rst/directives.html#generic-admonition) directive that _does_ support the inclusion of custom titles, but lacks the unifying kind & style information.

This syntax has been adopted directly in MyST, and has been demonstrated to confuse our users[^refs] who expect to be able to easily edit the admonition title without changing the directive kind.

[^refs]: See references below with multiple issues and discussions of people asking for help on how to edit admonition titles.

Currently the only way to edit the title of an admonition, while still picking up on a specific style, color and icon is to use the base `{admonition}` directive and specify a class attribute.

````markdown
```{admonition} Custom Title
:class: note
Body of the admonition
```
````

![](https://i.imgur.com/Bj6ZjDV.png)

## Proposal

We propose a simplified way to create styled admonitions with titles, where the argument is always the title of the admonition.

````markdown
```{note} Custom Title
Body of the admonition
```
````

![](https://i.imgur.com/Bj6ZjDV.png)

This syntax presents a clear mapping of text content to parts of the rendered admonition: (1) the icon, style & semantics (i.e. `{note}`); (2) the title as an argument; and (3) the body of the admonition in the fence. It also has the advantage of not requiring the user to know the word `admonition`, which is not commonly used outside of Sphinx and Docutils[^naming].

[^naming]: These elements are generally called "callouts", for example, in [obsidian](https://nicolevanderhoeven.com/blog/20220330-new-in-obsidian-obsidian-callouts/), [quarto](https://quarto.org/docs/authoring/callouts.html), [readme](https://docs.readme.com/rdmd/docs/callouts), and many other documentation packages.

The argument would be optional, with a fallback to the default title (e.g. "Note" in this case).

````
```{note}
Body of the admonition
```
````

![](https://i.imgur.com/I81tNEx.png)

## Examples

The current behavior around admonitions with classes should continue to be supported, so the following examples are the suggested way to _document_ admonitions with titles rather than the only way that they can be written.

Before:

````markdown
```{admonition} Custom Title
:class: note
Body of the admonition
```
````

After:

````markdown
```{note} Custom Title
Body of the admonition
```
````

## UX implications & migration

The user experience is enhanced as the new syntax provides a direct one-to-one mapping between the markup text and the rendered outcome.

This MEP also reduces the complexity of the overall MyST syntax as it moves named admonitions towards a more general usage of arguments, with less conditional logic in parsing.

````
```{directive} arguments
Body content for directive to act on.
```
````

### Deprecations

This will deviate from the `sphinx/docutils` specification that defines reStructuredText which uses any supplied elements to the directive as body text.

If this MEP is approved the following syntax:

````
```{note} A custom title
and some body text
```
````

would **no longer** render as:

![](https://i.imgur.com/woeVUs8.png)

but instead would render as:

![](https://i.imgur.com/iiwNH5M.png)

We propose an automated code modification that can be run on existing projects to target this upgrade, for example:

```bash
myst-mep upgrade 0002 "docs/*"
```

This codemod will target named admonitions in markdown and Jupyter Notebooks to insert a new line and preserve the intended behavior.

## Questions or objections

Deviation from RST & Docutils
: MyST has thus far mostly been a one-to-one mapping of RST --> Markdown. As we introduce new features like cross-references, we should look to improve the user-experience of the syntax based on feedback from where it is confusing or difficult to teach. In Python, we can make these changes and transform the docutils AST before it is passed on to Sphinx, this is already the case with several nodes (e.g. nested headers).

Single Line Terseness
: The single line for a note is desirable and is possible in RST, but currently requires two lines in MyST to open and close the fence. The current MEP would require this to be on _three_ lines. We encourage a future MEP to look at "Leaf Directives" that can be specified on a single line, such as single-line named admonitions or iframes (e.g. see [#57](https://github.com/executablebooks/myst-spec/issues/57)).

## References

- MyST users ask questions in issues and webinars around the ability to add a title to a named admonition. This is not currently possible, and requires users to change the directive they are using. See [#49](https://github.com/executablebooks/myst-spec/issues/49).
