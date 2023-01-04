VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "clsCmnDlg"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private Type OPENFILENAME
    lStructSize As Long
    hWndOwner As Long
    hInstance As Long
    lpstrFilter As String
    lpstrCustomFilter As String
    nMaxCustFilter As Long
    nFilterIndex As Long
    lpstrFile As String
    nMaxFile As Long
    lpstrFileTitle As String
    nMaxFileTitle As Long
    lpstrInitialDir As String
    lpstrTitle As String
    flags As Long
    nFileOffset As Integer
    nFileExtension As Integer
    lpstrDefExt As String
    lCustData As Long
    lpfnHook As Long
    lpTemplateName As String
End Type

Private Type oColorDlg
    lStructSize As Long
    hWndOwner As Long
    hInstance As Long
    rgbResult As Long
    lpCustColors As String
    flags As Long
    lCustData As Long
    lpfnHook As Long
    lpTemplateName As String
End Type

Private Type BrowseInfo
    hWndOwner As Long
    pIDLRoot As Long
    pszDisplayName As Long
    lpszTitle As Long
    ulFlags As Long
    lpfnCallback As Long
    lParam As Long
    iImage As Long
End Type

Public Enum FilterTypes
    textFiles = 0
    htmlFiles = 1
    exeFiles = 2
    zipFiles = 3
    AllFiles = 4
    CustomFilter = 5
End Enum

Private Declare Function GetOpenFileName Lib "comdlg32.dll" Alias "GetOpenFileNameA" (pOpenfilename As OPENFILENAME) As Long
Private Declare Function GetSaveFileName Lib "comdlg32.dll" Alias "GetSaveFileNameA" (pOpenfilename As OPENFILENAME) As Long
Private Declare Function ChooseColor Lib "comdlg32.dll" Alias "ChooseColorA" (pChoosecolor As oColorDlg) As Long
Private Declare Function lstrcat Lib "kernel32" Alias "lstrcatA" (ByVal lpString1 As String, ByVal lpString2 As String) As Long
Private Declare Function SHBrowseForFolder Lib "shell32" (lpbi As BrowseInfo) As Long
Private Declare Function SHGetPathFromIDList Lib "shell32" (ByVal pidList As Long, ByVal lpBuffer As String) As Long
Private Declare Sub CoTaskMemFree Lib "ole32.dll" (ByVal hMem As Long)
Private Declare Function GetForegroundWindow Lib "user32" () As Long

Private o As OPENFILENAME
Private filters(6) As String
Private extensions(6) As String
Private errOnCancel As Boolean

Property Let ErrorOnCancel(bln As Boolean)
    errOnCancel = bln
End Property

Property Get ErrorOnCancel() As Boolean
    ErrorOnCancel = errOnCancel
End Property

Sub SetCustomFilter(displayText As String, Optional wildCardExtMatch = "*.*")
    filters(5) = "____" + Chr$(0) + "___" + Chr$(0) + "All Files (*.*)" + Chr$(0) + "*.*" + Chr$(0)
    filters(5) = Replace(filters(5), "____", displayText)
    filters(5) = Replace(filters(5), "___", wildCardExtMatch)
    extensions(5) = Replace(wildCardExtMatch, "*", "")
End Sub

Private Sub Class_Initialize()
   
    ' If Not isRegistered And Not isInitalized Then TellThemAllAboutIt
    
    filters(0) = "Text Files (*.txt)" + Chr$(0) + "*.txt" + Chr$(0) + "All Files (*.*)" + Chr$(0) + "*.*" + Chr$(0)
    filters(1) = "Html Files (*.htm*)" + Chr$(0) + "*.htm*" + Chr$(0) + "All Files (*.*)" + Chr$(0) + "*.*" + Chr$(0)
    filters(2) = "Exe Files (*.exe)" + Chr$(0) + "*.exe" + Chr$(0) + "All Files (*.*)" + Chr$(0) + "*.*" + Chr$(0)
    filters(3) = "Zip Files (*.zip)" + Chr$(0) + "*.zip" + Chr$(0) + "All Files (*.*)" + Chr$(0) + "*.*" + Chr$(0)
    filters(4) = "All Files (*.*)" + Chr$(0) + "*.*" + Chr$(0)

    extensions(0) = ".txt"
    extensions(1) = ".html"
    extensions(2) = ".exe"
    extensions(3) = ".zip"
    extensions(4) = ".bin"
    
