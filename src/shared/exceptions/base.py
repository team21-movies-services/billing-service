class ObjectDoesNotExist(Exception):
    """Does not exist Exception"""


class TariffDoesNotExist(ObjectDoesNotExist):
    """Tariff does not exist Exception"""


class UserCurrentSubscriptionNotExist(ObjectDoesNotExist):
    """User doesn't have active subscription Exception"""
