---
category: breaking
---
`API::moduleImport` no longer has any results for dotted names, such as `API::moduleImport("foo.bar")`. Using `API::moduleImport("foo.bar").getMember("baz").getACall()` previously worked if the Python code was `from foo.bar import baz; baz()`, but not if the code was `import foo.bar; foo.bar.baz()` -- we are making this change to ensure the approach that can handle all cases is always used.
