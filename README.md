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

## Installation

Step 1:

Install HomeBrew via Terminal.app if you haven't already:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Step 2:

Install Ghostscript:

```
brew install gs
```

Step 3:

Download the latest [DMG](https://osi.3df.io/share/iDensify-0.1.0.dmg)

Step 4:

Mount DMG & copy App Bundle into your /Applications Folder

Step 5:

Allow Apps Downloaded from Anywhere

![Allow](https://osi.3df.io/wp-content/uploads/2018/05/MacSecuritySettings.png)

If the option *Anywhere* is missing, click on the lock icon to unlock the settings:

![Missing Anywhere Option](https://osi.3df.io/wp-content/uploads/2018/06/nodeveloperoption.png)

If it still does not show, then execute the following command in the terminal:

```
sudo spctl --master-disable
```

To lock the settings back up, execute the following command in the terminal:

```
sudo spectl --master-enable
```

Enjoy!

## Just Python

If this option is chosen, ensure that you already have Python3 installed on your Mac. If not, you can do the following:

Step 1:

Install HomeBrew via Terminal.app if you haven't already:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Step 2:

Install Python3:

```
brew install python3
```

#### Just run the Python script:

```
python3 iDensify.py
```

## Building Your Own One File Binary & MacOS Bundle

Dependencies: python3, gi, gtk+3, pygobject3, gs

Run the following inside the cloned directory:

```
python3 -m PyInstaller --clean iDensify.spec
```

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

Shout out goes to [Ivan Oung](https://github.com/ivanoung) for looking through the readme and suggesting changes to make this application more accessible!

## Want a CLI alternative instead?

Check out [cPDF](https://github.com/hkdb/cpdf), a Python script to simplify compress PDF file size with GhostScript

## What about Linux?

Check out [Densify](https://github.com/hkdb/Densify), the original PDF compressor written for Linux which iDensify is based on
