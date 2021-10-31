# Starting Tutorial (Part 1)

```{eval-rst}
.. sidebar:: Tutorial Parts

    **Part 1: What we have**
      A tour of Evennia and how to use the tools, including an introduction to Python.
    Part 2: `What we want <../Part2/Starting-Part2.html>`_
      Planning our tutorial game and what to think about when planning your own in the future.
    Part 3: `How we get there <../Part3/Starting-Part3.html>`_
         Getting down to the meat of extending Evennia to make our game
    Part 4: `Using what we created <../Part4/Starting-Part4.html>`_
      Building a tech-demo and world content to go with our code
    Part 5: `Showing the world <../Part5/Starting-Part5.html>`_
      Taking our new game online and let players try it out

```

Welcome to Evennia! This multi-part Tutorial will help you get off the ground. It consists
of five parts, each with several lessons. You can pick what seems interesting, but if you
follow through to the end you will have created a little online game of your own to play
and share with others!

## Lessons of Part 1 - "What we have"

1. Introduction (you are here)
1. [Building stuff](./Building-Quickstart.md)
1. [The Tutorial World](./Tutorial-World-Introduction.md)
1. [Python basics](./Python-basic-introduction.md)
1. [Game dir overview](./Gamedir-Overview.md)
1. [Python classes and objects](./Python-classes-and-objects.md)
1. [Accessing the Evennia library](./Evennia-Library-Overview.md)
1. [Typeclasses and Persistent objects](./Learning-Typeclasses.md)
1. [Making first own Commands](./Adding-Commands.md)
1. [Parsing and replacing default Commands](./More-on-Commands.md)
1. [Creating things](./Creating-Things.md)
1. [Searching for things](./Searching-Things.md)
1. [Advanced searching with Django queries](./Django-queries.md)

In this first part we'll focus on what we get out of the box in Evennia - we'll get used to the tools,
and how to find things we are looking for. We will also dive into some of things you'll
need to know to fully utilize the system, including giving you a brief rundown of Python concepts. If you are
an experienced Python programmer, some sections may feel a bit basic, but you will at least not have seen
these concepts in the context of Evennia before.

## Things you will need

### A Command line

First of all, you need to know how to find your Terminal/Console in your OS. The Evennia server can be controlled
from in-game, but you _will_ need to use the command-line to get anywhere. Here are some starters:

- [Django-girls' Intro to the Command line for different OS:es](https://tutorial.djangogirls.org/en/intro_to_command_line/)

> Note that we only use forward-slashes `/` to show file system paths in this documentation. Windows users need
> to convert this to back-slashes `\` in their heads.

### A MUD client

You might already have a MUD-client you prefer. Check out the [grid of supported clients](../../../Setup/Client-Support-Grid.md) for aid.
If telnet's not your thing, you can also just use Evennia's web client in your browser.

> In this documentation we often use 'MUD' and 'MU' or 'MU*' interchangeably
  as labels to represent all the historically different forms of text-based multiplayer game-styles,
  like MUD, MUX, MUSH, MUCK, MOO and others. Evennia can be used to create all those game-styles
  and more.

### An Editor
You need a text-editor to edit Python source files. Most everything that can edit and output raw
text works (so not Word).

- [Here's a blog post summing up some of the alternatives](https://www.elegantthemes.com/blog/resources/best-code-editors) - these
things don't change much from year to year. Popular choices for Python are PyCharm, VSCode, Atom, Sublime Text and Notepad++.
 Evennia is to a very large degree coded in VIM, but that's not suitable for beginners.

> Hint: When setting up your editor, make sure that pressing TAB inserts _4 spaces_ rather than a Tab-character. Since
> Python is whitespace-aware, this will make your life a lot easier.


### Set up a game dir for the tutorial

Next you should make sure you have [installed Evennia](../../../Setup/Setup-Quickstart.md). If you followed the instructions
you will already have created a game-dir. You could use that for this tutorial or you may want to do the
tutorial in its own, isolated game dir; it's up to you.

- If you want a new gamedir for the tutorial game and already have Evennia running with another gamedir,
first enter that gamedir and run

        evennia stop

> If you want to run two parallel servers, that'd be fine too, but one would have to use
> different ports from the defaults, or there'd be a clash. We will go into changing settings later.
-  Now go to where you want to create your tutorial-game. We will always refer to it as `mygame` so
  it may be convenient if you do too:

        evennia --init mygame
        cd mygame
        evennia migrate
        evennia start --log

    Add your superuser name and password at the prompt (email is optional). Make sure you can
    go to `localhost:4000` in your MUD client or to [http://localhost:4001](http://localhost:4001)
    in your web browser (Mac users: Try `127.0.0.1` instead of `localhost` if you have trouble).

    The above `--log` flag will have Evennia output all its logs to the terminal. This will block
    the terminal from other input. To leave the log-view, press `Ctrl-C` (`Cmd-C` on Mac). To see
    the log again just run

        evennia --log

  You should now be good to go!


```{toctree}
:hidden:

Building-Quickstart
Tutorial-World-Introduction
Python-basic-introduction
Gamedir-Overview
Python-classes-and-objects
Evennia-Library-Overview
Learning-Typeclasses
Adding-Commands
More-on-Commands
Creating-Things
Searching-Things
Django-queries
../Part2/Starting-Part2

```
