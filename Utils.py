class TextGeometry(object):
    def __init__(self,abs_beg,abs_end,
                 rel_beg_row,rel_beg_col,
                 rel_end_row,rel_end_col):
        self.abs_beg = abs_beg
        self.abs_end = abs_end
        self.rel_beg_row = rel_beg_row
        self.rel_beg_col = rel_beg_col
        self.rel_end_row = rel_end_row
        self.rel_end_col = rel_end_col

    def __str__(self):
        return str(self.abs_beg) + ':' + str(self.abs_end) + '//' + \
               str(self.rel_beg_row) + 'x' + str(self.rel_beg_col) + ':' + \
               str(self.rel_end_row) + 'x' + str(self.rel_end_col)

    def getAbsBeg(self):
        return self.abs_beg

    def getAbsEnd(self):
        return self.abs_end

    def getRelBeg(self):
        return (self.rel_beg_row,self.rel_beg_col)

    def getRelEnd(self):
        return (self.rel_end_row,self.rel_end_col)
