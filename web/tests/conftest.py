# '''module with fixtures for pytest/celery'''
# import pytest
#
#
# @pytest.fixture(scope='session')
# def celery_enable_logging():
#     return True
#
# @pytest.fixture(scope='session')
# def celery_config():
#     '''celery config fixture'''
#     return {
#         'result_backend': 'rpc',
#         'broker_backend': 'memory'
#     }
