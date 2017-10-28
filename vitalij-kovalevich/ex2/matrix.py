import random
import operator
import sys

class MatrixError(BaseException):
    """ ����� ���������� ��� ������ """
    pass

class Matrix(object):
    """������� ����� ������� � Python
    �������� �������� �������� ������� �����������
    ����� ���������� ���������� 
    """
    def __init__(self, n, m, init=True):
        """�����������
        #���������:
            n    :  int, ����� �����
            m    :  int, ����� �������� 
            init :  (�������������� ��������), ����������.
                    ���� False, �� ��������� ������ ������
        """
        if init:
            # ������� ������ �����
            self.array = [[0]*m for x in range(n)]
        else:
            self.array = []

        self.n = n
        self.m = m

    def __getitem__(self, idx):
        """���������� ��������� ��������� �������� ������� 
        """
        # ���������, ���� ������ - ��� ������ ��������
        if isinstance(idx, tuple): 
            if len(idx) == 2: 
                return self.array[idx[0]][idx[1]]
            else:
                # � ������� ���� ������ ������ � �������
                raise MatrixError("Matrix has only two shapes!")
        else:
            return self.array[idx]

    def __setitem__(self, idx, item):
        """���������� ��������� ������������ 
        """
        # ���������, ���� ������ - ��� ������ ��������
        if isinstance(idx, tuple):
            if len(idx) == 2: 
                self.array[idx[0]][idx[1]] = item
            else:
                # � ������� ���� ������ ������ � �������
                raise MatrixError("Matrix has only two shapes!")
        else:
            self.array[idx] = item

    def __str__(self):
        """�������������� ����� ������ ������� � �������
        """
        s='\n'.join([' '.join([str(item) for item in row]) for row in self.array])
        return s + '\n'

    def getRank(self):
        """�������� ����� ����� � ��������
        """
        return (self.n, self.m)


    def __eq__(self, mat):
        """ �������� �� ��������� """

        return (mat.array == self.array)

    def transpose(self):
        """ ����������������� ������������� ������� 
    
            ����� ����� ������� ���� ��� ��� �������� 
            �������, ������������ �����������������
            �������
            Aij = Aji
            
        """
        mat = Matrix(self.m, self.n)
        for i in range(self.n):
            for j in range(self.m):
                mat[j][i] = self.array[i][j]
                
        return mat

    def __add__(self, mat):
        """ ��������������� �������� �������� "+"
        ��� ������
        """
        mulmat = Matrix(self.n, self.m)
        if self.getRank() != mat.getRank():
            raise MatrixError("Trying to add matrixes of varying rank!")

        for i in range(self.n):
            for j in range(self.m):
                self.array[i][j] = self.array[i][j]+mat[i][j]
        '''
        ���� ������� ��� �������, �����������
        �������� ��������
        Cij = Aij+Bij
        '''
        return self
        

    def __sub__(self, mat):
        """ ��������������� �������� ��������� "-"
        ��� ������
        """
        mulmat = Matrix(self.n, self.m)
        if self.getRank() != mat.getRank():
            raise MatrixError("Trying to add matrixes of varying rank!")
        for i in range(self.n):
            for j in range(self.m):
                self.array[i][j] = self.array[i][j] - mat[i][j]

        '''
        ���� ������� ��� �������, �����������
        �������� ���������
        Cij = Aij-Bij
        '''
        return self

    def __mul__(self, mat):
        """������������ ������� ��� ���������� ���������"""
        mulmat = Matrix(self.n, self.m) # �������������� �������

        # ���� ������ �������� - �����, �� 
        # ������ �������� ������ ������� �� ��� �����
        if isinstance(mat, int) or isinstance(mat, float):
            for i in range(self.n):
                for j in range(self.m):
                    mulmat[i][j] = self.array[i][j]*mat
            return mulmat
        else:
            # ��� ����������� ������������ ������  
            # �� ����������� ������ ���� �����������
            if (self.n != mat.n or self.m != mat.m):
                raise MatrixError("Matrices cannot be multipled!")
                
            for i in range(self.n):
                for j in range(self.m):
                    mulmat[i][j] = self.array[i][j]*mat[i][j]
            return mulmat

    def dot(self, mat):
        """ ��������� ��������� """
        
        matn, matm = mat.getRank()
        matr = Matrix(self.n, self.m)
        # ��� ������������ ������ ����� �������� ����� 
        # ������ ��������� ����� ����� � ������
        if (self.m != matn):
            raise MatrixError("Matrices cannot be multipled!")
        for i in range(self.n):
            for j in range(self.m):
                matr[i][j] = 0
                for k in range(2):
                    matr[i][j] += mat[i][k]*self.array[k][j]
               
        '''
        ����� �������� ���, ����������� 
        ��������� ������������ � ������������
        ����� �������
        Cij = sum(Aik*Bkj)
        '''
        return matr

    @classmethod
    def _makeMatrix(cls, array):
        """��������������� ������������
        """
        n = len(array)
        m = len(array[0])
        # Validity check
        if any([len(row) != m for row in array[1:]]):
            raise MatrixError("inconsistent row length")
        mat = Matrix(n,m, init=False)
        mat.array = array

        return mat

    @classmethod
    def fromList(cls, listoflists):
        """ �������� ������� �������� �� ������ """

        # E.g: Matrix.fromList([[1 2 3], [4,5,6], [7,8,9]])

        array = listoflists[:]
        return cls._makeMatrix(array)

    @classmethod
    def makeId(cls, n):
        """ ������� ��������� ������� ������� (nxn) """

        array = [[0]*n for x in range(n)]
        idx = 0
        for row in array:
            row[idx] = 1
            idx += 1

        return cls.fromList(array)


if __name__ == "__main__":
    a = Matrix.fromList([[1,2], [3, 4]])
    print(a)
    print(a*2)
    print('Identity:')
    print(Matrix.makeId(3))
    print(a)
    print(Matrix.dot(a,a))
    pass

