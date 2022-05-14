from abc import ABC, abstractmethod
import re


class BaseValidator(ABC):
    """raises NotImplemented if validate is not provided"""

    @abstractmethod
    def validate(self, password) -> bool:
        raise not NotImplemented


class RegexValidator(
    BaseValidator,
):
    """validates password with provided regex"""

    def __init__(self, regex: str, error: Exception):
        super(BaseValidator, self).__init__()

        self.regex = regex
        self.error = error

    def validate(self, password):
        if not re.findall(self.regex, password):
            raise self.error


class ValidatorChain:
    """validates passwords with provided validators"""

    def __init__(self, validators: list[BaseValidator]):
        self.validators = validators

    def check(self, password):
        for validator in self.validators:
            validator.validate(password)
