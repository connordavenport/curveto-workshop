from fontTools.pens.basePen import BasePen
from fontTools.pens.recordingPen import RecordingPen
from fontPens.penTools import interpolatePoint

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


g = CurrentGlyph()
with g.undo():
    r = RecordingPen()
    filterpen = CurvePen(r)
    g.draw(filterpen)
    g.clear()
    r.replay(g.getPen())

