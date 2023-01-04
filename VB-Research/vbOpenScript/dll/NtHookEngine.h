
//This is a modified version of the open source x86/x64 
//NTCore Hooking Engine written by:
//Daniel Pistelli <ntcore@gmail.com>
//http://www.ntcore.com/files/nthookengine.htm
//
//It uses the x86/x64 GPL disassembler engine
//diStorm was written by Gil Dabah. 
//Copyright (C) 2003-2012 Gil Dabah. diStorm at gmail dot com.
//
//Mods by David Zimmer <dzzie@yahoo.com>

enum hookType{ 
	ht_jmp = 0,     /* 32 - 5 byte relative, 64 - 12 byte absolute                                                       */
	ht_pushret=1,   /* 32 - 6 byte absolute, 64 - 6 byte absolute (target MUST be 32 bit addressable)                    */
	ht_jmp5safe=2,  /* 32 bit only, 10 byte relative hook, safe against hook bypassers                                   */
	ht_jmpderef=3,  /* 32 bit - 10 byte absolute, 64 bit - 14 byte absolute                                              */
	ht_micro,       /* 32 bit - 2/5 byte hook (api/prealignment) relative jmp, 64 bit - 6/8 byte hook - absolute address */
	ht_auto         /* probes best hook to use automatically at runtime                                                  */
};


enum hookErrors{ he_None=0, he_cantDisasm, he_cantHook, he_maxHooks, he_UnknownHookType, he_cantInit  };
enum specificErrors{ hs_None, hs_NeedsAbs, hs_NoMicro, hs_ToBig, hs_x64NoPushRet };

extern specificErrors specificError;
extern hookErrors lastErrorCode;
extern int logLevel;

extern void  (__cdecl *debugMsgHandler)(char* msg);
extern char* __cdecl GetHookError(void);
extern char* __cdecl GetDisasm(ULONG_PTR pAddress, int* retLen = NULL);
extern int __cdecl DisableHook(ULONG_PTR Function);
extern void __cdecl EnableHook(ULONG_PTR Function);
extern ULONG_PTR __cdecl GetOriginalFunction(ULONG_PTR Hook);
extern BOOL __cdecl HookFunction(ULONG_PTR OriginalFunction, ULONG_PTR NewFunction, char* name, enum hookType ht);
extern bool is32BitSafe(ULONG_PTR value);
