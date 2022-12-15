#!/usr/bin/perl

##############################################################################
# User information display                                                   #
# Copyright 1998 Walt Bilofsky  bilofsky@toolworks.com                       #
# Modified from: Guestbook      Version 2.3.1                                #
# Copyright 1996 Matt Wright    mattw@worldwidemart.com                      #
# Created 4/21/95               Last Modified 10/29/95                       #
# Scripts Archive at:           http://www.worldwidemart.com/scripts/        #
##############################################################################
# COPYRIGHT NOTICE                                                           #
# Copyright 1996 Matthew M. Wright  All Rights Reserved.                     #
#                                                                            #
# Guestbook may be used and modified free of charge by anyone so long as     #
# this copyright notice and the comments above remain intact.  By using this #
# code you agree to indemnify Matthew M. Wright from any liability that      #  
# might arise from it's use.                                                 #  
#                                                                            #
# Selling the code for this program without prior written consent is         #
# expressly forbidden.  In other words, please ask first before you try and  #
# make money off of my program.                                              #
#                                                                            #
# Obtain permission before redistributing this software over the Internet or #
# in any other medium.	In all cases copyright and header must remain intact.#
##############################################################################
# Set Variables

$guestlog = "/home/bilofsky/public_html/capedory/register.log";
$cgiurl = "http://www.toolworks.com/cgi-bin/tw/register.cgi";
$date_command = "date";

$mailprog = "/usr/lib/sendmail -tf $mailmaster";

$counterfile = "/home/bilofsky/counters/data/cdbboard";

# Done
##############################################################################

# Get the Date for Entry
$date = `$date_command +"%A, %B %d, %Y at %T (%Z)"`; chop($date);
$shortdate = `$date_command +"%D %T %Z"`; chop($shortdate);

# query = delete to remove entries with the same name
# If $FORM{'editname'} is present, we are replacing entries with that name
$query = $ENV{'QUERY_STRING'};

# Get the input
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});

# Split the name-value pairs
@pairs = split(/&/, $buffer);

foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);

   # Un-Webify plus signs and %-encoding
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
   $value =~ s/<!--(.|\n)*-->//g;

   if ($allow_html != 1) {
      $value =~ s/<([^>]|\n)*>//g;
   }

   $FORM{$name} = $value;
}

   print "Content-type: text/html\n\n";
   print "<html><head><title>User Information</title></head>\n";
   print "<body><h1>User Information</h1>\n";
   print "<p>Date $date ($shortdate)<p>Remote Host: $ENV{'REMOTE_HOST'}\n";
   print "<p>Remote Address: $ENV{'REMOTE_ADDR'}<p>Remote User: $ENV{'REMOTE_USER'}\n";
   print "<p>Referring Page: $ENV{'HTTP_REFERER'}\n";
   print "<p>URL: $ENV{'URL'}\n";
   print "<p>HTTP_HOST: $ENV{'HTTP_HOST'}\n";
   if (open(DATA,"$counterfile")) {
	$counter = <DATA>;
	print "<p>Message Board counter = $counter\n";
	}

print "<table border=1 bordercolor=#0000FF cellpadding=0>\n";
foreach $key (sort (keys %ENV)) {
print "<tr><td><font face=Arial size=2>";
print "$key=$ENV{$key}\n";
print "</td></tr>";
}
print "</table>\n";

  print "\n</body></html>\n";

   exit;
