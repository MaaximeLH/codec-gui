import os
import numpy as np


# Codec class
class CODEC:
    # Methods
    bytes = {}
    encodedBytes = {}
    decodedBytes = {}
    matrix = {}
    identity = []

    # Constructor
    def __init__(self):
        self.fill_array_bytes()

    # Load matrix from path, and get matrix identity, fill encoded & decoded bytes (for prediction)
    def load_matrix(self, path):
        file = os.path.relpath(path)
        # Get matrix
        matrix = open(file, 'r').read().split('[')[1].split(']')[0]
        matrix = matrix.replace(' ', '')

        # Insert of matrix into Array
        amatrix = []
        amatrix.append(list(matrix[:8]))
        amatrix[0] = [int(i) for i in amatrix[0]]
        amatrix.append(list(matrix[8:16]))
        amatrix[1] = [int(i) for i in amatrix[1]]
        amatrix.append(list(matrix[16:24]))
        amatrix[2] = [int(i) for i in amatrix[2]]
        amatrix.append(list(matrix[24:32]))
        amatrix[3] = [int(i) for i in amatrix[3]]
        amatrix = np.array(amatrix, dtype=bool)

        self.matrix = amatrix
        self.get_matrixidentity()
        self.fill_array_encoded_bytes()
        self.fill_array_decoded_bytes()
        return True

    # Get matrix identity
    def get_matrixidentity(self):
        matrix = np.array(self.matrix, dtype=int)

        first = 0
        second = 0
        third = 0
        fourth = 0
        i = 0

        while i < 7:
            if matrix[0][i] == 1 and matrix[1][i] == 0 and matrix[2][i] == 0 and matrix[3][i] == 0:
                first = i
            if matrix[0][i] == 0 and matrix[1][i] == 1 and matrix[2][i] == 0 and matrix[3][i] == 0:
                second = i
            if matrix[0][i] == 0 and matrix[1][i] == 0 and matrix[2][i] == 1 and matrix[3][i] == 0:
                third = i
            if matrix[0][i] == 0 and matrix[1][i] == 0 and matrix[2][i] == 0 and matrix[3][i] == 1:
                fourth = i
            i += 1

        self.identity = [first, second, third, fourth]

    # Get all bytes between 0 & 255 into bytes array
    def fill_array_bytes(self):
        for i in range(0, 256):
            self.bytes[i] = i.to_bytes(1, byteorder="big")

    # Get all encoded bytes between 0 & 255 into encodedBytes array
    def fill_array_encoded_bytes(self):
        for i in range(0, 256):
            self.encodedBytes[i] = self.get_encoded_byte(i)

    # Get all decoded bytes between [0-255][0-255] into decodedBytes array
    def fill_array_decoded_bytes(self):
        for i in range(0, 256):
            x1 = bin(i)[2:].zfill(8)
            u1 = ""
            for j in range(0, 4):
                u1 += x1[self.identity[j]]

            self.decodedBytes[i] = {}

            for k in range(0, 256):
                x2 = bin(k)[2:].zfill(8)
                u2 = ""
                for l in range(0, 4):
                    u2 += x2[self.identity[l]]

                self.decodedBytes[i][k] = self.bytes[int(u1 + u2, 2)]

    # Multiply vector parameter with matrix method and return bytes
    def get_encoded_byte(self, vector):
        binary = list(bin(vector)[2:].zfill(8))
        binary = [int(i) for i in binary]

        u1 = np.array(binary[:4], dtype=bool)
        x1 = str(np.array_str(1 * np.dot(u1, self.matrix))).strip('[]').replace(' ', '')
        u2 = np.array(binary[4:], dtype=bool)
        x2 = str(np.array_str(1 * np.dot(u2, self.matrix))).strip('[]').replace(' ', '')

        encoded = self.bytes[int(x1, 2)]
        encoded += self.bytes[int(x2, 2)]

        return encoded

    # Encode file
    def encode(self, path):

        if len(self.matrix) == 0:
            raise Exception("Please load G4C matrix")

        with open(path + "c", 'wb') as e:
            with open(path, 'rb') as f:
                o = f.read(1)
                while o != b"":
                    int_byte = int.from_bytes(o, byteorder="big")
                    e.write(self.encodedBytes[int_byte])
                    o = f.read(1)
                f.close()
            e.close()

        return True

    # Decode file
    def decode(self, path):

        if len(self.matrix) == 0:
            raise Exception("Please load G4C matrix")

        with open(path + "d", 'wb') as d:
            with open(path, 'rb') as f:
                o = f.read(2)
                while o != b"":
                    d.write(self.decodedBytes[o[0]][o[1]])
                    o = f.read(2)
                f.close()
            d.close()

        return True