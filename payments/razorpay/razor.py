import razorpay
from constants.const import RAZORPAY_ID, RAZORPAY_AUTH_KEY


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PaymentRazorpay(metaclass=Singleton):
    razorpay_client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_AUTH_KEY))
