
Credits:
-----------------------------
NTCore Hooking Engine written by Daniel Pistelli ntcore at gmail dot com (slightly modified)
https://ntcore.com/files/nthookengine.htm

diStorm x86/x64 BSD disassembler engine
Copyright (C) 2003-2012 Gil Dabah. diStorm at gmail dot com.
https://github.com/gdabah/distorm

vb_structs.h is from vbParser by sysenter-eip

openscript.dll and injector written by David Zimmer dzzie@yahoo.com
http://sandsprite.com

About:
-----------------------------

This is a research project aimed at making any VB6 application scriptable.

This starts with an injection dll that hooks some functions in the vb runtime,
patches internal class ObjectTypes, and registers the vb.global.forms
object in the Running Object Table (ROT)

Now all of the forms, embedded controls, public methods/variables/classes are accessible
as if it were an ActiveX exe. Clients can include WSH scripts, python scripts, VB6 etc.
Basically any language that use COM objects.

A brief overview of the technique is as follows:

- VB6 process is started with an injection dll
- New thread hooks  CVBApplication_Init and BeginPaint
- CVBApplication_Init hook:
      - Stores a reference to internal VB objects during runtime initialization
      - Patches VBHeader.ProjectInfo.ObjectTable setting all classes public
- BeginPaint hook:
      - Runs from main VB6 thread
      - Adds a system menu item and subclasses main window for IPC (optional)
      - Registers internal VB.Global.Forms object in the ROT 

Note: This code is dependant on this particular version of the vb runtime (msvbvm60.dll)

See the following Avast blog post for more details: https://decoded.avast.io/davidzimmer/scripting-arbitrary-vb6-applications/


