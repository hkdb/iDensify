#!/usr/bin/env python

#################################################################
### PROJECT:
### iDensify
### VERSION:
### v0.1.0
### SCRIPT:
### iDensify.py
### DESCRIPTION:
### GTK+ application to easily compress pdf files w/ Ghostscript
### modified for macos
### MAINTAINED BY:
### hkdb <hkdb@3df.io>
### Disclaimer:
### This application is maintained by volunteers and in no way
### do the maintainers make any guarantees. Use at your own risk.
### ##############################################################

import sys
import threading
import subprocess
import traceback
import queue
import os
import re
import webbrowser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class MyWindow(Gtk.Window, threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # Set Window Specification
        Gtk.Window.__init__(self, title="iDensify - PDF Compression")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(450, 300)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=20)
        self.add(self.box)

        # App Logo
        header = self.resource_path("header.png")
        self.image = Gtk.Image()
        self.image.set_from_file(header)
        self.box.pack_start(self.image, True, True, padding=1)

        # App About
        aLabel = Gtk.Label("An Open Source Initiative Sponsored by 3DF")
        aLabel.set_markup("<small>An <a href=\"https://osi.3df.io\"" "title=\"OSI @ 3DF\">OSI</a> application sponsored by <a href=\"https://www.3df.com.hk\"" "title=\"3DF Ltd.\">3DF</a></small>")
        aLabel.connect("activate-link", self.link)
        self.box.pack_start(aLabel, True, True, 0)

        # App Version
        vLabel = Gtk.Label("v0.1.0")
        vLabel.set_justify(Gtk.Justification.CENTER)
        self.box.pack_start(vLabel, True, True, 0)

        # Separator
        bar = Gtk.HSeparator()
        self.box.pack_start(bar, True, True, 0)

        # Specify Input File
        iLabel = Gtk.Label("PDF:", xalign=0)
        self.box.pack_start(iLabel, True, True, 0)
        self.iChooser = Gtk.FileChooserButton()
        self.box.pack_start(self.iChooser, True, True, 0)

        # Separator
        bar1 = Gtk.HSeparator()
        self.box.pack_start(bar1, True, True, 0)

        # Specify Compression Type
        tLabel = Gtk.Label("Type:", xalign=0)
        self.box.pack_start(tLabel, True, True, 0)
        store = Gtk.ListStore(str)
        for item in ["ebook", "screen", "printer", "prepress", "default"]:
            store.append([item])
        self.cType = Gtk.ComboBox()
        self.cType.set_model(store)
        self.cType.set_active(0)
        self.cType.connect("changed", self.on_combobox_changed)
        self.box.pack_start(self.cType, True, True, 0)
        cellrenderertext = Gtk.CellRendererText()
        self.cType.pack_start(cellrenderertext, True)
        self.cType.add_attribute(cellrenderertext, "text", 0)

        # Help Button - Compression Types
        self.help = Gtk.Button(label="?")
        self.help.connect("clicked", self.on_help_clicked)
        self.box.pack_start(self.help, True, True, 0)

        # Separator
        bar2 = Gtk.HSeparator()
        self.box.pack_start(bar2, True, True, 0)

        # Specify Output File
        oLabel = Gtk.Label("Output:", xalign=0)
        self.box.pack_start(oLabel, True, True, 0)
        self.oFile = Gtk.Entry()
        self.oFile.set_placeholder_text("compressed.pdf")
        self.box.pack_start(self.oFile, True, True, 0)

        # Help Button - Output File
        self.oHelp = Gtk.Button(label="?")
        self.oHelp.connect("clicked", self.on_oHelp_clicked)
        self.box.pack_start(self.oHelp, True, True, 0)

        # Separator
        bar3 = Gtk.HSeparator()
        self.box.pack_start(bar3, True, True, 0)

        # Progress Bar
        pLabel = Gtk.Label("Status:", xalign=0)
        self.box.pack_start(pLabel, True, True, 0)
        self.progressbar = Gtk.ProgressBar()
        self.box.pack_start(self.progressbar, True, True, 1)
        show_text = True
        text = "Ready"
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)
        self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)
        self.activity_mode = False

        # Separator
        bar4 = Gtk.HSeparator()
        self.box.pack_start(bar4, True, True, 0)

        # Toggle Compress
        self.button = Gtk.Button(label="Compress Now!")
        self.button.set_sensitive(True)
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

    # ComboBox Handler
    def on_combobox_changed(self, combobox):
        treeiter = combobox.get_active_iter()
        model = combobox.get_model()

    # Help Button Handler
    def on_help_clicked(self, widget):
        # Show Compression Type Descriptions Help Dialog
        verbiage = "\n\n\nscreen:\n\nselects low-resolution output similar to the Acrobat Distiller \"Screen Optimized\" setting.\n\n\nebook:\n\nselects medium-resolution output similar to the Acrobat Distiller \"eBook\" setting.\n\n\nprinter:\n\nselects output similar to the Acrobat Distiller \"Print Optimized\" setting.\n\n\nprepress:\n\nselects output similar to Acrobat Distiller \"Prepress Optimized\" setting.\n\n\ndefault:\n\nselects output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file."
        self.info("Types of Compression", verbiage)

    # oHelp Button Handler
    def on_oHelp_clicked(self, widget):
        # Show Output File Help Dialog
        verbiage = "The output filename must not be the same as the input file name. The compressed PDF file will be placed in the same folder as your input file folder."
        self.info("Output File Name", verbiage)

    # Compression Button Handler - Where all the magic happens
    def on_button_clicked(self, widget):
        # Disable Compress Button
        self.button.set_sensitive(False)
        # Set Progress Bar Text to "Completed" and Progress Bar to Pulse
        self.progress()

        # Set Command Compression Type Variable
        iFile = self.iChooser.get_filename()
        slash = "/"
        oName = self.oFile.get_text()

        # If Output file name was not specified, use "compressed.pdf"
        if oName == None or oName == "":
            oName = "compressed.pdf"

        # If Input file is not specified, show an error dialog box
        if iFile == None:
            # Show Error Dialog
            verbiage = "The input file field is empty. Please specify an input file to compress..."
            self.warning("ERROR!", verbiage)
            # Set Progress Bar Text to "Ready"
            self.ready()
            # Enable Compress Button
            self.button.set_sensitive(True)

            return 1

        # If Input file does not end with .pdf, show an error dialog box
        if not iFile.endswith(".pdf"):
            # Show Error Dialog
            verbiage = "Only PDF files can be compressed with this application. Please specify a pdf file"
            self.warning("ERROR!", verbiage)
            # Set Progress Bar Text to "Ready"
            self.ready()
            # Enable Compress Button
            self.button.set_sensitive(True)

            return 1

        # Prep Type of Compression - Must happen before comparing iFile and oFile
        if iFile != None:
            iPath = os.path.dirname(os.path.realpath(iFile))
            oFile = iPath + slash + oName

        # If the Input File and Output File are the same, show an error dialog box
        if iFile == oFile:
            # Show Error Dialog
            verbiage = "The output file name cannot be the same as the input file name."
            self.warning("ERROR!", verbiage)
            # Set Progress Bar Text to "Ready"
            self.ready()
            # Enable Compress Button
            self.button.set_sensitive(True)

            return 1

        # If Output File does not end with .pdf, verify with user that's really what they want
        if not oFile.endswith(".pdf"):
            verbiage = "The output file name you specified does not end with \".pdf\". Are you sure that's what you want?"
            response = self.verify("Output file name does not end with \".pdf\"!", verbiage)

            # If OK, then continue to overwrite existing file. If cancel, then stop and go back to main window
            if response == Gtk.ResponseType.CANCEL:
                self.ready()
                # Enable Compress Button
                self.button.set_sensitive(True)

                return 1

        # Turn iFile to String to Prepare for Next Condition
        iName = str(os.path.basename(iFile))

        # If Specified Input File Name Contains Unsupported Characters, Show Dialog Error Dialog Box and Return to Main Window
        # Security Procaution
        if re.search('[\\\\\|:;\`]', iName):
            verbiage = "The input file name contains unsupported characters. Please ensure your input file name does not contain special characters / \\ : ; \`"
            self.warning("Unsupported File Name Convention!", verbiage)
            self.button.set_sensitive(True)

            return 1

        # If Specified Output File Name Contains Unsupported Characters, Show Dialog Error Dialog Box and Return to Main Window
        # Security Procaution
        if re.search('[\\\\\|:;\`]', oName):
            verbiage = "The output file name contains unsupported characters. Please ensure your output file name does not contain special characters / \\ : ; \`"
            self.warning("Unsupported File Name Convention!", verbiage)
            self.button.set_sensitive(True)

            return 1

        # If Specified Output File Name Matches a File in the Output Directory
        if os.path.isfile(oFile):
            # Show Error Dialog
            verbiage = "There's a file with the same name, \"" + oName + "\" already in the directory. Are you sure you want to overwrite?"
            response = self.verify("WARNING!", verbiage)

            # If OK, then continue to overwrite existing file. If cancel, then stop and go back to main window
            if response == Gtk.ResponseType.CANCEL:
                self.ready()
                # Enable Compress Button
                self.button.set_sensitive(True)

                return 1

        # Set Compression Type
        cTypeIter = self.cType.get_active_iter()
        cTypeModel = self.cType.get_model()
        cType = cTypeModel[cTypeIter][0]

        # Build gs Command
        self.cmmd = 'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.6 -dPDFSETTINGS=/' + cType + ' -dNOPAUSE -dQUIET -dBATCH -sOutputFile=' + "\"" + oFile + "\"" + ' ' + "\"" +iFile + "\""

        # Start Compressing
        q = queue.Queue()
        cnow = threading.Thread(target=self.compress, args=[q])
        cnow.start()
        # Keep Progress Bar Active
        while cnow.isAlive():
            Gtk.main_iteration_do(False)

        # Don't continue until thread is finished
        cnow.join(timeout=4)

        # Setup Queue to get try catch results
        success = q.get()

        # If try succeeds, tell user it succeeded, else, show an error dialog
        if success == True:
            # Get File Size
            iFileSizeRaw = os.path.getsize(iFile)
            oFileSizeRaw = os.path.getsize(oFile)

            # Determine to Display File Size in MB or KB +- 10MB
            if iFileSizeRaw < 10000000:
                iFileSize = iFileSizeRaw >> 10
                iUnit = "KB"
            else:
                iFileSize = iFileSizeRaw >> 20
                iUnit = "MB"

            if oFileSizeRaw < 10000000:
                oFileSize = oFileSizeRaw >> 10
                oUnit = "KB"
            else:
                oFileSize = oFileSizeRaw >> 20
                oUnit = "MB"

            # Set Progress Bar to Completed and Stop Pulsing
            self.completed()

            # Show Completion Dialog - Try Completed
            verbiage = "Your PDF File has been successfully compressed from " + str(iFileSize) + iUnit + " to " + str(oFileSize) + oUnit + "! Enjoy!"
            self.info("PDF Compressed!", verbiage)

        else:
            # Show Error Dialog - Exception
            verbiage = "Something went wrong! Maybe your PDF file is corrupted?"
            self.info("ERROR!", verbiage)
            # Set Progress Bar to Ready and Stop Pulsing
            self.ready()

    # Informational Dialog Message
    def info(self, title, verbiage):
        # Show Info Dialog
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(verbiage)
        response = dialog.run()
        dialog.destroy()

    # Warning Dialog Message
    def warning(self, title, verbiage):
        # Pause Compression Progress Bar
        self.pause()
        # Show Error Dialog
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(verbiage)
        response = dialog.run()
        dialog.destroy()

    # Verify What to Do Dialog Message
    def verify(self, title, verbiage):
        # Pause Compression Progress Bar
        self.pause()
        # Show Error Dialog
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, title)
        dialog.format_secondary_text(verbiage)
        response = dialog.run()
        dialog.destroy()
        # Resume Compression Progress Bar & Continue
        self.resume()

        return response

    # Set Progress Bar Text to "Compressing..." and Progress Bar to Pulse
    def progress(self):
        show_text = True
        text = "Compressing..."
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)
        self.activity_mode = True
        self.progressbar.pulse()

    # Set Progress Bar Text to "Ready" and Progress Bar to Stop
    def ready(self):
        show_text = True
        text = "Ready"
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)
        self.activity_mode = False
        self.progressbar.set_fraction(0.0)
        # Enable Compress Button
        self.button.set_sensitive(True)

    # Set Progress Bar Text to "Puased" and Progress Bar to Stop
    def pause(self):
        show_text = True
        text = "Paused"
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)
        self.activity_mode = False
        self.progressbar.set_fraction(0.0)

    # Set Progress Bar Text to "Compressing..." and Progress Bar to Resume
    def resume(self):
        show_text = True
        text = "Compressing..."
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)
        self.activity_mode = True
        self.progressbar.pulse()

    # Set Progress Bar Text to "Completed" and Progress Bar to Stop
    def completed(self):
        show_text = True
        text = "Completed"
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)
        self.activity_mode = False
        self.progressbar.set_fraction(0.0)
        # Enable Compress Button
        self.button.set_sensitive(True)

    # Compression Function to execute gs as SubProcess to be Called on a Separate Thread
    def compress(self, out_queue):
        try:
            process = subprocess.Popen(self.cmmd, shell=True, stdout=subprocess.PIPE)
            out, err = process.communicate()
            out_queue.put(True)
        except:
            if err == None:
                print("There's an error with no trace data...")
            else:
                print(err)
            out_queue.put(False)

    # Progress Bar Status Handler
    def on_timeout(self, user_data):

        # Update value on the progress bar
        if self.activity_mode:
            self.progressbar.pulse()
        else:
            new_value = self.progressbar.get_fraction()

            if new_value > 1:
                new_value = 0

            self.progressbar.set_fraction(new_value)

        # As this is a timeout function, return True so that it
        # continues to get called
        return True

    # Open WebBrowser for Links
    def link(self, widget, url):
        webbrowser.open(url)

    # Get Absolute Path of the Temp Work Directory
    def resource_path(self, relative_path):

        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

# Initiate Window
win = MyWindow()
win.start()
# win.set_icon_from_file("icon.icns") # Set App Icon
win.connect("destroy", Gtk.main_quit)
win.show_all()
# Bring to Front on Launch
win.set_keep_above(True)
# Allow to be backgrounded
win.set_keep_above(False)
Gtk.main()
