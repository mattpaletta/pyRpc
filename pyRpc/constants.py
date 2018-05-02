import tempfile
import sys

TEMPDIR = tempfile.gettempdir()

PyVersion = 3 if (sys.version_info > (3, 0)) else 2