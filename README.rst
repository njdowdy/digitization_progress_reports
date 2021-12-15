=================
DIGITIZATION PROGRESS REPORTS
=================

A resource for generating digitization effort graphs (or other efforts) on-the-fly.

More generally, for a series of entities (e.g., "Collections") and a series of activities
(e.g., "High Resolution Images"), this project takes a count of:

#. Total proposed units of activity
#. Total completed units of activity

combined with:

#. Project Start
#. Present
#. Project End
#. Project Extension End

and generates a figure like this:

.. image:: digitization_progress_reports/output/example.png
  :width: 500
  :alt: A digitization effort plot

As a starting point, try the data template file `here <https://github.com/njdowdy/digitization-progress-reports/digitization_progress_reports/input/input_template.csv>`_.

HOW TO USE
^^^^^^^^^^

#. Install "``poetry``" (see: `here <https://python-poetry.org/docs/#installation>`_) on your system
#. Run from the directory of your choice:
    - ``git clone https://github.com/njdowdy/digitization-progress-reports.git``
    - ``cd digitization-progress-reports``
    - ``poetry install``
    - ``source`poetry env info --path`/bin/activate``
#. Add your files to process into ``digitization_progress_reports/input/``
#. Adjust ``script.py`` to reflect the path to your file and adjust other options as needed
#. Run:
    - ``python script.py``
#. Once finished, run:
    - ``deactivate``

To update the source code:
    #. ``git update origin``

CONTACT
^^^^^^^^^^
Please report issues or questions `here <https://github.com/njdowdy/digitization-progress-reports/issues>`_.