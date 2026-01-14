from locust import HttpUser, task, between
from qa_framework.core.config import settings

class BasePerformanceTest(HttpUser):
    """
    Base class for Locust performance tests.
    """
    abstract = True
    wait_time = between(1, 5)
    host = settings.BASE_URL

    # Can add common hooks here
