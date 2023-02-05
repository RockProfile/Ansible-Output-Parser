Ansible Parser
==============

The Ansible Parser is intended to parse the output that Ansible returns.

Installation
------------

Simply install using:

.. code-block:: sh

    pip install ansible-output-parser

Usage
-----

.. code-block:: python

    from ansible_parser.play import Play
    play = "" # populate with play output
    ansible = Play(play_output=play)
    failures = ansible.failures()

Alternatively the following can be executed to read from a log file:

.. code-block:: python

    from ansible_parser.logs import Logs
    log_file = "" # path to log file
    log_plays = Logs(log_file=log_file)

Reading from a log file will result in multiple plays as it may process plays with the same
name.
