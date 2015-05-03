from . import ( magic, base64, tuple, simple, )
from ._delimit import ( slash, backslash, )

import datetime
def archive(transformer = tuple,
            date_format = '%Y-%m-%d',
            position = 'left',
            now = datetime.datetime.now):
    '''
    Wrap a transformer to add a date component to a path.

    :param transformer: Transformer to be wrapped
    :type transformer: transformer
    :param str date_format: This gets passed to
        :py:meth:`datetime.datetime.strftime`, and the result of this gets
        added to the file's path. Use :samp:`'%Y-%m-%d'`, for example,
        if you want to get new data once per day, or :samp:`'%Y-%m-%d %H:00'`
        if you want it every hour.
    :param str position: Should the date be added to the beginning
        of the path (:samp:`'left'`) or the end of the path
        (:samp:`'right'`). If (:samp:`'left'`), the new path will be
        :samp:`(date,) + old_path`; if right, the new path will be
        :samp:`old_path + (date,)`.
    :param function now: :py:func:`archive` will run this to determine
        the date that will be added to the path; you might change
        this for testing.
    '''

#@cache(transformer = vlermv.transformers.archive(vlermv.transformers.tuple)
