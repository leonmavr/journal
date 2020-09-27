/*
A simple graphics library for CSE 20211 by Douglas Thain

This work is licensed under a Creative Commons Attribution 4.0 International License.  https://creativecommons.org/licenses/by/4.0/

For complete documentation, see:
http://www.nd.edu/~dthain/courses/cse20211/fall2013/gfx
Version 3, 11/07/2012 - Now much faster at changing colors rapidly.
Version 2, 9/23/2011 - Fixes a bug that could result in jerky animation.
*/

#include <X11/Xlib.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "gfx.h"

// <-- omitted -->
//
static unsigned int find_octant(int x1, int y1, int x2, int y2) {
	if (x1 == x2)
		return 8;
	float m = (float)(y2 - y1)/(x2 - x1);
	if ((x1 <= x2) && (0 <= m) && (m <= 1))
		return 0;
	else if ((y1 <= y2) && (m > 1))
		return 1;
	else if ((y1 <= y2) && (m < -1))
		return 2;
	else if ((x2 <= x1) && (0 >= m) && (m >= -1))
		return 3;
	else if ((x2 <= x1) && (0 < m) && (m <= 1))
		return 4;
	else if ((y2 <= y1) && (m > 1))
		return 5;
	else if ((y2 <= y1) && (m < -1))
		return 6;
	else if ((x1 <= x2) && (-1 <= m) && (m <= 0))
		return 7;
}


/* Draw a line from (x1,y1) to (x2,y2) using Bresenham's */
void gfx_line_bres(int x1, int y1, int x2, int y2)
{
	int dx = x2 - x1;
	int dy = y2 - y1;
	float m = (float)dy/dx;
	int err = 0;
	int y = y1, x = x1;
	unsigned int oct = find_octant(x1, y1, x2, y2);
	switch(oct){
		case 0: // 1st octant
			y = y1;
			for (x = x1; x < x2; x++) {
				gfx_point(x, y);
				err += dy;
				if (2*err >= dx){
					err -= dx;
					y++;
				}
			}
			break;
		case 1:
			x = x1;
			for (y = y1; y < y2; y++) {
				gfx_point(x, y);
				err += dx;
				if (2*err >= dy){
					err -= dy;
					x++;
				}
			}
			break;
		case 2:
			x = x1;
			for (y = y1; y < y2; y++) {
				gfx_point(x, y);
				err -= dx;
				if (2*err >= dy){
					err -= dy;
					x--;
				}
			}
			break;
		case 3:
			y = y1;
			for (x = x1; x > x2; x--) {
				gfx_point(x, y);
				err += dy;
				if (2*err >= -dx){
					err += dx;
					y++;
				}
			}
			break;
		case 4:
			y = y1;
			for (x = x1; x > x2; x--) {
				gfx_point(x, y);
				err -= dy;
				if (2*err >= -dx){
					err += dx;
					y--;
				}
			}
			break;
		case 5:
			x = x1;
			for (y = y1; y > y2; y--) {
				gfx_point(x, y);
				err -= dx;
				if (2*err >= -dy){
					err -= dy;
					x--;
				}
			}
			break;
		case 6:
			x = x1;
			for (y = y1; y > y2; y--) {
				gfx_point(x, y);
				err += dx;
				if (2*err >= -dy){
					err += dy;
					x++;
				}
			}
			break;
		case 7:
			y = y1;
			for (x = x1; x < x2; x++) {
				gfx_point(x, y);
				err -= dy;
				if (2*err >= dx){
					err -= dx;
					y--;
				}
			}
			break;
		case 8:
			if (y1 < y2){
				for (y = y1; y < y2; y++) {
					gfx_point(x, y);	
				}
			} else {
				for (y = y2; y < y1; y++) {
					gfx_point(x, y);	
				}
			}
			break;
	}
}
