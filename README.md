# iDensify v0.1.0
**maintained by:** hkdb \<<hkdb@3df.io>\><br />

## Description

A GTK+ GUI Application written in Python that simplifies compressing PDF files with Ghostscript written for OS X

based on [Densify](https://github.com/hkdb/Densify)

## Change Log

#### MAY 25th, 2018 - v0.1.0 Released

- Birth of iDensify

## Screenshots

![Screenshot2](https://osi.3df.io/wp-content/uploads/2018/05/iDensify2.png)

## Under the Hood

It essentially takes your GUI input and turn them into the following Ghostscript command:

```
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.6 -dPDFSETTINGS=/ebook
-dNOPAUSE -dQUIET -dBATCH -sOutputFile=[compressed.pdf]
"[input.pdf]"
```

## Error Handling

Currently, if any of the below conditions are met, the application will either automatically handle or show an error/warning dialog message that returns to the main window without doing anything upon the user clicking "OK". This is designed to prevent any dangerous execution of Ghostscript. For the ones that are questionable, it will warn the user and provide a chance to cancel or confirm.

Automatically Handles:

- Output file name was not specified, use "compressed.pdf" by default

Shows an Error Dialog Message and Returns to Main Window Upon the User Clicking "OK":

- Input file is not specified
- Input file does not end with .pdf
- Input File and Output File are the same
- Input File Name Contains Unsupported Characters(/\\:;\`)
- Output File Name Contains Unsupported Characters(/\\:;\`)

Questionable Conditions that the application will verify with User via A Dialog Message:

- Output File does not end with .pdf, verify with user that's really what they want
- Output File Name Matches a File in the Output Directory


---

## Beofre Installation

### 1. Download Python
Users are required to have Python3 installed in their machine before using the application.
(Please provide a specific way of installing, either through Terminal/should they consider using bash?)


### 2. Grant access
(Reason behind this move shall be a reasonable move to ease new users without any ideas what they are getting into)
![Allow](https://osi.3df.io/wp-content/uploads/2018/05/MacSecuritySettings.png)

If the option *Anywhere* is missing, open Terminal.app and type in the following command.
![Missing Anywhere Option](https://github.com/ivanoung/iDensify/blob/master/img/nodeveloperoption.png?raw=true)
```
sudo spctl --master-disable
```
User can always revert the operation by entering in the following command.
```
sudo spectl --master-enable
```
![Sample](https://github.com/ivanoung/iDensify/blob/master/img/terminal.png?raw=true)

## Installation

#### Step 1:

Install HomeBrew via Terminal.app if you haven't already:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

#### Step 2:

Install Ghostscript:

```
brew install gs
```

#### Step 3:

Download the latest [DMG - disk image in Mac OS X](https://osi.3df.io/share/iDensify-0.1.0.dmg)
![Download folder](https://github.com/ivanoung/iDensify/blob/master/img/justdownloaded.png?raw=true)


#### Step 4:

Mount disk image by double-clicking onto the .dmg file
![Mounted](https://github.com/ivanoung/iDensify/blob/master/img/afterdoubleclick.png?raw=true)
You should see the disk image mounted under devices

Setp 5: Install App Bundle into Applications Folder 
(I'm not even sure what that means, it was difficult to understand without certain knowledge of what that means)


#### Step 5:
Launch the program by ...

## Building Your Own One File Binary & MacOS Bundle

Dependencies: python3, gi, gtk+3, pygobject3, gs

Run the following inside the cloned directory:

```
python3 -m PyInstaller --clean iDensify.spec
```

## Just Python

You can just run the Python script:

```
python3 iDensify.py
```

---

## Future Plans

- If app is not in foreground, notify user via desktop notification upon completing compression
- Fix Menu Bar Quit - Currently it does nothing
- Better MacOS integration
- More User Friendly Features

## Disclaimer

This application is maintained by volunteers and in no way do the maintainers make any guarantees. Please use at your own risk!

## Recognition

Many thanks to Anthony Wong and Koala Yeung for talking me through this and Dr. Haggen So for sharing the following link that inspired me to write this application:

https://www.tjansson.dk/2012/04/compressing-pdfs-using-ghostscript-under-linux/

This is an application utility sponsored by 3DF Limited's Open Source Initiative.

To Learn more please visit:

https://osi.3df.io

https://www.3df.com.hk

## Want a CLI alternative instead?

Check out [cPDF](https://github.com/hkdb/cpdf), a Python script to simplify compress PDF file size with GhostScript

## What about Linux?

Check out [Densify](https://github.com/hkdb/Densify), the original PDF compressor written for Linux which iDensify is based on
