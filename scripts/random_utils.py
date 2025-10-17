import math

class LCG:
    def __init__(self, seed=1, a=1664525, c=1013904223, m=2**32):
        self.x = seed % m
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x
    
    def random(self):
        return self.next()

    def sample(self, n):
        output = []
        for _ in range(n):
            output.append(self.next())
        return output
    
class Unif(LCG):
    def __init__(self, a=0, b=1, seed=1, m=2**32):
        super().__init__(seed=seed, m=m)  # forward full LCG params
        self.low = a
        self.high = b
        self.m = m

    def next(self):
        x = super().next() / self.m
        # print(x*self.m)
        return self.low + (self.high - self.low) * x
    
    def random(self):
        return self.next()

    def sample(self, n):
        output = []
        for _ in range(n):
            output.append(self.next())
        return output
    
class Gamma(Unif):
    def __init__(self, k, theta=1, seed=1, m=2**32):
        super().__init__(seed=seed, m=m)
        if k <= 0 or theta <= 0:
            raise ValueError("k and theta must be > 0")
        self.k = int(k)
        self.theta = theta

    def next(self):
        total = 0
        for _ in range(self.k):
            u = super().next()
            total += -math.log(1 - u) * self.theta
        return total

    def sample(self, n):
        return [self.next() for _ in range(n)]
    
class Geometric(Unif):
    def __init__(self, p, seed = 1, m =2**32):
        super().__init__(seed = seed, m=m)
        
        if not (0<p<1):
            raise ValueError("Probability of success should lie in (0,1)")
        else:
            self.p = p
    
    def next(self):
        u = super().next()
        x = (math.log(1-u))/(math.log(1-self.p))
        return math.ceil(x)
    
    def random(self):
        return self.next()

    def sample(self, n):
        output = []
        for _ in range(n):
            output.append(self.next())
        return output
    
class Poisson(Unif):
    def __init__(self, lmda, seed=1, m=2**32):
        super().__init__(a=0, b=1, seed=seed, m=m)
        if lmda <= 0:
            raise ValueError("λ (lmda) must be > 0")
        self.lmda = lmda

    def next(self):
        L = math.exp(-self.lmda)
        k = 0
        p = 1.0

        while p > L:
            k += 1
            u = super().next()
            p *= u

        return k - 1

    def sample(self, n):
        return [self.next() for _ in range(n)]

class Exponential(Unif):
    def __init__(self, lmda, seed = 1, m =2**32):
        super().__init__(seed = seed, m=m)
        
        if lmda <= 0:
            raise ValueError("Lambda should be strictly positive!!!")
        else:
            self.lmda = lmda

    def next(self):
        u = super().next()
        return -(math.log(1-u))/self.lmda
    
    def random(self):
        return self.next()

    def sample(self, n):
        output = []
        for _ in range(n):
            output.append(self.next())
        return output
    
class HalfNormal:
    def __init__(self, lmda=1, seed=1, m= 2**32):
        if lmda <= 0:
            raise ValueError("Lambda must be > 0")
        
        self.lmda = lmda
        self.proposal = Exponential(lmda=lmda, seed=seed, m=m)   # proposal Exp(λ)
        self.aux = Unif(a=0, b=1, seed=seed+1, m=m)              # uniform(0,1) for acceptance
        self.M = self.compute_M()                           # envelope constant

    def half_normal_pdf(self, x):
        if x < 0:
            return 0
        return math.sqrt(2/math.pi) * math.exp(-x**2 / 2)

    def proposal_pdf(self, x):
        if x < 0:
            return 0
        return self.lmda * math.exp(-self.lmda * x)

    def compute_M(self):
        """
        Compute the envelope constant M = sup_x f(x)/g(x).
        """
        # Analytical bound: maximize f(x)/g(x) over x>=0
        # f(x)/g(x) = sqrt(2/pi)/λ * exp(-x^2/2 + λx)
        # The exponent is quadratic in x, max at x=λ
        x_star = self.lmda
        ratio = self.half_normal_pdf(x_star) / self.proposal_pdf(x_star)
        return ratio

    def sample(self, n):
        """
        Generate n samples from the half-normal distribution.
        """
        samples = []
        while len(samples) < n:
            x = self.proposal.next()
            u = self.aux.next()
            if u <= self.half_normal_pdf(x) / (self.M * self.proposal_pdf(x)):
                samples.append(x)
        return samples

class Gamma(Unif):
    def __init__(self, k, theta=1, seed=1, m=2**32):
        super().__init__(seed=seed, m=m)
        if k <= 0 or theta <= 0:
            raise ValueError("k and theta must be > 0")
        self.k = int(k)
        self.theta = theta

    def next(self):
        total = 0
        for _ in range(self.k):
            u = super().next()
            total += -math.log(1 - u) * self.theta
        return total

    def sample(self, n):
        return [self.next() for _ in range(n)]
    
class Beta(Unif):
    def __init__(self, alpha, beta, seed=1, m=2**32):
        super().__init__(seed=seed, m=m)
        if alpha <= 0 or beta <= 0:
            raise ValueError("alpha and beta must be > 0")
        self.alpha = int(alpha)  # assume integer for Gamma construction
        self.beta = int(beta)

        self.gamma1 = Gamma(self.alpha, theta=1, seed=seed)
        self.gamma2 = Gamma(self.beta, theta=1, seed=seed+100)

    def next(self):
        y1 = self.gamma1.next()
        y2 = self.gamma2.next()
        return y1 / (y1 + y2)

    def sample(self, n):
        return [self.next() for _ in range(n)]