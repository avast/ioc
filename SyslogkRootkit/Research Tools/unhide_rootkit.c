// It unhides the Syslog Rootkit
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
 
void main(void)
{
	int fd = open("/proc/syslogk", O_WRONLY);
	lseek(fd, 0 , SEEK_SET);
	write(fd, "1", 1); // Command for unhiding the module
	close(fd);
}