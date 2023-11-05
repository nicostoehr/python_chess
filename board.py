class DefaultFigureCodec:
    w_p = 1
    w_r = 2
    w_kn = 3
    w_b = 4
    w_k = 5
    w_q = 6
    b_p = 11
    b_r = 12
    b_kn = 13
    b_b = 14
    b_k = 15
    b_q = 16

def initialize_board(c = DefaultFigureCodec):
    m = [[0 for i in range(8)] for j in range(8)]
    # PAWNS
    for i in range(8):
        #m[i][1] = c.w_p
        m[i][6] = c.b_p

    # OTHER FIGURES
    m[0][0] = c.w_r
    m[1][0] = c.w_kn
    m[2][0] = c.w_b
    m[3][0] = c.w_k
    m[4][0] = c.w_q
    m[5][0] = c.w_b
    m[6][0] = c.w_kn
    m[7][0] = c.w_r
    m[0][7] = c.b_r
    m[1][7] = c.b_kn
    m[2][7] = c.b_b
    m[3][7] = c.b_k
    m[4][7] = c.b_q
    m[5][7] = c.b_b
    m[6][7] = c.b_kn
    m[7][7] = c.b_r

    #RETURN
    return m
