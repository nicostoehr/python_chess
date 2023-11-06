def pawn_moves(bm, fp, iw):
    pm = []
    if iw:
        # TILE IN FRONT IS EMPTY
        if bm[fp[0]][fp[1] + 1] == 0:
            pm.append([fp[0], fp[1] + 1])
            if fp[1] == 1:
                pm.append([fp[0], fp[1] + 2])
        if 0 < fp[0] and bm[fp[0] - 1][fp[1] + 1]:
            pm.append([fp[0] - 1, fp[1] + 1])
        if 7 > fp[0] and bm[fp[0] + 1][fp[1] + 1]:
            pm.append([fp[0] + 1, fp[1] + 1])
    else:
        # TILE IN FRONT IS EMPTY
        if bm[fp[0]][fp[1] - 1] == 0:
            pm.append([fp[0], fp[1] - 1])
            if fp[1] == 6:
                pm.append([fp[0], fp[1] - 2])
        if 0 < fp[0] and bm[fp[0] - 1][fp[1] - 1]:
            pm.append([fp[0] - 1, fp[1] - 1])
        if 7 > fp[0] and bm[fp[0] + 1][fp[1] - 1]:
            pm.append([fp[0] + 1, fp[1] - 1])
    return pm


def rook_moves(bm, fp, iw):
    pm = []
    # RIGHT
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[0] + fields_out <= 7:
            if bm[fp[0] + fields_out][fp[1]] == 0:
                pm.append([fp[0] + fields_out, fp[1]])
            elif (iw and bm[fp[0] + fields_out][fp[1]] > 10) or (not iw and bm[fp[0] + fields_out][fp[1]] < 10):
                pm.append([fp[0] + fields_out, fp[1]])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    # LEFT
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[0] - fields_out <= 7:
            if bm[fp[0] - fields_out][fp[1]] == 0:
                pm.append([fp[0] - fields_out, fp[1]])
            elif (iw and bm[fp[0] - fields_out][fp[1]] > 10) or (
                    not iw and bm[fp[0] - fields_out][fp[1]] < 10):
                pm.append([fp[0] - fields_out, fp[1]])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    # UP
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[1] + fields_out <= 7:
            if bm[fp[0]][fp[1] + fields_out] == 0:
                pm.append([fp[0], fp[1] + fields_out])
            elif (iw and bm[fp[0]][fp[1] + fields_out] > 10) or (
                    not iw and bm[fp[0]][fp[1] + fields_out] < 10):
                pm.append([fp[0], fp[1] + fields_out])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    # DOWN
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[1] - fields_out <= 7:
            if bm[fp[0]][fp[1] - fields_out] == 0:
                pm.append([fp[0], fp[1] - fields_out])
            elif (iw and bm[fp[0]][fp[1] - fields_out] > 10) or (
                    not iw and bm[fp[0]][fp[1] - fields_out] < 10):
                pm.append([fp[0], fp[1] - fields_out])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    return pm


def knight_moves(bm, fp, iw):
    pm = []
    for i, j in [[-1, 2], [1, 2], [2, -1], [2, 1], [-1, -2], [1, -2], [-2, -1], [-2, 1]]:
        if 0 <= fp[0] + i <= 7 and 0 <= fp[1] + j <= 7:
            if (iw and bm[fp[0] + i][fp[1] + j] > 10) or (not iw and bm[fp[0] + i][fp[1] + j] < 10) or bm[fp[0] + i][
                fp[1] + j] == 0:
                pm.append([fp[0] + i, fp[1] + j])
    return pm


def bishop_moves(bm, fp, iw):
    pm = []
    # ++
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[0] + fields_out <= 7 and 0 <= fp[1] + fields_out <= 7:
            if bm[fp[0] + fields_out][fp[1] + fields_out] == 0:
                pm.append([fp[0] + fields_out, fp[1] + fields_out])
            elif (iw and bm[fp[0] + fields_out][fp[1] + fields_out] > 10) or (
                    not iw and bm[fp[0] + fields_out][fp[1] + fields_out] < 10):
                pm.append([fp[0] + fields_out, fp[1] + fields_out])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    # -+
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[0] - fields_out <= 7 and 0 <= fp[1] + fields_out <= 7:
            if bm[fp[0] - fields_out][fp[1] + fields_out] == 0:
                pm.append([fp[0] - fields_out, fp[1] + fields_out])
            elif (iw and bm[fp[0] - fields_out][fp[1] + fields_out] > 10) or (
                    not iw and bm[fp[0] - fields_out][fp[1] + fields_out] < 10):
                pm.append([fp[0] - fields_out, fp[1] + fields_out])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    # +-
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[0] + fields_out <= 7 and 0 <= fp[1] - fields_out <= 7:
            if bm[fp[0] + fields_out][fp[1] - fields_out] == 0:
                pm.append([fp[0] + fields_out, fp[1] - fields_out])
            elif (iw and bm[fp[0] + fields_out][fp[1] - fields_out] > 10) or (
                    not iw and bm[fp[0] + fields_out][fp[1] - fields_out] < 10):
                pm.append([fp[0] + fields_out, fp[1] - fields_out])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    # --
    unobstructed = True
    fields_out = 1
    while unobstructed:
        if 0 <= fp[0] - fields_out <= 7 and 0 <= fp[1] - fields_out <= 7:
            if bm[fp[0] - fields_out][fp[1] - fields_out] == 0:
                pm.append([fp[0] - fields_out, fp[1] - fields_out])
            elif (iw and bm[fp[0] - fields_out][fp[1] - fields_out] > 10) or (
                    not iw and bm[fp[0] - fields_out][fp[1] - fields_out] < 10):
                pm.append([fp[0] - fields_out, fp[1] - fields_out])
                unobstructed = False
            else:
                unobstructed = False
        else:
            unobstructed = False
        fields_out += 1
    return pm


def king_moves(bm, fp, iw):
    pm = []
    for i, j in [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]:
        if 0 <= fp[0] + i <= 7 and 0 <= fp[1] + j <= 7:
            if bm[fp[0] + i][fp[1] + j] == 0:
                pm.append([fp[0] + i, fp[1] + j])
            elif (iw and bm[fp[0] + i][fp[1] + j] > 10) or (not iw and bm[fp[0] + i][fp[1] + j] < 10):
                pm.append([fp[0] + i, fp[1] + j])
    return pm


def queen_moves(bm, fp, iw):
    return rook_moves(bm, fp, iw) + bishop_moves(bm, fp, iw)
