#!/usr/bin/perl
# -*- coding: UTF-8, tab-width: 2 -*-
use strict;
use warnings;
$| = 1;  # disable output buffering (tribute to perl 5.8.x)

my $input = join '', @ARGV;
$input =~ s![\+=]!1!g;
$input =~ s![\._\-]!0!g;
$input =~ s![^01]!!g;

foreach my $byte ($input =~ m![01]{1,8}!g) {
  print chr oct substr "0b${byte}00000000", 0, 10;
}
