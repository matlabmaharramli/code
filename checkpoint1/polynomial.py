class Polynomial:
    
    def __init__(self, list):
        self.list = list

    def order(self):
        order = len(self.list)
        return order
    
    def __add__(self, other):

        polynomial_sum = []

        if(self.order()>=other.order()):
            polynomial_sum = self.list.copy()
            for i in range(other.order()):
                polynomial_sum[i] = polynomial_sum[i] + other.list[i]
            
        elif(self.order()<other.order()):
            polynomial_sum = other.list
            for i in range(self.order()):
                polynomial_sum[i] = polynomial_sum[i] + self.list[i]
        
        return Polynomial(polynomial_sum)
    
    def derivative(self):
        derivative = []

        for i in range(1, self.order()):
            derivative.append((i)*self.list[i])
        return Polynomial(derivative)
    
    def indefinite_integral(self, integration_constant):
        indefinite_integral = [integration_constant]

        for i in range(self.order()):
            indefinite_integral.append(self.list[i]/(i+1))
        return Polynomial(indefinite_integral)
    
    def __str__(self):
        polynomial_string = ""
        isNonzero = False
        
        for i in range(0, self.order()):
            if (self.list[i] > 0) & (isNonzero):
                polynomial_string = polynomial_string + f" + {self.list[i]:g} x^{i}"
            
            elif (self.list[i] < 0) & (isNonzero):
                polynomial_string = polynomial_string + f" - {(-self.list[i]):g} x^{i}"


            elif self.list[i] != 0:
                isNonzero = True

                if i != 0:
                    polynomial_string = f"{self.list[i]:g} x^{i}"
                elif i == 0:
                    polynomial_string = f"{self.list[i]:g}"
       
        return polynomial_string