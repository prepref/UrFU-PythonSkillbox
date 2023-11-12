import random


def get_sum(a, b):
    """ 
    Sums up two numbers
	:param a: first number
	:param b: second number
        :return: sum of a and b
	"""
    # Sums up two numbers
    # a - first number; b - second number
    return a + b # sum of a and b


def generate_words(count, word_len, alpha):
    """
	Generates list of random words
	:param count: word count
	:param word_len: word length
	:param alpha: alphabet
	:return: list of random words
	"""
    # Generates list of random words
    # count - word count
    # word_len - word length
    # alpha - alphabet
    return [''.join([random.choice(alpha) for _ in range(word_len)]) for _ in range(count)]  # list of random words

def get_id(length):
    """
	Generates random id
	:param length: id length
	:return: generated random id
	"""
    # Generates random id
    # length - id length
    return ''.join(map(str, [random.randint(0, 9) for _ in range(length)]))  # generated random id


def register_new_user(name, age, email):  # user name, user age, user email
    """
	Register new user in system
	:param name: user name
	:param age: user age
	:param email: user email
	:return: registered user
	"""
    # Register new user in system
    return MyUser(name, age, email)  # registered user

class MyUser:
    def __init__(self, name, age, email):
        """
        initialisation of class
        :param name: user name
        :param age: user age
        :param email: user email
        """
        # initialisation of class
        self.name = name  # user name
        self.age = age  # user age
        self.email = email  # user email
        self.user_id = get_id(6)

    def get_card(self):
        """
		Get user data
		:return: user data in string format
		"""
		# Get user data
        return f'{self.user_id}: {self.name} ({self.age})'  # user data in string format

    def upload_to_database(self):	
        """
        Upload user data to database
        :return: None
        """
        # Upload user data to database
        raise NotImplementedError
        # return None