from decorator import decorator
import logging

LOG = logging.getLogger('errbit')


@decorator
def logging_exceptions(func, *args, **kwargs):
    """This decorator can be used in code trying to report an exception with errbit.
    It re-loggs exceptions happened during rendering an errbit exception.
    """
    try:
        return func(*args, **kwargs)
    except Exception, exc:
        exc._errbit_do_not_report = True
        LOG.exception('exception while trying to report other exception:')
        raise
