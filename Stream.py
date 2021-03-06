class RelPos(object):
    def __init__(self,row,col):
        assert(isinstance(row,int))
        assert(isinstance(col,int))

        self.__row = row
        self.__col = col

    def __str__(self):
        return str(self.__row) + 'x' + \
               str(self.__col)

    def __repr__(self):
        return 'Stream.RelPos(' + \
                 repr(self.__row) + ',' + \
                 repr(self.__col) + ')'

    def clone(self):
        return RelPos(self.__row,self.__col)

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

class Geometry(object):
    def __init__(self,abs_beg,rel_beg,abs_end,rel_end):
        assert(isinstance(abs_beg,int))
        assert(isinstance(rel_beg,RelPos))
        assert(isinstance(abs_end,int))
        assert(isinstance(rel_end,RelPos))

        self.__abs_beg = abs_beg
        self.__rel_beg = rel_beg.clone()
        self.__abs_end = abs_end
        self.__rel_end = rel_end.clone()

    def __str__(self):
        return str(self.__abs_beg) + ':' + \
               str(self.__rel_beg) + '//' + \
               str(self.__abs_end) + ':' + \
               str(self.__rel_end)

    def __repr__(self):
        return 'Stream.Geometry(' + \
                 repr(self.__abs_beg) + ',' + \
                 repr(self.__rel_beg) + ',' + \
                 repr(self.__abs_end) + ',' + \
                 repr(self.__rel_end) + ')'

    def expandTo(self,other_geometry):
        assert(isinstance(other_geometry,Geometry))

        return Geometry(self.__abs_beg,
                        self.__rel_beg,
                        other_geometry.absEnd,
                        other_geometry.relEnd)

    def clone(self):
        return Geometry(self.__abs_beg,self.__rel_beg,
                        self.__abs_end,self.__rel_end)

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
        assert(isinstance(basic_stream,str))

        self.__basic_stream = str(basic_stream)
        self.__abs_pos = 0
        self.__rel_pos = RelPos(0,0)

    def __str__(self):
        return 'Buffer ' + str(self.__abs_pos) + '@' + repr(self.__basic_stream)

    def __repr__(self):
        return 'Stream.Buffer(' + repr(self.__basic_stream) + ')'

    def tryConsume(self,reobject,group=0):
        # assert(isinstance(reobject,_sre.SRE_Pattern))

        m = reobject.match(self.__basic_stream,self.__abs_pos)

        if m:
            abs_pos = self.__abs_pos
            rel_pos = self.__rel_pos
            self.__abs_pos = m.end()
            self.__rel_pos = self.abs2RelPos(self.__abs_pos,abs_pos,rel_pos)
            geom = Geometry(abs_pos,rel_pos,self.__abs_pos,self.__rel_pos)
            return (m.group(group),geom)
        else:
            return None

    def abs2RelPos(self,abs_pos,old_abs_pos=0,old_rel_pos=None):
        assert(isinstance(abs_pos,int))
        assert(isinstance(old_abs_pos,int))
        assert(isinstance(old_rel_pos,RelPos) or old_rel_pos == None)

        c_abs = old_abs_pos
        c_row = old_rel_pos.row if old_rel_pos else 0
        c_col = old_rel_pos.col if old_rel_pos else 0

        while c_abs < abs_pos:
            if self.__basic_stream[c_abs] == '\n':
                c_row = c_row + 1
                c_col = 0
            else:
                c_col = c_col + 1

            c_abs = c_abs + 1

        return RelPos(c_row,c_col)

    def relPos2Abs(self,rel_pos):
        assert(isinstance(rel_pos,RelPos))

        c_abs = 0
        c_row = 0
        c_col = 0

        while c_row < rel_pos.row:
            if c_abs == len(self.__basic_stream) - 1:
                if c_row == rel_pos.row - 1 and rel_pos.col == 0:
                    return len(self.__basic_stream)
                else:
                    raise IndexError('RelPos out of stream bounds (by row)!')

            if self.__basic_stream[c_abs] == '\n':
                c_row = c_row + 1

            c_abs = c_abs + 1

        while c_col < rel_pos.col:
            if c_abs == len(self.__basic_stream) - 1:
                raise IndexError('RelPos out of stream bounds (by col)!')

            if self.__basic_stream[c_abs] == '\n':
                raise IndexError('RelPos does not contain col!')

            c_abs = c_abs + 1
            c_col = c_col + 1

        return c_abs

    def geometry2Frag(self,geometry):
        assert(isinstance(geometry,Geometry))

        return self.__basic_stream[geometry.absBeg:geometry.absEnd]

    def geometry2FragRows(self,geometry):
        assert(isinstance(geometry,Geometry))

        abs_beg = self.relPos2Abs(RelPos(geometry.relBeg.row,0))
        abs_end = self.relPos2Abs(RelPos(geometry.relEnd.row + 1,0))

        return self.__basic_stream[abs_beg:abs_end]

    def clone(self):
        new_buffer = Buffer(self.__basic_stream)
        new_buffer.__abs_pos = self.__abs_pos
        new_buffer.__rel_pos = self.__rel_pos

        return new_buffer

    @property
    def finished(self):
        return self.__abs_pos == len(self.__basic_stream)

    @property
    def absPos(self):
        return self.__abs_pos

    @property
    def relPos(self):
        return self.__rel_pos
