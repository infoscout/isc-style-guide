# InfoScout Style Guide

WIP

## Python Style

InfoScout primarily follows the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html), but has a few exceptions and additions.

### Exceptions

##### The maximum line length is 120 characters.

**Rationale**: Github displays code in a window with 120 columns. Setting a line length limit of 120 characters allows engineers to review code on Github without requiring horizontal scrolling.

### Additions

##### All tuples and multiline iterables should end in a trailing comma. Inline iterables (except for tuples) should never end in a trailing comma.

**Rationale**: A tuple with a single item *must* end with a trailing comma. Therefore, by ending all tuples with a trailing comma, it makes it easier for engineers to add and remove elements to a tuple, without worrying about the number of items in a tuple.

There is no benefit to adding trailing commas to other inline iterables (ie. lists, dicts, and sets), and we specifically do not add trailing commas in these cases because this violates other linting checks (also, it looks ugly).

See [Nik Graf's blog post](https://medium.com/@nikgraf/why-you-should-enforce-dangling-commas-for-multiline-statements-d034c98e36f8) on trailing commas for a strong argument in favour of trailing commas in multiline iterables. The blog post is written for JavaScript, but the same arguments apply to Python.
