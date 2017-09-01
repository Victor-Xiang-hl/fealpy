import numpy as np

class SinSinData:
    def __init__(self):
        pass

    def solution(self, p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = np.sin(pi*x)*np.sin(pi*x)*np.sin(pi*y)*np.sin(pi*y)
        return r

    def gradient(self, p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        val = np.zeros((len(x),2), dtype=p.dtype)
        val[:,0] = 2*pi*np.sin(pi*x)*np.cos(pi*x)*np.sin(pi*y)*np.sin(pi*y)
        val[:,1] = 2*pi*np.sin(pi*x)*np.sin(pi*x)*np.sin(pi*y)*np.cos(pi*y)
        return val


    def laplace(self, p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = 2*pi**2*np.cos(pi*y)**2*np.sin(pi*x)**2
        r += 2*pi**2*np.cos(pi*x)**2*np.sin(pi*y)**2 
        r -= 4*pi**2*np.sin(pi*x)**2*np.sin(pi*y)**2
        return r

    def dirichlet(self, p):
        """ Dilichlet boundary condition
        """
        return self.solution(p)

    def neuman(self, p, n):
        """ Neuman boundary condition
        """
        val = self.gradient(p)
        return np.sum(val*n, axis=1)

    def source(self, p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        pi4 = pi**4
        r1 = np.sin(pi*x)**2
        r2 = np.cos(pi*x)**2
        r3 = np.sin(pi*y)**2
        r4 = np.cos(pi*y)**2
        r = 8*pi4*r2*r4 - 16*pi4*r4*r1 - 16*pi4*r2*r3 + 24*pi4*r1*r3
        return r

    def is_boundary_dof(self, p):
        eps = 1e-14 
        return (p[:,0] < eps) | (p[:,1] < eps) | (p[:, 0] > 1.0 - eps) | (p[:, 1] > 1.0 - eps)

class BiharmonicData2:
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def solution(self,p):
        """ The exact solution 
        """
        a = self.a
        b = self.b
        x = p[:, 0]
        y = p[:, 1]
        r = 2350*(x**4)*(x-a)*(x-a)*(y**4)*(y-b)*(y-b)
        return r

    def gradient(self,p):
        x = p[:, 0]
        y = p[:, 1]
        a = self.a
        b = self.b
        val = np.zeros((len(x), 2), dtype=p.dtype)
        val[:,0] = 2350*2*(x**3)*(x-a)*(3*x-2*a)*(y**4)*(y-b)*(y-b)
        val[:,1] = 2350*(x**4)*(x-a)*(x-a)*2*(y**3)*(y-b)*(3*y-2*b)
        return val

    def laplace(self,p):
        x = p[:, 0]
        y = p[:, 1]
        a = self.a
        b = self.b
        r = 2350*(y**6-2*b*y**5+b**2*y**4)*(30*x**4-40*a*x**3+12*a**2*x**2)
        r += 2350*(x**6-2*a*x**5+a**2*x**4)*(30*y**4-40*b*y**3+12*b**2*y**2)
        return r


    def dirichlet(self, p):
        """ Dilichlet boundary condition
        """
        return np.zeros((p.shape[0],), dtype=np.float)

    def neuman(self, p, n):
        """ Neuman boundary condition
        """
        return np.zeros((p.shape[0],), dtype=np.float)

    def source(self,p):
        x = p[:, 0]
        y = p[:, 1]
        a = self.a
        b = self.b
        r1 = 56400*(a**2-10*a*x+15*x**2)*(b-y)*(b-y)*y**4
        r2 = 18800*x**2*(6*a**2-20*a*x+15*x**2)*y**2*(6*b**2-20*b*y+15*y**2)
        r3 = 56400*(a-x)*(a-x)*x**4*(b**2-10*b*y+15*y**2)
        r = r1 + r2 + r3
        return r

    def is_boundary_dof(self, p):
        eps = 1e-14 
        return (p[:,0] < eps) | (p[:,1] < eps) | (p[:, 0] > 1.0 - eps) | (p[:, 1] > 1.0 - eps)

class BiharmonicData3:
    def __init__(self):
        pass
    
    def solution(self, p):
        """ The exact solution 
        """
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = np.cos(2*pi*x)*np.cos(2*pi*y)
        return r

    def gradient(self,p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        val = np.zeros((len(x), 2), dtype=p.dtype)
        val[:,0] = -2*pi*np.sin(2*pi*x)*np.cos(2*pi*y) 
        val[:,1] = -2*pi*np.cos(2*pi*x)*np.sin(2*pi*y)
        return val

    def laplace(self,p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = -8*pi**2*self.solution(p)
        return r


    def dirichlet(self, p):
        """ Dilichlet boundary condition
        """
        return self.solution(p) 

    def neuman(self, p, n):
        """ Neuman boundary condition
        """
        return np.zeros(p.shape[0], dtype=p.dtype) 

    def source(self,p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = 64*pi**4*np.cos(2*pi*x)*np.cos(2*pi*y)
        return r

    def is_boundary_dof(self, p):
        eps = 1e-14 
        return (p[:,0] < eps) | (p[:,1] < eps) | (p[:, 0] > 1.0 - eps) | (p[:, 1] > 1.0 - eps)

class BiharmonicData4:
    def __init__(self):
        pass
    
    def solution(self, p):
        """ The exact solution 
        """
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = np.sin(2*pi*x)*np.sin(2*pi*y)
        return r

    def gradient(self,p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        val = np.zeros((len(x), 2), dtype=p.dtype)
        val[:,0] = 2*pi*np.cos(2*pi*x)*np.sin(2*pi*y) 
        val[:,1] = 2*pi*np.cos(2*pi*y)*np.sin(2*pi*x)
        return val


    def laplace(self,p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = -8*pi**2*self.solution(p)
        return r


    def dirichlet(self, p):
        """ Dilichlet boundary condition
        """
        return np.zeros((p.shape[0],), dtype=np.float)

    def neuman(self, p, n):
        """ Neuman boundary condition
        """
        val = self.gradient(p)
        return np.sum(val*n, axis=1)

    def source(self,p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        r = 64*pi**4*np.sin(2*pi*x)*np.sin(2*pi*y)
        return r

    def is_boundary_dof(self, p):
        eps = 1e-14 
        return (p[:,0] < eps) | (p[:,1] < eps) | (p[:, 0] > 1.0 - eps) | (p[:, 1] > 1.0 - eps)


class BiharmonicData5:
    def __init__(self):
        pass
    
    def solution(self, p):
        """ The exact solution 
        """
        x = p[:, 0]
        y = p[:, 1]
        r1 = (x - 0.5)**2 + (y - 0.5)**2 + 0.01
        r2 = (x + 0.5)**2 + (y + 0.5)**2 + 0.01
        return 1.0/r1 - 1.0/r2 

    def gradient(self,p):
        x = p[:, 0]
        y = p[:, 1]
        pi = np.pi
        val = np.zeros((len(x), 2), dtype=p.dtype)
        val[:,0] = -(-2*x - 1.0)/((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**2 + (-2*x + 1.0)/((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**2
        val[:,1] = -(-2*y - 1.0)/((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**2 + (-2*y + 1.0)/((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**2
        return val


    def laplace(self,p):
        x = p[:, 0]
        y = p[:, 1]
        r = (2*x - 1.0)*(4*x - 2.0)/((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**3 - (2*x + 1.0)*(4*x + 2.0)/((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**3 + (2*y - 1.0)*(4*y - 2.0)/((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**3 - (2*y + 1.0)*(4*y + 2.0)/((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**3 + 4/((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**2 - 4/((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**2
        return r


    def dirichlet(self, p):
        """ Dilichlet boundary condition
        """
        return self.solution(p)

    def neuman(self, p, n):
        """ Neuman boundary condition
        """
        val = self.gradient(p)
        return np.sum(val*n, axis=1)

    def source(self,p):
        x = p[:, 0]
        y = p[:, 1]
        r = ((6*x - 3.0)*(8*x - 4.0)*((2*x - 1.0)*(4*x - 2.0) + (2*y - 1.0)*(4*y - 2.0))*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**5 - (6*x + 3.0)*(8*x + 4.0)*((2*x + 1.0)*(4*x + 2.0) + (2*y + 1.0)*(4*y + 2.0))*((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**5 + ((2*y - 1.0)*(4*y - 2.0) + 32)*((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**2*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**5 - ((2*y + 1.0)*(4*y + 2.0) + 32)*((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**5*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**2 + 2*((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**5*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**3 + 2*((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**5*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)*(3*(2*x + 1.0)*(4*x + 2.0) + 4*(2*x + 1.0)*(6*x + 3.0) + 4*(4*x + 2.0)*(6*x + 3.0) + 3*(2*y + 1.0)*(4*y + 2.0)) - 2*((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**3*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**5 - 2*((x - 0.5)**2 + (y - 0.5)**2 + 0.01)*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**5*(3*(2*x - 1.0)*(4*x - 2.0) + 4*(2*x - 1.0)*(6*x - 3.0) + 4*(4*x - 2.0)*(6*x - 3.0) + 3*(2*y - 1.0)*(4*y - 2.0)))/(((x - 0.5)**2 + (y - 0.5)**2 + 0.01)**5*((x + 0.5)**2 + (y + 0.5)**2 + 0.01)**5)
        return r

    def is_boundary_dof(self, p):
        eps = 1e-14 
        return (p[:,0] < eps) | (p[:,1] < eps) | (p[:, 0] > 1.0 - eps) | (p[:, 1] > 1.0 - eps)
