#!/bin/sh

/usr/lib/rpm/find-provides $* | egrep -v 'perl\(Automake::Struct\)' | egrep -v 'perl\(Class::Struct::Tie_ISA\)' | sort -u
