#!/bin/bash

set -x

tmp=$(mktemp -d)
tmp=obs-studio

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
package=obs-studio
branch=master
name=obs-studio

pushd ${tmp}
git clone https://github.com/jp9000/obs-studio.git
cd ${package}
git checkout ${branch}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
version=`git describe --tags | awk -F '-' '{print $1}' | tr -d 'v'`
git archive --prefix="${name}-${version}/" --format=tar master > "$pwd"/${name}-${version}-${date}-${tag}.tar
gzip "$pwd"/${name}-${version}-${date}-${tag}.tar



