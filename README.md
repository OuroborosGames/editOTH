editOTH
=======
editOTH is an editor for data files used by **On The Hill**, a WIP
strategy game by Ouroboros Games. The core of the project is
[JSON Editor](https://github.com/jdorn/json-editor/) by Jeremy Dorn,
our work is mostly about generating an appropriate schema with the help
of [JSL](https://pypi.python.org/pypi/jsl).

Usage
=====
To use editOTH, open editor.html in your browser and start writing
content. When you're done, copy and paste the resulting JSON to an
appropriate file. Sorry about shitty documentation, one day I might
write a better one.

If you want to create your own schema or just 'compile' editor.html for
some reason, you'll need jsl. It can be installed with pip:
```
    pip install jsl
```