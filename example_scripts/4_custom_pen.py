from fontTools.pens.basePen import BasePen
from fontTools.pens.recordingPen import RecordingPen
from fontPens.penTools import interpolatePoint
from fontPens.flattenPen import FlattenPen
import math

class CurvePen(BasePen):
    def __init__(self, otherPen, filterDoubles=True):
        BasePen.__init__(self, {})
        self.otherPen = otherPen
        self.currentPt = None
        self.firstPt = None

    def _moveTo(self, pt):
        self.otherPen.moveTo(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        if pt == self.currentPt:
            return
        oc1 = interpolatePoint(self.currentPt, pt, (1/3))
        oc2 = interpolatePoint(self.currentPt, pt, (2/3))
        self.otherPen.curveTo(oc1, oc2, pt)
        self.currentPt = pt
        return

    def _curveToOne(self, pt1, pt2, pt3):
        self.otherPen.curveTo(pt1, pt2, pt3)
        self.currentPt = pt3

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.otherPen.closePath()
        self.currentPt = None

    def _endPath(self):
        self.otherPen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)


class MetaPen(BasePen):
    def __init__(self, otherPen, filterDoubles=True):
        BasePen.__init__(self, {})
        self.otherPen = otherPen
        self.currentPt = None
        self.firstPt = None

    def _moveTo(self, pt):
        self.oncurves = []
        self.offcurves = []

        self.otherPen.moveTo(pt)
        self.oncurves.append(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        if pt == self.currentPt:
            return
        self.otherPen.lineTo(pt)
        self.oncurves.append(pt)
        self.currentPt = pt
        return

    def _curveToOne(self, pt1, pt2, pt3):
        self.otherPen.curveTo(pt1, pt2, pt3)
        self.oncurves.append(pt3)
        self.offcurves.extend([pt1,pt2])
        self.currentPt = pt3

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.otherPen.closePath()
        for on in self.oncurves:
            self.circle(self.otherPen, on, 15)
        for off in self.offcurves:
            self.circle(self.otherPen, off, 7)
        self.currentPt = None

    def circle(self, pos, radius, roundness=0.55):
        cx, cy = pos
        r = radius
        self.otherPen.moveTo((cx+r, cy))
        self.otherPen.curveTo((cx+r, cy+(r*roundness)), (cx+(r*roundness), cy+r), (cx, cy+r))
        self.otherPen.curveTo((cx-(r*roundness), cy+r), (cx-r, cy+(r*roundness)), (cx-r, cy))
        self.otherPen.curveTo((cx-r, cy-(r*roundness)), (cx-(r*roundness), cy-r), (cx, cy-r))
        self.otherPen.curveTo((cx+(r*roundness), cy-r), (cx+r, cy-(r*roundness)), (cx+r, cy))
        self.otherPen.closePath()

    def _endPath(self):
        self.otherPen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)


g = CurrentGlyph()
with g.undo():
    r = RecordingPen()
    filterpen = MetaPen(r)
    g.draw(filterpen)
    g.clearContours()
    r.replay(g.getPen())

