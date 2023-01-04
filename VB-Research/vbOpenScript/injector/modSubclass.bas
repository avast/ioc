Attribute VB_Name = "modSubclass"
Option Explicit
'Author: david zimmer <dzzie@yahoo.com>
'Site:   http://sandsprite.com

'Design: you can have an unlimited number of classes, and should be
'        able to subclass an unlimited number of windows. Each class
'        can in turn subclass as many windows as it wants, and it should
'        be able to attach to as many messages per window as it wants.
'
'        You can edit message parameters and cancel them directly in
'        the eventhandler you implement for the clsSubClass in your code.
'
'       One thing you cannot do, is to have multiple classes subclass the
'       same window looking for the same message. Different subclasses can not
'       subclass the same window (new limitation in sake of cleanliness/sanity/stability)

Private Declare Function SetWindowLong Lib "user32" Alias "SetWindowLongA" (ByVal hwnd As Long, ByVal nIndex As Long, ByVal dwNewLong As Long) As Long
Private Declare Function GetWindowLong Lib "user32" Alias "GetWindowLongA" (ByVal hwnd As Long, ByVal nIndex As Long) As Long
Private Declare Function CallWindowProc Lib "user32" Alias "CallWindowProcA" (ByVal lpPrevWndFunc As Long, ByVal hwnd As Long, ByVal msg As Long, ByVal wParam As Long, ByVal lParam As Long) As Long
Private Declare Function IsWindow Lib "user32" (ByVal hwnd As Long) As Long
Private Const GWL_WNDPROC = (-4)

Private ActiveClasses As New Collection 'of CSubclass2
Private Windows As New Collection 'of CWindow

Function RegisterClassActive(clsActive As CSubclass2)
    ActiveClasses.Add clsActive, "Objptr:" & ObjPtr(clsActive)
End Function

Sub RemoveActiveClass(clsTerminate As CSubclass2)
    On Error Resume Next
    CloseOutClass clsTerminate
    ActiveClasses.Remove "Objptr:" & ObjPtr(clsTerminate)
    If ActiveClasses.Count = 0 Then InitTearDown
End Sub



'updated
Private Sub InitTearDown()
    On Error Resume Next
    Dim cw As CWindow
    
    For Each cw In Windows
        SetWindowLong cw.hwnd, GWL_WNDPROC, cw.pOldWndProc
        Set cw.Handler = Nothing
    Next

    Set Windows = New Collection
    
End Sub


Sub MonitorWindowMessage(notify As CSubclass2, ByVal hwnd As Long, ByVal wMsg As Long)
    
    'updated
    If IsWindow(hwnd) = False Then Err.Raise 1, , "Invalid Window Handle"

    Dim cw As CWindow
    
    If AlreadySubclassing(hwnd, cw) Then
         
        If Not ObjPtr(cw.Handler) <> ObjPtr(notify) Then
            Err.Raise 3, , "This window is already subclassed by another class, not supported in name of stability.."
        Else
            If Not cw.MsgExists(wMsg) Then cw.AddMsg wMsg
        End If
        
   Else
       
        'subclass each window only once
        Set cw = New CWindow
        cw.pOldWndProc = SetWindowLong(hwnd, GWL_WNDPROC, AddressOf WindowProc)
        
        If cw.pOldWndProc = 0 Then Err.Raise 2, , "Subclass failed hwnd: " & hwnd
        
        cw.hwnd = hwnd
        Set cw.Handler = notify
        cw.AddMsg wMsg
        Windows.Add cw, "Hwnd:" & hwnd
        
    End If
                

End Sub

'updated
Sub DetachWindowMessage(ByVal hwnd As Long, ByVal wMsg As Long)
    
    Dim cw As CWindow
    
    If AlreadySubclassing(hwnd, cw) Then
        cw.RemoveMsg wMsg
        If cw.ActiveMessages = 0 Then
            SetWindowLong hwnd, GWL_WNDPROC, cw.pOldWndProc
            Set cw.Handler = Nothing
            Set cw = Nothing
            Windows.Remove "Hwnd:" & hwnd
        End If
    End If
    
End Sub

Function CloseOutClass(c As CSubclass2)

    Dim cw As CWindow
    
    For Each cw In Windows
        If ObjPtr(cw.Handler) = ObjPtr(c) Then
            SetWindowLong cw.hwnd, GWL_WNDPROC, cw.pOldWndProc
            Set cw.Handler = Nothing
            Windows.Remove "Hwnd:" & cw.hwnd
        End If
    Next
            
End Function

Function WindowProc(ByVal hwnd As Long, ByVal wMsg As Long, ByVal wParam As Long, ByVal lParam As Long) As Long
    
    Dim stopIt As Boolean
    Dim ret As Long
    Dim s2 As CSubclass2
    Dim cw As CWindow
    
    If Not AlreadySubclassing(hwnd, cw) Then Exit Function 'shouldnt happen...
        
    If cw.Handler Is Nothing Then 'shouldnt happen
        DetachWindowMessage hwnd, wMsg
        Exit Function
    End If
    
    If Not cw.MsgExists(wMsg) Then 'we dont care just pass it on..
        WindowProc = CallWindowProc(cw.pOldWndProc, hwnd, wMsg, wParam, ByVal lParam)
        Exit Function
    End If
    
    cw.Handler.ForwardMessage hwnd, wMsg, wParam, lParam, stopIt
    
    If cw.Handler.WasOverRidden() Then
        WindowProc = cw.Handler.OverRideVal()
        Exit Function
    End If
    
    'stopit can be set = true when event is raised from clsSubClass
    'any of the parameters passed in forward message could be changed
    If Not stopIt Then
        WindowProc = CallWindowProc(cw.pOldWndProc, hwnd, wMsg, wParam, ByVal lParam)
    End If
    
    
End Function

Private Function AlreadySubclassing(hwnd As Long, cw As CWindow) As Boolean
    On Error Resume Next
    For Each cw In Windows
        If cw.hwnd = hwnd Then
            AlreadySubclassing = True
            Exit Function
        End If
    Next
    AlreadySubclassing = False
End Function


