from Products.Five.browser import BrowserView


class ErrbitTestingException(Exception):
    """An exception for testing the errbit connection.
    """


class MakeError(BrowserView):

    def __call__(self):
        raise ErrbitTestingException('Testing the errbit connection.')
