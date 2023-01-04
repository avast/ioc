#include <intrin.h>

void msg(char);
void msgf(const char*, ...);

HWND hServer=0;

typedef struct{
    int dwFlag;
    int cbSize;
    int lpData;
} cpyData; 

void FindVBWindow(){
	char *vbIDEClassName = "ThunderFormDC" ;
	char *vbEXEClassName = "ThunderRT6FormDC" ;
	char *vbWindowCaption = "injector" ;

	hServer = FindWindowA( vbIDEClassName, vbWindowCaption );
	if(hServer==0) hServer = FindWindowA( vbEXEClassName, vbWindowCaption );
} 

int msg(char *Buffer){
  
  char msgbuf[0x1001];

  if(!IsWindow(hServer)) hServer=0;
  if(hServer==0) FindVBWindow();
  
  COPYDATASTRUCT cpStructData;
  memset(&cpStructData,0, sizeof(struct tagCOPYDATASTRUCT )) ;
  _snprintf(msgbuf, 0x1000, "%x,%x,%s", GetCurrentProcessId(), GetCurrentThreadId(), Buffer);

  cpStructData.dwData = 3;
  cpStructData.cbData = strlen(msgbuf) ;
  cpStructData.lpData = (void*)msgbuf;
  
  int ret = SendMessage(hServer, WM_COPYDATA, 0,(LPARAM)&cpStructData);

  //if ret = trigger then do something special 

  return ret;

} 

void msgf(const char *format, ...)
{
	DWORD dwErr = GetLastError();
		
	if(format){
		char buf[1024]; 
		va_list args; 
		va_start(args,format); 
		try{
 			 _vsnprintf(buf,1024,format,args);
			 msg(buf);
		}
		catch(...){}
	}

	SetLastError(dwErr);
}

int* pPlus(int * p, int increment){
  _asm{
	mov eax, p
	add eax, increment
   }
}

int* pPlus(void * p, int increment){
  _asm{
	mov eax, p
	add eax, increment
   }
}


 

