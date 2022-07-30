#!/usr/bin/bash
# Make μ-tool tarball
help() {
  echo "Usage: $0 <folder>"
  exit
}

[ -z "$1" ] && echo "Usage: $0 <folder>" && exit
[ ! -d "$1" ] && echo "Folder '$1' not found or is not folder" && exit
[ ! -f "$1/ver" ] && echo "File '$1/ver' not found" && exit
[ ! -f "$1/.2tar" ] && echo "File '$1/.2tar' not found" && exit
pushd "$1" > /dev/null || exit
FNAME="$1-$(cat ver)"
tar -Jcf "../$FNAME.tar.xz" --transform="s,^,$FNAME/,S" -T .2tar
popd > /dev/null || exit
