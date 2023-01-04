VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "CWindow"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit
'Author: david zimmer <dzzie@yahoo.com>
'Site:   http://sandsprite.com

'each window can only be subclassed by one subclasser.
'this is a new limitation for simplicity/sanity/stability/readability etc!

Public hwnd As Long
Private Messages() As Long
Public pOldWndProc As Long
Public Handler As CSubclass2

Public Function MsgExists(msg As Long) As Boolean
    On Error Resume Next
    
    If AryIsEmpty(Messages) Then
        MsgExists = False
        Exit Function
    End If
    
    Dim i As Long
    For i = 0 To UBound(Messages)
        If Messages(i) = msg Then
            MsgExists = True
            Exit Function
        End If
    Next
    
    Exit Function
    
End Function

Public Function ActiveMessages() As Long
    Dim i, found As Long
    
    If Not AryIsEmpty(Messages) Then
        For i = 0 To UBound(Messages)
            If Messages(i) <> 0 Then
                found = found + 1
            End If
        Next
    End If
    
    ActiveMessages = found
    
End Function

Public Sub RemoveMsg(msg As Long)
    Dim i As Long
    If AryIsEmpty(Messages) Then Exit Sub
    For i = 0 To UBound(Messages)
        If Messages(i) = msg Then
            Messages(i) = 0
            Exit Sub
        End If
    Next
End Sub

Public Function AddMsg(msg As Long) As Boolean
    lpush Messages, msg
End Function

Private Function AryIsEmpty(ary) As Boolean
  On Error GoTo oops
    Dim x As Long
    x = UBound(ary)
    AryIsEmpty = False
  Exit Function
oops: AryIsEmpty = True
End Function

Private Sub lpush(ary() As Long, value As Long)   'this modifies parent ary object
    On Error GoTo init
    Dim x As Long
    x = UBound(ary) '<-throws Error If Not initalized
    ReDim Preserve ary(UBound(ary) + 1)
    ary(UBound(ary)) = value
    Exit Sub
init: ReDim ary(0): ary(0) = value
End Sub
