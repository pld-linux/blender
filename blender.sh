#!/bin/sh

if ! [ -f ~/.B.blend ] ; then
	cp /usr/X11R6/share/blender/defaults ~/.B.blend
fi

exec /usr/X11R6/lib/blender/blender $*
