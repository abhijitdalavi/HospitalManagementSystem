from random import shuffle

from DataGenerator.config import *


def inheritors(cls):
    """
    Finds all descendant classes of a given class.
    Taken from: https://stackoverflow.com/questions/5881873/python-find-all-classes-which-inherit-from-this-one
    :param cls: class, which descendants one wants to find
    :return:
    """
    subclasses = set()
    work = [cls]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


class Singleton:
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        Redefine __new__ for creating single object.
        :param cls: the class itself
        :return: instance of the class
        """
        if not hasattr(cls, 'instance'):
            print("Creating: " + str(cls))
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self._initialized: return
        self._initialized = True


class Pool(Singleton):
    _name = None
    _data = None

    def __init__(self):
        if not self._initialized:
            print(f"Calling init from: {self.__class__}")
            self.init_data()
        super().__init__()

    def _get_data(self):
        with open(self._name, 'r', encoding='utf-8') as f:
            return f.read().splitlines()

    def get(self, n: int = 1):
        return None if len(self._data) == 0 else self._data.pop()

    def init_data(self):
        self._data = self._get_data()
        shuffle(self._data)


class AddressPool(Pool):
    """
    This is a singleton that stores all available emails.
    Emails are static and were generated with some script.
    They are stored in a file (one email on a single line).
    """

    def __init__(self):
        self._name = "DataGenerator/address.txt"
        super().__init__()


class FNamePool(Pool):
    def __init__(self):
        self._name = "DataGenerator/first_names.all.txt"
        super().__init__()


class LNamePool(Pool):
    def __init__(self):
        self._name = "DataGenerator/last_names.all.txt"
        super().__init__()


class EmailPool(Pool):
    def __init__(self):
        self._name = "DataGenerator/email.txt"
        super().__init__()


class PhonePool(Pool):
    def __init__(self):
        self._name = "DataGenerator/phone.txt"
        super().__init__()


class PasswordPool(Pool):
    def __init__(self):
        self._name = "DataGenerator/password.txt"
        super().__init__()


class UserIDPool(Pool):
    def init_data(self):
        self._data = list(reversed([i for i in range(1, 100001)]))


class WorkingStaffIDPool(Pool):
    def init_data(self):
        self._data = list(reversed([i for i in range(1, USER_NUMBER)]))


class AppointmentIDPool(Pool):
    def init_data(self):
        self._data = list(reversed([i for i in range(1, 100001)]))


class LicensePool(Pool):
    def init_data(self):
        self._data = [i for i in range(10 ** 5, 10 ** 6)]
        shuffle(self._data)


class AccountantLicensePool(LicensePool):
    pass


class PharmacistLicensePool(LicensePool):
    pass


class SlotPool(Pool):
    data = []
    _data = data

    def __init__(self):
        pass

    def _get_data(self):
        pass


class DoctorRoomPool(Pool):
    def init_data(self):
        self._data = [i for i in range(1, DOCTOR_NUMBER + 1)]
        shuffle(self._data)


class GeneralPool(Singleton):
    def __init__(self):
        super().__init__()
        subs = inheritors(Pool)
        for sub in subs:
            # print(sub)
            self.__setattr__("_" + sub.__name__.lower(), sub())

    def get(self, name):
        """
        Get something from general pool.
        :param name: what one wants to get.
        Possible values: email, fname, lname, address, phone, password, userID, AccountantLicense, PharmacistLicense,
        AppointmentID, slot, DoctorRoom
        (Not case sensitive).
        :return: random value of what is requested
        """
        return self.__getattribute__(f"_{name.lower()}pool").get()


if __name__ == "__main__":
    sos = GeneralPool()
    sos1 = GeneralPool()
    print(sos.get("email"))
