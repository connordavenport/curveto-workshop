from fontTools.pens.basePen import BasePen
from fontTools.pens.recordingPen import RecordingPen
from fontPens.penTools import interpolatePoint
from fontPens.flattenPen import FlattenPen
import math

class CurvePen(BasePen):

    def __init__(self, other_pen, filterDoubles=True):
        BasePen.__init__(self, {})
        self.other_pen = other_pen
        self.currentPt = None
        self.firstPt = None

    def _moveTo(self, pt):
        self.other_pen.moveTo(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        if pt == self.currentPt:
            return
        oc1 = interpolatePoint(self.currentPt, pt, (1/3))
        oc2 = interpolatePoint(self.currentPt, pt, (2/3))
        self.other_pen.curveTo(oc1, oc2, pt)
        self.currentPt = pt
        return

    def _curveToOne(self, pt1, pt2, pt3):
        self.other_pen.curveTo(pt1, pt2, pt3)
        self.currentPt = pt3

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.other_pen.closePath()
        self.currentPt = None

    def _endPath(self):
        self.other_pen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.other_pen.addComponent(glyphName, transformation)


class MetaPen(BasePen):

    def __init__(self, other_pen, filterDoubles=True):
        BasePen.__init__(self, {})
        self.other_pen = other_pen
        self.currentPt = None
        self.firstPt = None

    def _moveTo(self, pt):
        self.oncurves = []
        self.offcurves = []

        self.other_pen.moveTo(pt)
        self.oncurves.append(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        if pt == self.currentPt:
            return
        self.other_pen.lineTo(pt)
        self.oncurves.append(pt)
        self.currentPt = pt
        return

    def _curveToOne(self, pt1, pt2, pt3):
        self.other_pen.curveTo(pt1, pt2, pt3)
        self.oncurves.append(pt3)
        self.offcurves.extend([pt1,pt2])
        self.currentPt = pt3

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.other_pen.closePath()
        for on in self.oncurves:
            self.circle(on, 15)
        for off in self.offcurves:
            self.circle(off, 7)
        self.currentPt = None

    def circle(self, pos, radius, roundness=0.55):
        cx, cy = pos
        r = radius
        self.other_pen.moveTo((cx+r, cy))
        self.other_pen.curveTo((cx+r, cy+(r*roundness)), (cx+(r*roundness), cy+r), (cx, cy+r))
        self.other_pen.curveTo((cx-(r*roundness), cy+r), (cx-r, cy+(r*roundness)), (cx-r, cy))
        self.other_pen.curveTo((cx-r, cy-(r*roundness)), (cx-(r*roundness), cy-r), (cx, cy-r))
        self.other_pen.curveTo((cx+(r*roundness), cy-r), (cx+r, cy-(r*roundness)), (cx+r, cy))
        self.other_pen.closePath()

    def _endPath(self):
        self.other_pen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.other_pen.addComponent(glyphName, transformation)



class MutatorPen(BasePen):

    def __init__(self, other_pen, other_glyph, factor=0.5):
        BasePen.__init__(self, {})

        r = RecordingPen()
        other_glyph.draw(r)
        self.other_points = r.value
        self.other_pen = other_pen
        self.factor = factor
        self.currentPt = None
        self.index = 0

    def getOther(self):
        return self.other_points[self.index]

    def _moveTo(self, pt):
        self.currentPt = pt
        opt = self.getOther()[1]
        oc1 = interpolatePoint(self.currentPt, opt[0], self.factor)
        self.other_pen.moveTo(oc1)
        self.index += 1

    def _lineTo(self, pt):
        if pt == self.currentPt:
            return
        self.currentPt = pt
        opt = self.getOther()[1]
        oc1 = interpolatePoint(self.currentPt, opt[0], self.factor)
        self.other_pen.lineTo(oc1)
        self.index += 1

    def _curveToOne(self, pt1, pt2, pt3):
        opt = self.getOther()[1]
        oc1 = interpolatePoint(pt1, opt[0], self.factor)
        oc2 = interpolatePoint(pt2, opt[1], self.factor)
        oc3 = interpolatePoint(pt3, opt[2], self.factor)
        self.other_pen.curveTo(oc1, oc2, oc3)
        self.index += 1
        self.currentPt = pt3

    def _closePath(self):
        self.other_pen.closePath()
        self.currentPt = None
        self.index += 1

    def _endPath(self):
        self.other_pen.endPath()
        self.currentPt = None
        self.index += 1

    def addComponent(self, glyphName, transformation):
        self.other_pen.addComponent(glyphName, transformation)



class CheckInterpolatablePen(BasePen):

    def __init__(self, other_pen, other_glyph, factor=0.5):
        BasePen.__init__(self, {})
        r = RecordingPen()
        other_glyph.draw(r)
        self.other_points = r.value
        self.other_pen = other_pen
        self.factor = factor
        self.currentPt = None
        self.index = 0
        self._checks = []

    @property
    def other(self):
        try:
            return self.other_points[self.index]
        except IndexError:
            return

    @property
    def isInterpolatable(self):
        if list(set(self._checks)) == [True]:
            return True
        else:
            return False

    def _moveTo(self, pt):
        opt = self.other
        if not opt:
            self._checks.append(False)
            return
        p = True if opt[0] == "moveTo" else False
        self._checks.append(p)
        self.index += 1

    def _lineTo(self, pt):
        opt = self.other
        if not opt:
            self._checks.append(False)
            return
        p = True if opt[0] == "lineTo" else False
        self._checks.append(p)
        self.index += 1

    def _curveToOne(self, pt1, pt2, pt3):
        opt = self.other
        if not opt:
            self._checks.append(False)
            return
        p = True if opt[0] == "curveTo" else False
        self._checks.append(p)
        self.index += 1

    def _closePath(self):
        opt = self.other
        if not opt:
            self._checks.append(False)
            return
        p = True if opt[0] == "closePath" else False
        self._checks.append(p)
        self.index += 1

    def _endPath(self):
        opt = self.other
        if not opt:
            self._checks.append(False)
            return
        p = True if opt[0] == "endPath" else False
        self._checks.append(p)
        self.index += 1

    def addComponent(self, glyphName, transformation):
        self.other_pen.addComponent(glyphName, transformation)



g = CurrentGlyph()
with g.undo():
    r = RecordingPen()
    filterpen = MutatorPen(r, AllFonts()[1][g.name])
    g.draw(filterpen)
    # print(r.value)
    g.clearContours()
    r.replay(g.getPen())

