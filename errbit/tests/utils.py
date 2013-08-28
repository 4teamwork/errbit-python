class NothingRaised(object):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            raise AssertionError(
                'Expected no exception, but got: %s, %s' % (
                    exc_type.__name__, exc_value))
