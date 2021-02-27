# -*- coding: utf-8 -*-
from tkinter import *
from ToolTip.ToolTip import ToolTip


####################################################################################################
###
###     Canvas Text Widget Text Editor
###
###        This class allows the user to click on and edit the displayed text
###     for basic widgets in a canvas. Mainly intended for the create_text
###     widget
###
###     Author:  Chad Unterschultz
###
###     V 1.0.0    Jan 28, 2021  First stable release
###     V 1.0.1    Feb 8,  2021  add = '+' ensures event handlers do not replace one another



debugging = False
VERSION     = (1,0,1)
VERSION_s   = "%s.%s.%s" %VERSION
DATE        = "Day: %s, Month: %s, Year: %s" % (8, "FEb", 2021)

class CanvasTextEdit:
    """ Class to enable user editing of text fields in a Canvas
        Usage: CanvasTextEdit(<Widget>, <Canvas_>, <Root>, <positionX>, <positionY>, <Text>, <tooltipText>)
        <Widget>         = required, Canvas widget whose Text you want to Edit
        <Canvas_>        = required, handle to canvas required to edit text
        <Root>           = required, handle to create entry field
        <positionX>      = optional, not currently used
        <positionY>      = optional, not currently used
        <Text>           = optional, if scrollbar Y-axis
        <tooltipText>    = optional, text to display for edit window tooltip

    """

    Canvas_Items = ["arc", "bitmap", "image", "line", "oval", "polygon",
                    "rectangle", "text", "window"]

    Entry_numberof_Spaces = 20

    def __init__(self, Widget, Canvas_, Root, positionX = 0, positionY = 0, Text = "Default Text", tooltipText = "Enter to finish Editing" ):
        """ CanvasTextTexit initalization, widget, canvas, Root, positionX and position Y are mandatory """

        self.Widget    = None                                                   # Handle to the Text widget in a Canvas that you want to edit
        self.Canvas    = None                                                   # Handle to the Canvas itself
        self.Root      = None                                                   # Handle to the Window itself
        self.positionX = None                                                   # Absolute X position of the Text Widget in the Canvas
        self.positionY = None                                                   # Absolute Y position of the Text Widget in the Canvas
        self.Text      = None                                                   # Text in the
        self.tooltipText = None

        self.Width = None


        self.typetest(Widget, Canvas_, Root, Text, positionX, positionY,
                      tooltipText)                                              # Test the inputs, make sure they are valid
        self.state = 0                                                          # 0 means Display Text, 1 means Edit Text
        self.Canvas.tag_bind(self.Widget, "<Button-1>", self.onLeftClick)       # Mouse click to invoke edit

    def config(self, Widget = None, Canvas_ = None , Root = None, positionX = None, positionY = None, Text = None, tooltipText = None):
        """ configuration of the Canvas Text Widget Edit instance """

        if        Widget == None:                                               # If Widget not updated, assign old as new
            Widget = self.Widget
        if        Canvas_== None:                                               # If Canvas not updated, assign old as new
            Canvas_ = self.Canvas
        if          Root == None:                                               # If Root not updated, assign old as new
            Root = self.Root
        if     positionX == None:                                               # If top left X position of text not updated, assign old as new
            positionX = self.positionX
        if     positionY == None:                                               # If top left Y position of text not updated, assign old as new
            positionY = self.positionY
        if       tooltipText == None:                                           # If Edit tooltip text not updated, assign old as new
            tooltipText = self.tooltipText

        self.typetest(Widget, Canvas_, Root, Text, positionX, positionY,        # Check if the configuration variables are current
                      tooltipText)


        if "entry" in self.__dict__.keys():                                     # In the unlikely event a configuration is invoked while
                                                                                # in the edit  state
            self.entry.delete(0, END)                                           # Delete the Text in the Entry Widget
            self.Root.unbind(self.entry)                                        # unBind the enter button from the Entry Widget
            self.entry.destroy()                                                # Destroy the entry widget
            del self.window                                                     # Delete Handle to Entry Widget Canvas Window
            del self.entry                                                      # Delete Handle to Entry Widget itself

        self.state = 1                                                          # 0 means Display Text, 1 means Edit Text
        self.Canvas.tag_bind(self.Widget, "<Button-1>", self.onLeftClick, add = '+')  # Mouse click to invoke edit

        self.updateText(self)                                                   # Update the ToolTip Text




    def updateText(self):
        """ Update the Text Widget Text """
        self.Canvas.itemconfig(self.Widget, text = self.Text)
        self.Canvas.tkraise(self.Widget)

    def currentText(self):
        """ Return the current Text """
        return self.Text




    def version_info(self):
        """ Current Version Information """
        print(VERSION_s)
        print(DATE)
        pass



    def typetest(self, Widget, Canvas_, Root, Text, positionX, positionY, tooltipText):
        """ Test to make sure the inputs are the correct data type """
        if debugging == True: print("Root.__class__.__name__ != Tk.__name__", Root.__class__.__name__ != Tk.__name__)
        if debugging == True: print("Root.__class__.__name__ != Frame.__name__", Root.__class__.__name__ != Frame.__name__)
        if  ( (Root.__class__.__name__ != Tk.__name__) and
            (Root.__class__.__name__ != Frame.__name__) ) :
            raise TypeError("<Root> must be a Window or a Frame")
        else:
            self.Root = Root

        if debugging == True: print("Root.__class__.__name__ !=  Canvas.__name__",  Root.__class__.__name__ !=  Canvas.__name__)
        if Canvas_.__class__.__name__ !=  Canvas.__name__:
            raise TypeError("<Canvas> must be a Tkinter Canvas type Widget")
        else:
            self.Canvas = Canvas_

        if debugging == True: print(" self.Canvas.type(Widget) not in CanvasTextEdit.Canvas_Items:", self.Canvas.type(Widget),   self.Canvas.type(Widget) not in CanvasTextEdit.Canvas_Items)
        if self.Canvas.type(Widget) not in CanvasTextEdit.Canvas_Items:
            raise TypeError("<Widget> must of a canvas widget")
        else:
            self.Widget = Widget


        if type(Text) != str:
            raise TypeError("<Text> must be of type String")
        else:
            self.Text = Text
        if type(positionX) != int:
            raise TypeError ("<positionX> is not an integer")
        else:
            self.positionX = positionX
        if type(positionY) != int:
            raise TypeError ("<posoitionY> is not an integer")
        else:
            self.positionY = positionY
        if type(tooltipText) != str:
            raise TypeError ("<tooltipText> is not a string")
        else:
            self.tooltipText = tooltipText



    def onLeftClick(self, event):
        """ First Click to edit, then Enter to Finish Editing """
        if self.state == 0:                                                     # State == 0, then enter Edit State


            if debugging == True: print("State 0")

            self.Text = StringVar()

            self.Text = self.Canvas.itemcget(self.Widget, "text")               # Obtain the Text Widget Text

            if debugging == True: print(self.Text)
            if debugging == True: print("Canvas width: ",
                                        self.Canvas.cget("width"))
            if debugging == True: print("Canvas height: ",
                                        self.Canvas.cget("height"))


            self.entry = Entry(self.Root)                                       # Make a Text Entry Widget
            self.entry.config(textvariable = self.Text)



            position = self.Canvas.bbox(self.Widget)                            # Determine the Widget Absolute Position
                                                                                # position = x1, y1, x2, y2
            self.positionX = position[0]                                        # positionX actually self calculated
            self.positionY = position[1]                                        # positionY acually self calculated





                                                                                # how to get Get widget width?




            self.window = self.Canvas.create_window(self.positionX,             # Create a Window, top left corner at the top left
                                                    self.positionY,             # position of the original Canvas Text Widget
                                                    window = self.entry,
                                                    anchor = NW,
                                                    width =  len(self.Text)*5.5 )
            self.Canvas.tkraise(self.window)                                    # Raise the Entry Widget to the Front or Top
            self.entry.focus()                                                  # Bring the Mouse Cursor to the Entry Widget
            self.entry.insert(0,                                                # Insert the Current Text into the Entry Widget
                              self.Text
                              +
                              CanvasTextEdit.Entry_numberof_Spaces*" ")         # Add some extra spaces on the end to ease of entry purpose (not required)
            self.entry.icursor(0)


            self.window_ToolTip = ToolTip(self.entry, self.Root,                # Popup ToolTip giving instructions on how to finish editing
                                          text = "Enter to finish Editing")

            self.state = 1                                                      # Setup of Edit complete, we are now in Edit State
            self.entry.bind("<Return>", self.onLeftClick, add = '+')            # Use Enter to Finish Editing, to exit Entry
            if debugging == True: print("State 0")
            return                                                              # Return to prevent automatically exiting afer entering

        if self.state == 1:                                                     # State == 1, then return to Display State

            if debugging == True: print("State 1")

            self.Text = self.entry.get()                                        # Obtain current text
            self.Text = self.Text.rstrip()
            if debugging == True: print("Numberof characters: ", len(self.Text))


            self.entry.config(width = len(self.Text))

            self.entry.delete(0, END)                                           # Delete text in Entry Widget
            self.Root.unbind(self.entry)                                        # Unbind enter from the Entry Widget
            self.window_ToolTip.canvas_widget_leave()                           # Delete ToolTip, prevent errors
            self.entry.destroy()                                                # Destroy the Entry Widget from the GUI
            self.Canvas.delete(self.window)                                     # Destroy the Entry Widget Window from the GUI

            del self.window                                                     # Delete the Entry Widget Window Handle
            del self.entry                                                      # Delete the Entry Widget Handle

            self.Canvas.itemconfig(self.Widget, text = self.Text)               # Refresh text in the original Text Widget
            self.Canvas.tkraise(self.Widget)                                    # Raise Text forwards to the Top (why isn't it already at the top?)
            self.state = 0                                                      # Enter back into Display State


            if debugging == True: print("State 1")
            return


if __name__ == "__main__":
    Root = Tk()

    Root.focus_set()

    canvas = Canvas(Root, width = 400, height = 400)
    canvas.pack()

    canvasText = canvas.create_text(10, 10, text = "Default Text", anchor = NW)
    canvasTextEdit = CanvasTextEdit(canvasText, canvas, Root, 10, 10)
    canvasTextToolTip = ToolTip(canvasText, Root, canvas, text = "Left click to Edit")
    canvasTextEditToolTip = ToolTip(canvasTextEdit, Root, canvas, text = "Enter to Finish Editing")


    Root.mainloop()






