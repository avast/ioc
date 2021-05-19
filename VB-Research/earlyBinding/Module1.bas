Attribute VB_Name = "Module1"
Option Explicit

Sub main()

    Dim s As New SpeechLib.SpVoice
    Call s.Speak("Early binding is cool")
    
End Sub
