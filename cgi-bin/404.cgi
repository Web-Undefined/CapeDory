#!/usr/bin/perl

# print header
print "Content-type: text/html\n";
#print "Status: 404 File Not Found\n" unless $ENV{'HTTP_REFERER'} =~ /MSIE/;
print "\n";

$url = $ENV{'REQUEST_URI'};


PrintHead();

print "<BODY bgcolor=\"#F6FEFF\" text=\"#000000\">";
print "<HR>\n";
print "<ADDRESS>\n";
print "&nbsp;\n";
print "</ADDRESS>\n";
print "<div align=\"left\">\n";
print "  <table align = left border=\"0\" cellpadding=\"3\" cellspacing=\"0\" background=\"http://www.capedory.org/images/30drawing_background.gif\">\n";
print "    <tr>\n";
print "      <td valign=\"top\" width=\"300\" height=\"300\"><H2>404: File Not Found</H2></td>\n";
print "      <td valign=\"middle\">\n";
print "<center><font size=4>\n";
print "<p>The page<br><b>http://www.capedory.org&shy;$url</b><br>can not be found.</font>\n";
if ($ENV{'HTTP_REFERER'}) {
	print "<p><font size=3>Please contact the administrator of <A HREF=\"$ENV{'HTTP_REFERER'}\">$ENV{'HTTP_REFERER'}</A> and inform them their link is invalid.</font>\n" 
   }
print "</center>\n";
print "        <p>&nbsp;</td>\n";
print "    </tr>\n";
print "  </table>\n";
print "</div><br clear=\"all\">\n";
print "<HR>\n";
print "<ADDRESS>&nbsp;</ADDRESS>\n";
InError();


# Debugging to print out all environment variables.

#print "<table cellpadding=3>\n<tr><td align=center colspan=2><b>Environment Variables</b></td></tr>\n";
#foreach $key (sort (keys %ENV)) {
#print "<tr><td><font face=Arial size=2>";
#print "$key</td><td>$ENV{$key}\n";
#print "</td></tr>";
#}
#print "</table>\n";


sub InError {
print "<p><font size=3><i>If you think you have received this message in error, please email <a href=\"mailto:webmaster\@capedory.org?subject=404 Error: $url\">the webmaster</a>.</i></font>\n";
print "<P>\n";
}

sub PrintHead {
   print <<EOHead;
<HTML>
<HEAD>
<TITLE>404 File Not Found</TITLE>
</HEAD>
EOHead

}
