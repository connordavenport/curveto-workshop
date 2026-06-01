## AbstractPen -> BasePen

class AbstractPen:
    def moveTo(self, pt: Tuple[float, float]) -> None:
        raise NotImplementedError

    def lineTo(self, pt: Tuple[float, float]) -> None:
        raise NotImplementedError

    def curveTo(self, *points: Tuple[float, float]) -> None:
        raise NotImplementedError

    def qCurveTo(self, *points: Tuple[float, float]) -> None:
        raise NotImplementedError

    def closePath(self) -> None:
        pass

    def endPath(self) -> None:
        pass

    def addComponent(
        self,
        glyphName: str,
        transformation: Tuple[float, float, float, float, float, float],
    ) -> None:
        raise NotImplementedError



class BasePen(DecomposingPen):

    def __init__(self, glyphSet=None):
        super(BasePen, self).__init__(glyphSet)
        self.__currentPoint = None

    def _moveTo(self, pt):  # MUST OVERRIDE
        raise NotImplementedError 

    def _lineTo(self, pt):  # MUST OVERRIDE
        raise NotImplementedError 

    def _curveToOne(self, pt1, pt2, pt3):  # MUST OVERRIDE
        raise NotImplementedError 

    def _closePath(self):  # MAY OVERRIDE
        pass

    def _endPath(self):  # MAY OVERRIDE
        pass

    def _qCurveToOne(self, pt1, pt2):  # MAY OVERRIDE
        pt0x, pt0y = self.__currentPoint
        pt1x, pt1y = pt1
        pt2x, pt2y = pt2
        mid1x = pt0x + 0.66666666666666667 * (pt1x - pt0x)
        mid1y = pt0y + 0.66666666666666667 * (pt1y - pt0y)
        mid2x = pt2x + 0.66666666666666667 * (pt1x - pt2x)
        mid2y = pt2y + 0.66666666666666667 * (pt1y - pt2y)
        self._curveToOne((mid1x, mid1y), (mid2x, mid2y), pt2)

    def _getCurrentPoint(self):  # DON'T OVERRIDE
        return self.__currentPoint

    def closePath(self):  # DON'T OVERRIDE
        self._closePath()
        self.__currentPoint = None

    def endPath(self):  # DON'T OVERRIDE
        self._endPath()
        self.__currentPoint = None

    def moveTo(self, pt):  # DON'T OVERRIDE
        self._moveTo(pt)
        self.__currentPoint = pt

    def lineTo(self, pt):  # DON'T OVERRIDE
        self._lineTo(pt)
        self.__currentPoint = pt

    def curveTo(self, *points):  # DON'T OVERRIDE
        n = len(points) - 1
        assert n >= 0
        if n == 2:
            self._curveToOne(*points)
            self.__currentPoint = points[-1]
        elif n > 2:
            _curveToOne = self._curveToOne
            for pt1, pt2, pt3 in decomposeSuperBezierSegment(points):
                _curveToOne(pt1, pt2, pt3)
                self.__currentPoint = pt3
        elif n == 1:
            self.qCurveTo(*points)
        elif n == 0:
            self.lineTo(points[0])
        else:
            raise AssertionError("can't get there from here")

    def qCurveTo(self, *points):  # DON'T OVERRIDE
        n = len(points) - 1
        assert n >= 0
        if points[-1] is None:
            x, y = points[-2]
            nx, ny = points[0]
            impliedStartPoint = (0.5 * (x + nx), 0.5 * (y + ny))
            self.__currentPoint = impliedStartPoint
            self._moveTo(impliedStartPoint)
            points = points[:-1] + (impliedStartPoint,)
        if n > 0:
            _qCurveToOne = self._qCurveToOne
            for pt1, pt2 in decomposeQuadraticSegment(points):
                _qCurveToOne(pt1, pt2)
                self.__currentPoint = pt2
        else:
            self.lineTo(points[0])



# example implimentation

class RecordingPen(AbstractPen):

    def __init__(self):
        self.value = []

    def moveTo(self, p0):
        self.value.append(("moveTo", (p0,)))

    def lineTo(self, p1):
        self.value.append(("lineTo", (p1,)))

    def qCurveTo(self, *points):
        self.value.append(("qCurveTo", points))

    def curveTo(self, *points):
        self.value.append(("curveTo", points))

    def closePath(self):
        self.value.append(("closePath", ()))

    def endPath(self):
        self.value.append(("endPath", ()))

    def addComponent(self, glyphName, transformation):
        self.value.append(("addComponent", (glyphName, transformation)))

    def replay(self, pen):
        replayRecording(self.value, pen)

    draw = replay


# process a pen the sloppy way

glyph = CurrentGlyph()
with glyph.undo():
    g = RGlyph()
    p = g.getPen()
    pen = FlattenPen(p, approximateSegmentLength=60)
    glyph.draw(pen)
    glyph.clear()
    glyph.appendGlyph(g)

"""
filter_pen  dummy_glyph     glyph
   |            |             |      
   |        dg.getPen()       |          
   |            |             |      
   |------load dg in pen------|      
                |
            parse glyph
            through pen
                |
        clear existing glyph
                |
        append newly processed
       glyph from pen into glyph
"""
    


# process a pen object the nice way

from fontPens.flattenPen import FlattenPen
from fontTools.pens.recordingPen import *

glyph = CurrentGlyph()
with glyph.undo():
    recorder = RecordingPen() # get a pen object
    filterpen = FlattenPen(recorder, approximateSegmentLength=60)
    glyph.draw(filterpen)
    glyph.clear()
    print(recorder.value) # prints out the pen values
    recorder.replay(glyph.getPen())

"""
recording_pen    glyph
    |              |
filter_pen         |
    |              |
    |-------|------|
            |
       parse glyph
       through pen
            |
            |
    now the recording pen 
    has a stored list of 
    the processed items
            |
    replay will run the
    stored processes
"""