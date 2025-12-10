### Benefits

1. **Seamless Integration**: Code-generated content can now participate fully in MyST builds without special handling.

2. **Better Cross-Referencing**: Generated figures, equations, and sections can be referenced from anywhere in the document.

3. **Flexible Generation**: Users can generate MyST content programmatically using any Jupyter kernel without kernel-specific libraries.

4. **Consistent Behavior**: Output parsing follows the same rules and capabilities as the rest of the document.

## Examples

### Markdown Output with References

With this change, a code cell can generate Markdown output that defines and references labels:

```python
# Generate MyST content with a figure reference
markdown_output = """
Here is a reference to [](#fig:my-figure).

:::{figure} images/plot.png
:name: fig:my-figure

My generated plot.
:::
"""

from IPython.display import display
display({
  "text/markdown": markdown_output,
}, raw=True)
```

The Markdown output can now be parsed and integrated into the document's reference resolution system.

### Multiple Outputs with Individual ASTs

A code cell that produces multiple outputs, each with its own parsed content:

```python
print("First output stream")
display({"text/markdown": "**Second** output"}, raw=True)
display({"text/latex": "$$E = mc^2$$"}, raw=True)
```

Each of these outputs will be represented as a separate `Output` node with its own AST subtree.
