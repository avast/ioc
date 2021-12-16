#include "main.h"
#include <windows.h>

void DLL_EXPORT SetNtApiFunctions()
{
    ShellExecuteA(0, "open", "calc.exe", 0, 0, SW_SHOWNORMAL);
}
