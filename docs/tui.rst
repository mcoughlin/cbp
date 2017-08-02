TUI
===

The TUI(Text User Interface) is a UI written in asciimatics, a cross platform terminal manipulation library similar to
the curses library found on different platforms. One of the positives of this implementation is that it can be run over
a regular ssh connection without having to deal with running an x-server to generate an x-window. This should make it
more portable and easier to maintain should any of the equipment need to be changed.

Limitations
-----------

As it stands, the operator can either use the TUI or the command line but not both at the same time. This is because
there can only be one connection at a time for the instruments' port. Another limitation is that instrument status can
only be checked at the initialization of the program, this means that instruments are not hot-swappable at least from
the TUI's perspective.

Suggestions
-----------

Take the TUI interface slowly as you can potentially overshoot the options that you were looking for and end up places
that you did not want to be.