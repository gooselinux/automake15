#!/bin/sh

/usr/lib/rpm/find-requires $* | egrep -v 'perl\(Automake::Struct\)' | sort -u
