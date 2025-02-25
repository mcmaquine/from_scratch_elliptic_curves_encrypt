class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            raise ValueError( 'Num {} not in field range 0 to {}'.format(num, prime - 1))
        self.num    =   num
        self.prime  =   prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime
    
    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num =   (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)
    
    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add sub numbers in different Fields')
        num =   (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)
    
    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply numbers in different Fields')
        num =   (self.num * other.num)  % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, power):
        #num =   (self.num ** power) % self.prime
        
        n = power % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)
    
    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide numbers in different Fields')
        num = (self.num * other.num ** (other.prime - 2)) % self.prime
        return self.__class__(num, self.prime)
    
class Point:

    def __init__(self, x, y, a, b):
        self.a  =   a
        self.b  =   b
        self.x  =   x
        self.y  =   y

        if self.x is None and self.y is None:
            return
        
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError('{} {} is not on the curve'.format(x,y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y \
               and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self.__eq__( other )

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError('Points {}, {} are note on the same curve'.format(self, other))

        if self.x is None:
            return other
        if other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return Point(None, None, self.a, self.b)

        if self.x != other.x:
            s = (other.y - self.y)/(other.x - self.x)
            x3 = s**2 - self.x - other.x
            y3 = s*(self.x - x3) - self.y

            return self.__class__(x3, y3, self.a, self.b)