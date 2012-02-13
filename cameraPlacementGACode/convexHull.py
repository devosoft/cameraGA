class CH(object):
    """Computes the convex hull of a set of 2D points.
 
    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """
    def __init__(self):
        ''''''
        
    def __str__(self):
        theStr=str(self.points)
        return theStr
        
    def convexHull(self, P):
        "Calculate the convex hull of a set of points."

        # Get a local list copy of the points and sort them lexically.
        #points = map(None, P)
        #points.sort()
        in_points = list(P)
        points = []
        for point in in_points:
          if point not in points:
            points.append(point)
        points.sort()

        # Build upper half of the hull.
        upper = [points[0], points[1]]
        for p in points[2:]:
            upper.append(p)
            while len(upper) > 2 and not self._isRightTurn(upper[-3:]):
                del upper[-2]

        # Build lower half of the hull.
        points.reverse()
        lower = [points[0], points[1]]
        for p in points[2:]:
            lower.append(p)
            while len(lower) > 2 and not self._isRightTurn(lower[-3:]):
                del lower[-2]

        # Remove duplicates across lower and upper hulls.
        del lower[0]
        del lower[-1]

        # Concatenate both halfs and return.
        return list(upper + lower)

    def _isRightTurn(self, pqr): 
        "Do the vectors pq:qr form a right turn, or not?"
        p = pqr[0]
        q = pqr[1]
        r = pqr[2]
        assert p != q and q != r and p != r
                
        if self._myDet(p, q, r) < 0:
            return 1
        else:
            return 0

    def _myDet(self, p, q, r):
        """Calc. determinant of a special matrix with three 2D points.

        The sign, "-" or "+", determines the side, right or left,
        respectivly, on which the point r lies, when measured against
        a directed vector from p to q.
        """

        # We use Sarrus' Rule to calculate the determinant.
        # (could also use the Numeric package...)
        sum1 = q[0]*r[1] + p[0]*q[1] + r[0]*p[1]
        sum2 = q[0]*p[1] + r[0]*q[1] + p[0]*r[1]

        return sum1 - sum2


    def polygon_area(self, t):  
        if t[0] != t[-1]: t.append(t[0])  
        A = 0.0  
        for i in range(len(t)-1):  
                A += t[i][0]*t[i+1][1] - t[i][1]*t[i+1][0]
        return abs(A/2)
        
