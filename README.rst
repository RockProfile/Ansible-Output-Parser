Ansible Parser
==============

The Ansible Parser is intended to parse the output that Ansible returns.

Istallation
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

