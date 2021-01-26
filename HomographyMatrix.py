import numpy as np
from scipy.linalg import svd

def homographic_matrix(A,B):
    '''
    Retruns the homographic matrix corresponding to the
    homography of 2 images

    Args
        A:  ordered pair of keypoint pixels in the source domain image.
            ndArray of the form [[x,y]...]
        B:  ordered pair of keypoint pixels in the target domain image.
            ndArray of the form [[x,y]...]
    Returns
        A matrix H, corresponding to the homographic matrix
    '''
    def last_singular_vector(M):
        '''
        Returns the last singular vector in V in the SVD UEV^T of the 
        matrix given
        Args
            M: Matrix upon whom svd has to be performed
        '''
        U, s, VT = svd(M)
        return VT.T[:,-1]
    
    def generate_P_matrix(A,B):
        '''
        Returns the matrix that satisfies the homographic equation
        
        Args
        A:  ordered pair of keypoint pixels in the source domain image.
            ndArray of the form [[x,y]...]
        B:  ordered pair of keypoint pixels in the target domain image.
            ndArray of the form [[x,y]...]
        Returns
            A matrix H, corresponding to the homographic matrix
        '''
        A_ = np.ones((4, 3))
        A_[:,:-1] = A
        
        B_ = np.ones((4, 3))
        B_[:, :-1] = B

        P = np.zeros((8,9))
        P[::2,0:3] = -1*A_
        P[1::2,3:6] = -1*A_

        P[0, 6:9] = A_[0,:]*B_[0, 0]
        P[1, 6:9] = A_[0,:]*B_[0, 1]
        P[2, 6:9] = A_[1,:]*B_[1, 0]
        P[3, 6:9] = A_[1,:]*B_[1, 1]
        P[4, 6:9] = A_[2,:]*B_[2, 0]
        P[5, 6:9] = A_[2,:]*B_[2, 1]
        P[6, 6:9] = A_[3,:]*B_[3, 0]
        P[7, 6:9] = A_[3,:]*B_[3, 1]
        return P
    P = generate_P_matrix(A, B)
    V = last_singular_vector(P)
    H = V.reshape(3,3)
    return H
