import adsk.core, adsk.fusion

def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    names = {'Body13': 'Draft hinge barrel L - hidden',
             'Body14': 'Draft hinge barrel R - hidden',
             'Lid shell 238.6 x 138.6 x 10.4 mm (1)': 'Draft hinge barrel center - hidden'}
    for i in range(root.bRepBodies.count):
        b = root.bRepBodies.item(i)
        if b.name in names:
            b.isVisible = False
            b.name = names[b.name]
    ui.messageBox('Hidden misoriented draft hinge bodies. The corrected case, lid, three integrated barrels, and corrected pin remain visible.')

def stop(context):
    pass
