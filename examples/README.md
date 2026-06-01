# Collection of Pens

Examples are pulled from the authors' repos' `README.md`

## FontPens

[Original Repo](https://github.com/robotools/fontPens)

[FontPens - Gustavo Ferreira's Fork](https://github.com/gferreira/fontPens/tree/master)

`PrintPen`

`DigestPointPen`

`DigestPointStructurePen`

`FlattenPen`

`SamplingPen`

`SplitPen`

`SpikePen`

`JitterPen`

`DotPen`

`DashPen`

`PerlinPen`

`TranslationPen`

`OutlinePen`


## PenBallWizard

[RoboDocs' Fork](https://github.com/roboDocs/PenBallWizard)


##### Single filter

![alt tag](https://github.com/roboDocs/PenBallWizard/tree/master/source/html/images/penBallWizard-1.png)
![alt tag](https://github.com/roboDocs/PenBallWizard/tree/master/source/html/images/penBallWizard-2.png)

##### Operations filter

Filters can be defined as a succession of filters and/or boolean operations:

![alt tag](https://github.com/roboDocs/PenBallWizard/tree/master/source/html/images/penBallWizard-3.png)
![alt tag](https://github.com/roboDocs/PenBallWizard/tree/master/source/html/images/penBallWizard-4.png)

When defining an operation, you call existing single filters by name and you have a couple of options for each filter in the process. By default, at each step, the glyph is filtered and returned to be passed to the next filter. The ```mode``` option allows you to define how the glyph is passed on to the next step.

Here are the possible arguments for the *mode* option:

- `add`: add filtered glyph on top of the existing glyph instead of filtering the existing
- `union`, `intersection`, `difference`: see [BooleanOperations]

[BooleanOperations]: http://robofont.com/documentation/building-tools/toolkit/boolean-glyphmath/

![alt tag](https://github.com/roboDocs/PenBallWizard/tree/master/source/html/images/penBallWizard-5.png)
![alt tag](https://github.com/roboDocs/PenBallWizard/tree/master/source/html/images/penBallWizard-6.png)

The `source` value is used to changed the source glyph, possibly at each step if you feel like it. If the cell remains empty, each operation receives the previously filtered glyph. However, you can change that by providing either layer names or numbers that correspond to previous steps. It allows you to either use the original glyph by asking for `'foreground'`, but you can also get glyphs from other layers of the initial glyph or a specific filtered glyph.
This functionality makes it easy to create a filter that is only a succession of boolean operations between layers, for instance.

In an operation, you don’t necessarily need to call an existing filter. If at some step you simply wish to duplicate the existing glyph and only perform a boolean operation with it for instance, you can leave the `filterName` field empty or fill it with `'copy'`.
