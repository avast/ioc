VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "CSubclass2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
'Author: david zimmer <dzzie@yahoo.com>
'Site:   http://sandsprite.com

'added 5.17.12 - supports changing the return value to the callers SendMessage()

Event MessageReceived(hwnd As Long, wMsg As Long, wParam As Long, lParam As Long, Cancel As Boolean)

Public ErrorMessage As String
Public ErrorNumber As Long
 
Private mOverRide As Boolean
Private mVal As Long

Public Windows As New Collection

Friend Function WasOverRidden() As Boolean
    WasOverRidden = mOverRide
End Function

Friend Function OverRideVal() As Long
    OverRideVal = mVal
End Function

Function OverRideRetVal(newRetVal As Long)
    mOverRide = True
    mVal = newRetVal
End Function

Function AttachMessage(hwnd As Long, wMsg As Long) As Boolean
On Error GoTo hell
    
    modSubclass.MonitorWindowMessage Me, hwnd, wMsg
    AttachMessage = True
    ErrorMessage = ""
    ErrorNumber = 0

Exit Function
hell:
      ErrorMessage = Err.Description
      ErrorNumber = Err.Number

End Function

Sub DetatchMessage(hwnd As Long, wMsg As Long)
    
    modSubclass.DetachWindowMessage hwnd, wMsg
    
End Sub

Private Sub Class_Initialize()
    modSubclass.RegisterClassActive Me
End Sub

Private Sub Class_Terminate()
    modSubclass.RemoveActiveClass Me
End Sub

Friend Sub ForwardMessage(hwnd As Long, wMsg As Long, wParam As Long, lParam As Long, Optional Cancel As Boolean)
    
    'this sub is only called from the module,
    'friend methods are not externally visible in compiled dll interface
    
    mOverRide = False
    RaiseEvent MessageReceived(hwnd, wMsg, wParam, lParam, Cancel)
    
    
End Sub


