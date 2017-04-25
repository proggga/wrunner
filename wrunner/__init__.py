'''import file for project wrunner'''
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from wrunner.celery import CELERY_APP as CELERY_APP

__all__ = ['CELERY_APP']
