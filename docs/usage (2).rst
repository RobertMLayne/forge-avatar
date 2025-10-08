.. docs/usage.rst
##############################################################################
Usage Guide
##############################################################################

Quick-start
===========

.. code-block:: bash

   # Full remaster, GPU auto-detect
   avatargen -i my_lowres.jpg -o avatar.png \
             --sr-scale 4 --quality 100 --format PNG

   # Fast CPU-only pass, skip colour & face clean-ups
   avatargen -i selfie.jpg -o avatar.webp \
             --sr-backend opencv --no-face-restore --no-color-fix \
             --quality 90

--------------------------------------------------------------------
Command-line reference
--------------------------------------------------------------------

.. code-block:: text

   avatargen [-h] [--gui] --input FILE --output FILE
             [--format PNG|JPEG|WEBP]
             [--sr-scale N] [--sr-backend auto|realesrgan|opencv]
             [--no-face-restore] [--no-color-fix]
             [--bezel PX] [--corner-radius PX] [--no-shadow]
             [--quality N] [--lossless]

Quality flags
^^^^^^^^^^^^^

====================  =======================================================
Flag                  Purpose
--------------------  -------------------------------------------------------
``--sr-scale``        Super-resolution factor (1 = off, 2/4 recommended)
``--sr-backend``      *auto* (prefer Real-ESRGAN), *realesrgan*, or *opencv*
``--no-face-restore`` Skip GFPGAN clean-up
``--no-color-fix``    Skip auto white-balance + CLAHE
``--quality``         JPEG / WebP quality (1-100, default 95)
``--lossless``        WebP lossless encoding
====================  =======================================================

GUI walkthrough
^^^^^^^^^^^^^^^

* ``python -m forgeavatar.gui``  
  Drag one or many images; enable **Quality boost** for the full pipeline.
* Status bar logs the chosen SR back-end (CUDA vs CPU fallback).
* Click **Save…** to export PNG / JPEG / WebP.

--------------------------------------------------------------------
Batch mode
--------------------------------------------------------------------

Use the helper script in *scripts/batch_convert.py* or call the
``AvatarGenerator`` class:

.. code-block:: python

   from pathlib import Path
   from forgeavatar.core import AvatarGenerator

   gen = AvatarGenerator({"sr_scale": 4})
   in_dir = Path("input")
   out_dir = Path("output")

   for img_path in in_dir.glob("*.jpg"):
       out = out_dir / f"{img_path.stem}_avatar.png"
       gen.generate(img_path.open("rb"), output=out)