End Sub

Function OpenDialog(filt As FilterTypes, Optional initDir As String, Optional title As String, Optional pHwnd As Long = 0) As String

    If pHwnd = 0 Then pHwnd = GetForegroundWindow()
    
    o.lStructSize = Len(o)
    o.hWndOwner = pHwnd
    o.hInstance = 0
    o.lpstrFilter = filters(filt)
    o.lpstrFile = Space$(254)
    o.nMaxFile = 255
    o.lpstrFileTitle = Space$(254)
    o.nMaxFileTitle = 255
    o.lpstrInitialDir = initDir
    o.lpstrTitle = title
    o.flags = 0

    OpenDialog = IIf(GetOpenFileName(o), Trim$(o.lpstrFile), "")
    OpenDialog = Replace(OpenDialog, Chr(0), Empty)
    If Len(OpenDialog) = 0 And errOnCancel Then Err.Raise 1, "OpenDialog", "Cancel"
    
End Function

Function SaveDialog(filt As FilterTypes, Optional initDir As String, Optional title As String = "", Optional ConfirmOvewrite As Boolean = True, Optional pHwnd As Long = 0) As String
    
    If pHwnd = 0 Then pHwnd = GetForegroundWindow()
    
    o.lStructSize = Len(o)
    o.hWndOwner = pHwnd
    o.hInstance = pHwnd
    o.lpstrFilter = filters(filt)
    o.lpstrFile = Space$(254)
    o.nMaxFile = 255
    o.lpstrFileTitle = Space$(254)
    o.nMaxFileTitle = 255
    o.lpstrInitialDir = initDir
    o.lpstrTitle = title
    o.lpstrDefExt = extensions(filt)
    o.flags = 0

    Dim tmp As String
    tmp = IIf(GetSaveFileName(o), Trim$(o.lpstrFile), "")
    If ConfirmOvewrite And tmp <> "" Then
        If FileExists(tmp) Then
            If MsgBox("File Already Exists" & vbCrLf & vbCrLf & "Are you sure you wish to overwrite existing file?", vbYesNo + vbExclamation, "Confirm Overwrite") = vbYes Then SaveDialog = tmp
        Else
            SaveDialog = tmp
        End If
    Else
       SaveDialog = tmp
    End If
    
    If Len(SaveDialog) = 0 And errOnCancel Then Err.Raise 1, "SaveDialog", "Cancel"
    
End Function

Function ColorDialog(Optional pHwnd As Long) As Long
    Dim c As oColorDlg
    Dim cColors() As Byte
    
    If pHwnd = 0 Then pHwnd = GetForegroundWindow()
    
    c.lStructSize = Len(c)
    c.hWndOwner = pHwnd
    c.hInstance = App.hInstance
    c.lpCustColors = StrConv(cColors, vbUnicode)
    c.flags = 0

    If ChooseColor(c) <> 0 Then
        ColorDialog = c.rgbResult
        cColors = StrConv(c.lpCustColors, vbFromUnicode)
    Else
        ColorDialog = -1
        If errOnCancel Then Err.Raise 1, "ShowColor", "Cancel"
    End If
    
End Function

Function FolderDialog(Optional initDir As String, Optional pHwnd As Long = 0) As String
    Dim bInfo As BrowseInfo, ret As String, ptrList As Long, nullChar As Long

    If pHwnd = 0 Then pHwnd = GetForegroundWindow()
    
    With bInfo
        .hWndOwner = pHwnd
        .lpszTitle = lstrcat(initDir, "")  'returns memaddress
        .ulFlags = 1                      'only directories
    End With

    ptrList = SHBrowseForFolder(bInfo)
    If ptrList Then
        ret = String$(260, 0)
        SHGetPathFromIDList ptrList, ret 'Get the path from the IDList
        CoTaskMemFree ptrList            'free the block of memory
        nullChar = InStr(ret, vbNullChar)
        If nullChar > 0 Then ret = Left$(ret, nullChar - 1)
    End If

    FolderDialog = ret
    
    If Len(ret) = 0 And errOnCancel Then Err.Raise 1, "ChooseFolder", "Cancel"

End Function

Private Function FileExists(path) As Boolean
  If Len(path) = 0 Then Exit Function
  If Dir(path, vbHidden Or vbNormal Or vbReadOnly Or vbSystem) <> "" Then FileExists = True
End Function


