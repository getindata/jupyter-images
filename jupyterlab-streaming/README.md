# Base Jupyter Notebook Stack for Streaming

This is a copy of [base-notebook](https://github.com/jupyter/docker-stacks/tree/main/base-notebook) jupyter image.

For Apache Flink (v 1.15) needs - Python 3.8 must be installed inside Jupyter notebook container, additionally, due to number of existing vulnerabilities in official (old) [docker image](https://hub.docker.com/layers/jupyter/base-notebook/python-3.8.8/images/sha256-d832504205f10b2267543335eb5bc8b1079fb916a712687a698962bed873c17d?context=explore), custom base-notebook image has to be maintained and published.

Changes to between upstream and current version:

* Python 3.8
* Ubuntu 20.04 as base image
