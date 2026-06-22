# What is this thing?

This is a tiny project put together over the course of a sleepless night that partially implements a leaf venation algorithm described in "Modelling and visualization of leaf venation patterns" by Runions et al. Refer to the provided reference. This implementation is not to be taken as a faithful and complete reproduction of the algorithm as described by Runions et al, it is just a fun project.

# What is leaf venation?

Leaves on trees (the biological kind, not the computational one), as they develop, grow various kinds of vein patterns based on biological signals and rules. This algorithm replicates this process for a given leaf shape, and generates veins that are (hopefully) biologically realistic-looking. Please take this explanation with a grain of salt, as I am not an expert in biology or botany, and this is the limit of my knowledge on the subject. Refer to the provided article for an in-depth view of what the goal is.

# How do I run this?

The dependencies are very light, mostly just `numpy` and `matplotlib` (yes, the leaf veins are plotted in matplotlib). To install dependencies, I recommend you start with a virtual environment, however, this is optional:

`python -m venv <env_name>`

Activate you virtual environment by running the appropriate script for your platform in `<env_name>/Scripts` (again, don't do this if you are not in an env)

Make sure you are in the root of the repository. Install the dependencies with `python -m pip install -r requirements.txt`

Run `python main.py` to see a leaf venation pattern

# Reference

Adam Runions, Martin Fuhrer, Brendan Lane, Pavol Federl, Anne−Gaëlle Rolland−Lagan, and Przemyslaw Prusinkiewicz. Modeling and visualization of leaf venation patterns. ACM Transactions on Graphics 24(3), pp. 702−711.