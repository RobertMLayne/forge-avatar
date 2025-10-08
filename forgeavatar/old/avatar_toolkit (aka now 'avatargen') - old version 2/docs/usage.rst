.. docs/usage.rst

Usage Guide
===========

Command-Line Interface (CLI)
----------------------------
To run the tool from the command line:

.. code-block:: bash

   avatargen --url "https://example.com/image.jpg" --output out.png --bezel 4 --drop-shadow --retina-scale 2

GUI Interface
-------------
To launch the graphical interface:

.. code-block:: bash

   python -m avatargen.gui

You can select an image, preview the output in real time, and export the final image with optional settings.

Batch Processing
----------------
To process an entire folder:

.. code-block:: bash

   python -m avatargen.batch --input-dir ./images --output-dir ./out --config config.json

Drag-and-Drop
-------------
The GUI supports drag-and-drop for quick image loading.

Face Detection
--------------
By default, if OpenCV is installed, the tool attempts to crop to the face region before processing. This can be disabled with `--no-face-detect`.

Customization
-------------
Most parameters can be tuned:

- ``--bezel``: Width of the circular or rounded bezel
- ``--corner-radius``: Controls roundness of rectangles
- ``--drop-shadow``: Enables soft shadows
- ``--retina-scale``: Outputs Retina versions (e.g., @2x)
- ``--format``: Choose from PNG, JPEG, WEBP, etc.

For advanced use, modify the default settings in `config.py`.
