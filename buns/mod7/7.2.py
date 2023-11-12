import unittest

class TestMultiply(unittest.TestCase):
	def test_multiply(self):	
		# multiply int and int
		result = multiply(5, 5)
		self.assertEqual(result, 25)		
		
		# multiply int and -int
		result = multiply(5, -5)
		self.assertEqual(result, -25)
		
		# multiply -int and int
		result = multiply(-5, 5)
		self.assertEqual(result, -25)
		
		# multiply -int and -int
		result = multiply(-5, -5)
		self.assertEqual(result, 25)
		
		# multiply zero and zero
		result = multiply(0, 0)
		self.assertEqual(result, 0)	
		
		# multiply int and zero
		result = multiply(2, 0)
		self.assertEqual(result, 0)	
		
		# multiply zero and float
		result = multiply(0, 2.5)
		self.assertEqual(result, 0)	
		
		# multiply float and int
		result = multiply(2.5,1)
		self.assertEqual(result, 2.5)	
		
		# multiply float and float
		result = multiply(1.5, 3.5)
		self.assertEqual(result, 5.25)
			
		# multiply big int and int
		result = multiply(2**10, 2)
		self.assertEqual(result, 2*2**10)
		
		# multiply int and big int
		result = multiply(2,2**10)
		self.assertEqual(result, 2*2**10)
		
		# multiply big int and big int
		result = multiply(10**10, 10**20)
		self.assertEqual(result, 10**30)
		
		
loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestMultiply)
runner = unittest.TextTestRunner()
result = runner.run(suite)