def ip_neighbors(ix0, bad_px_list):
    """Finds the indices of the nearest neighbor pixels.

    Given an index, f.ex. [9, 7], we want to find all neighboring pixels.:

    [ 8, 6]  [ 8, 7] | Out of bounds 
    [ 9, 6]  [ 9, 7] | Out of bounds
    [10, 6]  [10, 7] | Out of bounds

    I.e. ip_neighbors([9, 7], ...) =  [[8, 6], [8, 7], [9, 6], [10, 6], [10, 7]]

    for [0, 0] we would have:  

    [0, 0] [0, 1]  
    [1, 0] [1, 1]

    ip_neighbors([0, 0], None) = [[0, 1], [1, 0], [1, 1]]

    Another situation where bad_px_list = [[9, 7], [16, 2],  [16, 3], [18, 7], [19, 0],
    [19, 1], [19, 2], [20, 3], [23, 5]]

    We should get
    >>> res = ip_neighbors(bad_px_list[5], bad_px_list)
    >>> res                                                                                                                                                                                                                                                                                                                           
    [[18, 0], [18, 1], [18, 2], [20, 0], [20, 1], [20, 2]]

   
    """
    # List of pixels in the row above
    row_up = [[ix0[0] - 1, rr] for rr in [ix0[1] -1, ix0[1], ix0[1] + 1]]
    # List of pixels in the same row
    row_mid = [[ix0[0], ix0[1] - 1], [ix0[0], ix0[1] + 1]]
    # List of pixels in the row below
    row_lo = [[ix0[0] + 1, rr] for rr in [ix0[1] -1, ix0[1], ix0[1] + 1]]

    all_neighbors = row_up + row_mid + row_lo

    # Next, filter the neighbors for out-of-bounds values
    all_neighbors = list(filter(lambda ix: ix[0] not in [-1, 24], all_neighbors))
    all_neighbors = list(filter(lambda ix: ix[1] not in [-1, 8], all_neighbors))
    # Finally, filter out values from bad pixels.
    all_neighbors = list(filter(lambda ix: ix not in bad_px_list, all_neighbors))

    return all_neighbors

#  bad_px_list = [list(ix) for ix in np.argwhere(bad_channels)]


