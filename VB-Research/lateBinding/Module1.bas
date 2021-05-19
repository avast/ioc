Attribute VB_Name = "Module1"
Option Explicit

Sub main()
    
    Dim voice As Object
    Set voice = CreateObject("SAPI.SpVoice")
    Call voice.Speak("Late binding is cool")
    
End Sub
