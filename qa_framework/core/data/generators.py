from faker import Faker

class DataGenerator:
    """
    Wrapper around Faker to generate test data.
    """
    def __init__(self, locale: str = "en_US"):
        self._faker = Faker(locale)

    @property
    def faker(self) -> Faker:
        return self._faker

    def get_email(self) -> str:
        return self._faker.email()

    def get_name(self) -> str:
        return self._faker.name()

    def get_address(self) -> str:
        return self._faker.address()
    
    # Can extend with custom providers if needed
