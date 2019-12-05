#!/bin/bash
# -*- coding: utf-8, tab-width: 2 -*-


function sendchars () {
  export LANG{,UAGE}=en_US.UTF-8  # make error messages search engine-friendly
  local LPDEV="${LPDEV:-/dev/usb/lp0}"
  local REPEAT="$1"; shift
  local CHARS="$*"

  case "$CHARS" in
    [+.]* )
      CHARS="$(perl bin2chr.pl "$CHARS"; echo :)"
      CHARS="${CHARS%:}"
      ;;
  esac

  local -A TS=(
    )
  let TS[bytes]="${#CHARS} * $REPEAT"
  TS[start]="$(date +%s%3N)"
  while [ "$REPEAT" -ge 1 ]; do
    echo -n "$CHARS" >>"$LPDEV" || return $?
    (( REPEAT -= 1 ))
  done
  TS[end]="$(date +%s%3N)"
  TS[diff]=$(( ${TS[end]} - ${TS[start]} ))
  echo "Printed ${TS[bytes]} in ${TS[diff]} ms = $(
    units -t "${TS[bytes]} bytes / ${TS[diff]} ms" 'KiB/s') KiB/s"
}










sendchars "$@"; exit $?
