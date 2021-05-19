Attribute VB_Name = "Module1"
Option Explicit

Dim g As Long

Private Declare Sub callback Lib "dummy.dll" (ByVal s As Long)

Sub Main()
    g = 21
    callback g + 1
End Sub


