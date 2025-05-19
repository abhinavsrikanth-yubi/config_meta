import sys
import traceback
from io import StringIO
from contextlib import redirect_stderr


def retrieve_exception(exception):
    stderr_out = StringIO()
    with redirect_stderr(stderr_out):
        traceback.print_exception(exception)
    return stderr_out.getvalue()