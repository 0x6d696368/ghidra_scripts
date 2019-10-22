#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "BuiltInTypes.h"

// TODO: place the decompiled code here
void decode(char *in, int len, char *out)
{
	memcpy(out, in, len);
}



int main(int argc, char *argv[])
{
	// TODO: adjust this
	ssize_t len = 1024*1024*4; // 4 MiB
	char *buffer_in = malloc(len);
	char *buffer_out = malloc(len);
	len = read(0, buffer_in, len);
	if ( len <= 0 ) return 1;
	decode(buffer_in, len, buffer_out);
	write(1, buffer_out, len);
	return 0;
}

