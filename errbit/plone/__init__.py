from errbit.plone.loghandler import ErrbitLoggingHandler
import logging


logging.root.addHandler(ErrbitLoggingHandler())
