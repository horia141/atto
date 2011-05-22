class RelPos(object):
    def __init__(self,row,col):
        self.__row = row
        self.__col = col

    def __str__(self):
        return str(self.__row) + 'x' + \
               str(self.__col)

    def __repr__(self):
        return 'RelPos(' + \
                 repr(self.__row) + ',' + \
                 repr(self.__col) + ')'

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

class Geometry(object):
    def __init__(self,abs_beg,rel_beg,abs_end,rel_end):
        self.__abs_beg = abs_beg
        self.__rel_beg = rel_beg
        self.__abs_end = abs_end
        self.__rel_end = rel_end

    def __str__(self):
        return str(self.__abs_beg) + ':' + \
               str(self.__rel_beg) + '//' + \
               str(self.__abs_end) + ':' + \
               str(self.__rel_end)

    def __repr__(self):
        return 'Geometry(' + \
                 repr(self.__abs_beg) + ',' + \
                 repr(self.__rel_beg) + ',' + \
                 repr(self.__abs_end) + ',' + \
                 repr(self.__rel_end) + ')'

    @property
    def absBeg(self):
        return self.__abs_beg

    @property
    def relBeg(self):
        return self.__rel_beg

    @property
    def absEnd(self):
        return self.__abs_end

    @property
    def relEnd(self):
        return self.__rel_end

class Buffer(object):
    def __init__(self,basic_stream):
        self.__basic_stream = basic_stream
        self.__curr_pos = 0

    def tryConsume(self,reobject,group=0):
        m = reobject.match(self.__basic_stream,self.__curr_pos)

        if m:
            abs_pos = self.absPos
            rel_pos = self.relPos
            self.__curr_pos = m.end()
            geom = Geometry(abs_pos,rel_pos,self.absPos,self.relPos)
            return (m.group(group),geom)
        else:
            return None

    def isFinished(self):
        return self.__curr_pos == len(self.__basic_stream)

    def abs2RelPos(self,absPos):
        cAbs = 0
        cRow = 0
        cCol = 0

        while cAbs < absPos:
            if self.__basic_stream[cAbs] == '\n':
                cRow = cRow + 1
                cCol = 0
            else:
                cCol = cCol + 1

            cAbs = cAbs + 1

        return RelPos(cRow,cCol)

    @property
    def absPos(self):
        return self.__curr_pos

    @property
    def relPos(self):
        return self.abs2RelPos(self.__curr_pos)
