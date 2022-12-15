#!/usr/bin/perl 

# To do:
#  Test find on testboard for extra <ul>s in middle.

####################################################################
# find.cgi  Search WWWBoard Articles
# Created by: Craig D. Horton, DBasics Software Company
# I can be reached at: dbasics@aol.com
# Script Found at:     http://www.dbasics.com/
# This script may be redistributed for non-commericial reasons
# as long as this header remains intact. All copyrights reserved.
####################################################################
#
# Modified by Walt Bilofsky http://www.toolworks.com/bilofsky/wwwboard
# Changes Copyright 1999 Walt Bilofsky (insert GPL info here)
# Script has been modified to generate a packed database and index
#	file of the messages in the WWWBoard message directory.
#	Also automatically moves messages from index file to
#	archive index file if there is one.  Deleting is manual tho.
# This database can be used to (1) speed up searching greatly, since
#	only one file needs to be opened for the search, and (2) allow
#	for generation of HTML display of messages on the fly.
#	This permits archiving rarely-viewed messages and generating
#	them, to save space, while preserving the speedy display of
#	recent messages in the original WWWBoard format.
# Archiving can be done at two levels:
#	Search level:  All messages are archived but used only for search.
#		Message files must not be deleted.
#	Archive level:  Only messages older than a given number are
#		archived.  Used both for search and display.  Archived
#		messages may not have followups posted.
#
####################################################################
#
# Call with query:search key.
# If a list of files to search has already been prepared, also
#	use files:file1\nfile2\n...
# To build a master file with searchable text from all files to be
#	searched, call with argument build:1.
# Mod 3/99: Indexed archive file. 
#
####################################################################

$board = $ENV{'QUERY_STRING'};

#if ($#ARGV >= 0 && $ARGV[0] eq "build") { 	# Allow to be run from command line with "build" as arg to build.
#	$FORM{'build'} = 1;
#      $FORM{'query'} = "";
#	$FORM{'lastmsg'} = 14100;
#	$board = "localtest";   #### For debugging on local machine only!
#	$debug = 1;
#	}

$MAXSIZE = 20000;		       # Only these many bytes of each file are examined - otherwise real slow.

$FS = "\275";			 # Field separator
$SS = "\274";			 # Section separator

# Define Variables

$cgi_url = "/cgi-bin/wwboard.cgi";
$background = $fbackground = "";
$mesgdir = "messages";
$datafile = "data.txt";
$dbasefile = "msgdbase.txt";
$logfile = "findlog.txt";
$indexfile = "index.bin";
$tempfile = "tempfile";
@mesgfiles = ( "index.html" );
$mesglink = "index.html";	 # Where mesgfile is referenced from baseurl
$faqfile = "faq.htm";
$show_faq = 0;
$posturl = "post.htm";	         # URL for posting new messages, from baseurl
$domain = "toolworks.com";       # for email return address

$basedir = "/home/toolwo5/public_html";
$baseurl = "http://www.toolworks.com";

$ext = "html";
$lastfile = 0;			   # Highest file number to put into database
$maxfile = 0;			   # Highest file number not in packed database
$actually_wrote = 0;

&process_args if ($board ne "localtest");			# Process the input arguments to script
if ($FORM{'board'}) { $board = $FORM{'board'}; }

if ($board eq "cd") {
   $basedir = "/home/toolwo5/public_html/cdsoa";
   $baseurl = "http://www.capedory.org";
   @mesgfiles = ( "index.html", "oldmsgs.html" );
   $dir = "bboard";
   $title = "Cape Dory Information Exchange";
   $background = " bgcolor=\"#F6FEFF\"";
   $background = " bgcolor=\"#FFFFFF\" text=\"#000066\" ";
   $fbackground = "$background background=\"/cgi-bin/rand_image.cgi\"";
   $posturl = "cdbbpost.htm";	 # URL for posting new messages, from baseurl
#   $counterfile = "/home/httpd/vhosts/toolworks.com/httpdocs/counters/data/cdbboard";
   }
elsif ($board eq "tyc") {
   $baseurl = "http://www.tyc.org";
   $domain = "tyc.org";       # for email return address
   $basedir = "/home/httpd/vhosts/toolworks.com/httpdocs/tyc";
   $dir = "raceresults";
   $title = "TYC Race Results";
   $background = " bgcolor=\"#FFFFFF\" background=\"http://www.tyc.org/images/bg.gif\"";
   $fbackground = $background;
   $titles_only = 1;		# Message titles only in index file (for read-only board)
   }
elsif ($board eq "tide") {
   $dir = "bilofsky/tidetool/board";
   $title = "French Tide Tool Message Board";
   $background = $fbackground = " BGCOLOR=\"#D5EBF0\"";
   }
elsif ($board eq "test") {
# Debugging settings - rename file to testboard.cgi
   $dir = "testboard";
   @mesgfiles = ( "index.html", "oldmsgs.html" );
   $cgi_url = "/cgi-bin/testboard.cgi";
   $background = $fbackground = " BGCOLOR=\"#FFFFE8\"";
   $title = "TEST Message Board";
   }
elsif ($board eq "localtest") {
#  This option is for testing on your own machine, not an Internet host.
#  Get the argument list by running testboard on the ISP, paste it in here, 
#    add the $FORM{ "action" } you want, duplicate your board directory on your home
#    machine, and run this script using PERL.  Should work ...
   $basedir = ".";
   @mesgfiles = ( "index.html", "oldmsgs.html" );
   $dir = "testboard";
   $title = "TEST Message Board";
   $background = $fbackground = " BGCOLOR=\"#FFFFE8\"";
   }
elsif ($board eq "wvbr") {
   $dir = "wvbr/board";
   $title = "WVBR Alumni Message Board";
   $background = $fbackground = " BGCOLOR=\"#FFFFE8\"";
#   $mail_posts = 2;
   }
else { $baseurl = ""; }		# Error - but need to report it later.

$basedir = "$basedir/$dir";
$baseurl = "$baseurl/$dir";
$nbtitle = $title;
$nbtitle =~ s/ /&nbsp;/g;

%months = ( "January" => 1,"February" => 2,"March" => 3,"April" => 4,
		"May" => 5,"June" => 6,"July" => 7,"August" => 8,
		"September" => 9,"October" => 10,"November" => 11,"December" => 12);

# This is the listing of message files in relationship to basedir/mesgdir
# It is understood that all these files must be nnn.html.
@files = ("*.html"
          );

# Print out a content-type for HTTP/1.0 compatibility
  print "Content-type: text/html\n\n";
  print "<html><head><title>Search Results For $FORM{'query'}</title></head>\n";
  print "<body $fbackground>\n";
  print "<center><h2>$title</h2></center>\n";
  if ($show_faq == 1) {
      print "<center>[&nbsp;<a href=\"$baseurl/$posturl\">Post&nbsp;a&nbsp;New&nbsp;Message</a>&nbsp;] [&nbsp;<a href=\"$baseurl/$mesglink\">$title</a>&nbsp;] [&nbsp;<a href=\"$baseurl/$faqfile\">How&nbsp;to&nbsp;Use&nbsp;This&nbsp;Board</a>&nbsp;]</center>\n";
   }
   else {
      print "<center>[&nbsp;<a href=\"$baseurl/$posturl\">Post&nbsp;a&nbsp;New&nbsp;Message</a>&nbsp;] [&nbsp;<a href=\"$baseurl/$mesglink\">$title</a>&nbsp;]</center>\n";
   }
if ($baseurl eq "/") {
	&fatal("Unknown Message Board: Internal error: Please <a href=\"mailto:bilofsky\@toolworks.com\">notify the Webmaster</a>."); };
$fq = $FORM{'query'};

# If searching on specified files, load them into @FILES
if ($FORM{'search'}) {
   @FILES = split(/ /,$FORM{'filelist'});
   $FORM{'filelist'} = " $FORM{'filelist'} ";
   }
# Otherwise load all files designated in @files into the array @FILES
 else {
   foreach $file (@files) {
#     if ($debug != 0) {
#       $fq = $FORM{'query'} = "Henry";
#	 $ls = "";
#       for ($i = 1; $i < 20; ++$i ) {
#          $ls = "$ls $i.html";
#       }  } else
     { $ls = `cd $basedir/$mesgdir; ls $file`; }
     @FILES = split(/\s+/,$ls);
  }  }

$dbasefile = "$basedir/$dbasefile";
$indexfile = "$basedir/$indexfile";
$pack = "";

### If building the data file, open the existing files and get current lengths.

if( $FORM{'build'}) {
   if (!$FORM{'lastmsg'} && $#mesgfiles != 0) {
	fatal("The '$board' message board has an archive page.  You must specify an ending message number.");
	}
   foreach $FILE (@FILES) {				  # Find the highest file number
	if ( $FILE =~ /^(\d+)\./ && $1 > $lastfile) { $lastfile = $1; }
   	}
   if ($FORM{'lastmsg'} && $FORM{'lastmsg'} < $lastfile) { $lastfile = $FORM{'lastmsg'}; }
 
   $i = $#FILES + 1;
   print "<p>Consolidating up to $lastfile.html from a total of $i files.\n";
   if (! (-e $indexfile)) { 
	open(INDEX,">$indexfile"); 				# Create if doesn't already exist.
	close(INDEX);
	}
   if (! (-e $dbasefile)) { 
	open(DATA,">$dbasefile"); 
	print DATA "Walt Bilofsky fecit\n";			# Make first line start at nonzero
	close(DATA);
	}
   open(INDEX,"+<$indexfile") || &fatal("Can't open $indexfile.\n");
   binmode(INDEX);
   if (sysread(INDEX,$pack,4) == 4) {   		  # Read highest file nr
   	$maxfile = unpack("l",$pack);			  #   if it's there (otherwise it's 0)
	if ($maxfile > $lastfile) {
		&fatal("Nothing to archive: You requested up to $lastfile but archive already goes to $maxfile.");
	}	}
   open(DATA,"+<$dbasefile") || &fatal("Can't open $dbasefile.\n");
   seek(DATA,0,2);					# Position at end of data file
   $orig_datasize = tell(DATA);
   &open_log;

   print LOG "\n**************************************************\n\n";
   print LOG "$shortdate: REBUILDING DATABASE FILE.  Called by $ENV{'REMOTE_HOST'};$ENV{'REMOTE_ADDR'}.\n";
   print LOG "\Consolidating up to $lastfile.html from a total of $i files.\n";
   $MAXSIZE = 1000000;		       		# If building, read entire file (or first megabyte anyway)
   }

### If searching:  First get a quick key for fast elimination of most records.

 else {
  @QUICK = split(/\s+/, $fq);				  # Get words in key
  if (!$debug && $#QUICK == -1 ) 			  # Find a good word to use to eliminate most msgs.
	{ &fatal("You didn't specify a search key.  Click the \"Back\" button on your browser and try again."); }
  @QUICK = sort bylen @QUICK;
  $quick_fq = $QUICK[0];				  #  Use the longest one in the list.

### Open the database files.  Search through the packed database for any
###	records containing the search key.
  $lastfile = 9999999;
  if (open(INDEX,"<$indexfile")) {		        # Searching.  Is there a database?
   binmode(INDEX);					  # If so, let's look in there now.
   open(DATA,"<$dbasefile") || &fatal("Can't open $dbasefile.\n");
   if (sysread(INDEX,$pack,4) != 4) {   		  # Read highest file nr
	&fatal("Can't read $indexfile.\n"); }
   $maxfile = unpack("l",$pack);			  # Remember maximum file that is in database
   <DATA>;							  # Get past dummy line at start
   while (<DATA>) {					  # Then search through master data file.
	$line = $_;
	if ($quick_fq 					  # If no blanks in search key,
		&& !$line =~ /$quick_fq/io) {		  # can quickly eliminate most records.
			next; }
	if (!($line =~ /(\d+?):/)) {  		  # Pick off file name
		&fatal("Bad database format - line $line\n"); }
	$FILE = "$1.html";
	if ($FORM{'search'}) {				  # If searching a file list,
		if (! ($FORM{'filelist'} =~ / $FILE /))
			{ next; }				  #   reject filenames not on list.
		}
	if ( $line =~ /$quick_fq/io ) { 		  # If didn't screen already, do that now.
		&ExamineFile; }				  # Search actual file.
	}
   } }

### Examine each of the unscreened files.
foreach $FILE (@FILES) {
   $FILE =~ /^(\d+)\./;
   if ($FORM{'build'} || $1 > $maxfile) { 	  # Search only those files not
	&ExamineFile; 					  #	already screened.
   }	}

### If rebuilding database - close out the files, print statistics and exit.

if ($FORM{'build'}) {
   $pack = pack("l",$lastfile);			  # Write file number of last file in database
   seek(INDEX,0,0);
   if (syswrite(INDEX,$pack,4) != 4) {   		  # Create data file and print highest nr.
	&fatal("Can't write at start of $indexfile.\n"); }

   $bytes = ($tell = tell(DATA)) - $orig_datasize;	  #  print statistics and exit.
   close(DATA);
   close(INDEX);

   &update_archive_page;

   if ($board ne "localtest") {
      @endtimes = times();
      $cputime = $endtimes[0] - $startimes[0]; 
      $systime = $endtimes[1] - $startimes[1];

      print LOG "\tExamined $nfiles files.\n";
      print LOG "\tWrote $bytes bytes from $actually_wrote files on database file.\n";
   	print LOG "\tDatabase file now $tell bytes long.\n";
 	print LOG "\tLast file entered was $lastfile.html.\n";
      print LOG "\tTimes used:  CPU: $cputime secs.; System: $systime secs.\n\n";
   }
   print "<p>Examined $nfiles files.\n";
   print "<br>Wrote $bytes bytes from $actually_wrote files on database file.\n";
   print "<br>Database file now $tell bytes long.\n";
   print "<br>Last file entered was $lastfile.html.\n";

   print "<p>Times used:  CPU: $cputime secs.; System: $systime secs.\n\n";
   print "\n</body></html>\n";

   exit;
 }

#### If searching, print out search results.

@OUTPUT = sort(@OUTPUT);				  # Reversing gets later files first.
$goodfiles = join(' ', @GOODFILES);

print "<form method=POST action=\"$ENV{'SCRIPT_NAME'}?$board\">\n";
print "<p><center><b>Search on Keyword: <input type=text name=\"query\" size=20> \n";
print "<input type=submit value=\" Search! \"> <A HREF=$baseurl/$faqfile#search\">Search Tips</A><br>\n";
print "<INPUT TYPE=\"radio\" NAME=\"search\" VALUE=\"0\" CHECKED>New Search ";
print "<INPUT TYPE=\"radio\" NAME=\"search\" VALUE=\"1\">Search These Messages Only</b>\n";
print "<input type=hidden name=\"filelist\" value=\"$goodfiles\"\n";
print "</form></center>\n";

  print "<hr size=3 width=75%><p>\n";
  print "<center><h1>Search Results for \"$fq\"</h1></center>\n";

$results = $#OUTPUT + 1;
if ($results != 0) {
   print "<OL>\n@OUTPUT\n</OL>";
 } else {
   print "<b><center>No matching messages found.  Try another key or read the <A HREF=$baseurl/$faqfile#search\">Search Tips</A></b></center>\n";
}

if ($board ne "localtest") {
   @endtimes = times();
   $cputime = $endtimes[0] - $startimes[0];
   $systime = $endtimes[1] - $startimes[1];
   }

&open_log;

$type = "New"; if ($FORM{'search'}) { $type = "Refined"; }
if (LOG) {
	print LOG "$shortdate: $type search used $cputime CPU and $systime system secs.  Scrutinized $nexamined and found $results messages with \"$fq\".  Called by $ENV{'REMOTE_HOST'};$ENV{'REMOTE_ADDR'}.\n";
	close(LOG);
	}

print "</body></html>\n";

exit;

#######################################################################
#
#  MOVE LINES FROM THE MAIN INDEX PAGE TO THE ARCHIVE PAGE
#	AND UPDATE LINKS
#
sub update_archive_page {

	$indent = 0;
	$iname = "$basedir/$mesgfiles[0]"; 		# Open the index files, and temp files for copying
	open(INDEXF,$iname) || &fatal("Can't open $iname to archive.\n");
	$tiname = "$basedir/$tempfile"."2"; 
	open(IFTEMP,">$tiname") || &fatal("Can't create $tiname to archive.\n");
	if ($#mesgfiles) {
		$aname = "$basedir/$mesgfiles[1]"; 
		open(ARCHIVE,$aname) || &fatal("Can't open $aname to archive.\n");
		$taname = "$basedir/$tempfile"; 
		open(AFTEMP,">$taname") || &fatal("Can't create $taname to archive.\n");
		}

	&lock_num;						# Lock databases to prevent double access.

	while ($line = <INDEXF>) {			# Read current message file.
		last if ($line =~ /<!--(t|top): ?$lastfile-->/o);	# Skip to start of archive sect
		$indent++ if ($line =~ /<ul>/i);
		$indent-- if ($line =~ /<\/ul>/i);
		print IFTEMP $line;			# Copy current message file to IFTEMP until $lastfile.
		}
	if ($#mesgfiles) {				##### If copying to the archive,
	   while ($aline = <ARCHIVE>) {		# Read archive file and copy it to temp file.
		print AFTEMP $aline;
		last if ($aline =~ "<!--begin-->");	#   up to start of message lines.
		}
	   if ($indent > 1) {				# Don't break at a followup - URLs will be
		fatal(					#  wrong in original message.
			"Can't break archive at message number $lastfile - it is a followup at level $indent.<p>Line: $line\n");
		}

 	   &fix_url(999999);
	   print AFTEMP $line;				# Start of archiving.
	   while ($line = <INDEXF>) {			# Now copy section being archived from index file.
		&fix_url(999999);				# In archive, all URLS use CGI script
		last if (!($line =~ /<!--(t|r|i|e)/));	# Stop when no more comment lines
		print AFTEMP $line;
		}
	  while ($aline = <ARCHIVE>) {			# Copy remainder of archive file.
		print AFTEMP $aline; }
	  unlink("$aname.bak");				# Rename temp to new archive file.
	  close(AFTEMP);
	  close(ARCHIVE);
	  rename($aname, "$aname.bak") || &fatal("Can't rename $aname to $aname.bak");
	  rename($taname, $aname) || &fatal("Can't rename $taname to $aname");
	  chmod(0664, $aname);
	  }							##### END copying to archive file

	{ do {						# Copy remainder of index file.
		&fix_url($lastfile);			# Anything past lastfile in index	
		print IFTEMP $line; 			#  uses CGI script.
	   } while ($line = <INDEXF>); }		# Copy remainder of index file.
	unlink("$iname.bak");
	close(IFTEMP);
	close(INDEXF);					# Rename IFTEMP to new index file.
	rename($iname, "$iname.bak") || &fatal("Can't rename $iname to $iname.bak");
	rename($tiname, $iname) || &fatal("Can't rename $tiname to $iname");
	chmod(0664, $iname);

	&unlock_num;					# Remove lock on database
	}

# Open number datafile and lock it - this prevents two simultaneous updates.
sub lock_num {
   open(NUMBER,"$basedir/$datafile");
   if (!$debug) {
	$LOCK_EX = 2;
   	flock(NUMBER,$LOCK_EX);
   }	}

sub unlock_num {
   close(NUMBER);
   }
sub fix_url {
	($last2fix) = @_;
	if ($line =~ /$mesgdir\/(\d+).$ext/	&& $1 <= $last2fix) {
		$line =~ s/$mesgdir\/(\d+).$ext/$cgi_url?$board&$1/;
	}	}

###########################################
#
# LOOK AT ONE MESSAGE - EITHER TO SEARCH IT
#	OR TO COPY IT INTO THE DATABASE FILE
#
# Database format:
#	INDEX file contains one long per message: offset into data file
#		First entry holds highest file number in database.
#	DATA file contains records terminated by newline, as follows:
#		filename:title~postername~email~origmsgnr~timedate^~^messagetext^~^followups\n
#		   where:
#			~ is the field separator $FS
#			^~^ is the section separator $SS
#			messagetext is the body text only (newlines => $SS)
#			followups is the followups section of the message with 
#				just the message numbers and indenting HTML commands.

sub ExamineFile {
   $FILE =~ /^(\d+)\./;
   $filenum = $1;
   $url = '';
   $msgtitle = '';
   $body = '';
   if ($filenum > $maxfile) { 	  		  # Message is still in a separate file
      if (!open(FILE,"$basedir/$mesgdir/$FILE"))   # If file isn't really there
		{ return; }					  #  do nothing.
	if ($filenum > $lastfile) { return; }	  # If past the max archiving limit return.
   	++$nfiles;						  # Otherwise read file into $filecont.
   	$i = sysread(FILE,$filecont,$MAXSIZE);
   	close(FILE);
	if (!$i) { return; }				  # Return if it's empty.
	if ($quick_fq &&
	   ! ($filecont =~ /$quick_fq/io)) {	  # Quick check for short key.
		return; }
	}
    else {							  # If file is in the database already
	if ( $FORM{'build'}) {return; }		  # Ignore if building database.
	&get_packed_message;				  # If searching - extract the components
	$msgtitle = $m_subject;
	$filecont = "$msgtitle: Posted by $m_name on $m_date$FS$m_body";
	}
   ++$nexamined;
   if( $FORM{'build'}) {				  # If building the database file,
	$poster = $email = 
		$replyto = $timedate = $followups = 
		$in_followups = "";
	$in_header = 1;
	$whereami = tell(DATA);				  # Remember start of record
     	}
    else {							  # If searching,
	if ($filenum > $maxfile) { 
     	  $filecont =~ s/<a name="followups">(.|\n)*$//;  # String in line - get rid of stuff after msg
	 } else {
	  $filecont =~ s/$FS<i>:.*?(?=$FS)//iog; # Remove lines starting with colon (quoted msg)
	  $filecont =~ s/$FS/\n/og;			  # Replace line ends by spaces
	} }
   @LINES = split(/\n/, $filecont);
   foreach $line (@LINES) {
     if ($line =~ /<title>/i ) {
       $lpos = (index(lc($line),"<title") + 7);
       $rpos = (rindex(lc($line),"/title"));
       $msgtitle = substr($line,$lpos,($rpos-$lpos)-1);
	 next;
       }
     if ($line =~ "^<i>:") {
       if (!$FORM{'build'}) { next; }             # On this board, indicates quotes in a reply
       }                                          #  so ignore this unless building the body text
     if ($line =~ /^<h(r|1)/) {
       next; 				              # Ignore horizontal rule  and header lines
       }
     if ($line =~ s/In Reply To:.*?href=\"//i) {  # Reply-to line?
	 $line =~ s/(.*)$cgi_url\?$board&//io;		  # Strip off CGI url if it's in the reference
       if ($line =~ /^(\d+)/) {
	 	$replyto = $1; }				  # Ignore reply-to line (remembering the file number)
	 next; }
     if ($FORM{'build'}) {				  # If building file, scan for the other fields
	 $line =~ s/[\012\r\n]*\Z//;			  # Remove all CR and LFs at end of line.
	 if (!$poster && $line =~ s/.*Posted by:? (<\/em>)?(.*)/$2/i) {
	      $email = "";				  # Posted-by line - scan for poster
		if ($line =~ /\<a href=\"mailto:(.*)">(.*)<\/a> on (.*?)\</ 
		 || $line =~ /\<a href=\"mailto:(.*)">(.*)<\/a> on (.*)/) {
			$email = $1;
			$poster = $2; 
			$timedate = $3;
			$poster =~ s/ \Q($email)\E//;	  # If email appears in poster name, remove it.
			}
		  elsif ($line =~ /(.*) on (.*?)\</ || $line =~ /(.*) on (.*)/) {
			$poster = $1; 
			$timedate = $2; }
		  else { &fatal("Can't dissect Posted-by line: File $FILE = $line"); }
		if ($timedate =~ /(\w+) (\d+), (\d+) at (\d+):(\d+):/) {
			$timedate = "$months{$1}/$2/$3 at $4:$5";  # Convert date/time to compact format
			}
     		$in_header = 0; 				  # end of header
		next;
		}
	  next if ($in_header);				  # If still in header, ignore
	  if ($line =~ /<a name="followups">/) {  # Start of followups?
		$in_followups = 1;
		next;
	  	}
	    elsif ($in_followups && $line =~ s/<!--(e|end): ?$filenum-->//) {
		$followups .= $line;
		last;						  # After followups - done with file.
	  	}
	  }		
     elsif ($line =~ "<!--(i|insert):") {
       last;                                      # If not building, stop searching after the message text
       }
     if ($FORM{'build'}) {				  # If building the compressed search file
	 if (!$in_followups) {				  #  and not in the followup section
	    next if ($line =~ /^<\/LI><\/UL>/i);		  #  and line after message header
          if (!$line =~ /^<ul><li><a href/i) {		  #  (Fix 11/02: Preserve link line WB)
	       next if ($line =~ /^<UL>/i);	}	  	  #   (new way here)
	    next if ($line =~ /<h(r|1)/i);			  #  and horizontal rules and title line
	    next if ($line =~ /^\s*<\/?center>\s*$/i);  # and lines entirely with <center>
	    }
	 $line =~ s/<!--(t|top): ?\d*-->//;  	  # Remove comment tags from followup section
	 $line =~ s/<!--(i|insert): ?\d*-->//;
	 $line =~ s/<!--(e|end): ?\d*-->//;
	 $line =~ s/\(<!--(r|responses): ?\d*-->\d*\)//;
	 if ($in_followups) {
		if ($line =~ s/<a href=\"(\d+).$ext\"(.*)/$SS/i) {
			# Here need to make sure any URL for a message is going to work now and,
			#   if the target message isn't yet archived, later on when it is.
			$x1 = $1; $x2 = $2;	 	 # Find URL reference to message
			if ($x1 > $lastfile) {		  # If file not yet packed
				$x1 = "<a href=\"$cgi_url?$board&$1\"$x2"; # keep the full line with CGI href
				}				  #  else just put the number in.
			$line =~s/$SS/$x1/;		  # Replace the reference with it.
			}
		$followups .= $line;
	  	}
	   elsif (!$body) { $body = $line; }
	   else { $body .= $FS . $line; }
	 }
      elsif ($line =~ /$fq/io) {                   # Not building - searching. Found the search key
       $line =~ s/<.*?>//g;                       # Eliminate the HTML markings
       if (! ($line =~/$fq/io)) { next; }          # Did that get rid of the match?
       $url = $FILE;
       $url =~ s/$basedir/$baseurl/o;              # OK, we got a match.
       $lpos = index(lc($line),lc($fq));
       $rpos = $lpos + length($fq);               # Make a copy of line with match in bold
       $ll = substr($line,0,$lpos);
       $rr = substr($line,$rpos);
       if ($lpos > 50) { $ll = substr($ll,-50); }
       if (length($rr) > 50) { $rr = substr($rr,0,50); }
       $goodline = "$ll<b>$fq</b>$rr";
       $goodline =~ s/"/&quot;/g;
       last;
     }
   }
   if ($FORM{'build'}) {				  # If building the compressed search file
	if ($msgtitle eq "") { &fatal("Can't find title for message $FILE.\n"); }
	if ($poster eq "") { &fatal("Can't find poster's name for message $FILE - $msgtitle.\n"); }
	if ($timedate eq "") { &fatal("Can't find posting date for message $FILE - $msgtitle.\n"); }
	$FILE =~ /\d*/;
	print DATA "$&:";					  # Print file number in data file.
			  					  # print the header info and body
	print DATA "$msgtitle$FS$poster$FS$email$FS$replyto$FS$timedate$SS$body$SS";
	$followups =~ s/<ul><\/ul>//ig;		  # Remove null indents
	print DATA "$followups\n";	 		  # Print followups.

	$pack = pack("l",$whereami);			  # Write record into index file
	$whereindex = 4 * $filenum;
	if (!seek(INDEX, $whereindex, 0)) {
		&fatal("Can't write index record for $FILE.\n");
	 	}
	print INDEX $pack;
	++$actually_wrote;
	}
    elsif ($url ne '') {				  # Otherwise if search key found,
     push(@GOODFILES,$FILE);				  #  add file to the list.
     $sortindex = 1000000 - $filenum;		  # Get constant-width key putting latest files first
     if ($filenum > $maxfile) {
		$href = "$baseurl/$mesgdir/$url"; }	  # Construct URL that will display this message
	else { $href = "$cgi_url?$board&$filenum"; }
     push(@OUTPUT,"<!--$sortindex--><LI><a href=\"$href\"><b>$msgtitle</b></A> - <font size=-1>$goodline</font>\n");  
   }
}

sub get_packed_message {				  # EXTRACT A MESSAGE FROM THE DATABASE
	if (! ($line =~ /(\d+):(.*?)$FS(.*?)$FS(.*?)$FS(.*?)$FS(.*?)$SS(.*?)$SS(.*)/o)) {
		&fatal("Bad Message Format: Message $FILE is garbled in the database.  Please notify the system administrator.<p>Message text: $line");
		  }
	$m_number = $1;
	$m_subject = $2;
	$m_name = $3;
	$m_email = $4;
	$m_replyto = $5;
	$m_date = $6;
	$m_body = $7;
	$m_followups = $8;
}

sub process_args {
	@startimes = times(); 
# Get the input
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});

# Split the name-value pairs
	@pairs = split(/&/, $buffer);

	foreach $pair (@pairs) {
	   ($name, $value) = split(/=/, $pair);
	
	   $value =~ tr/+/ /;
	   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	   $FORM{$name} = $value;
	   }
}

# Handle fatal errors.
# Manage the files too.  If the datafile was written on, truncate it.
#  Index file does not get the last message number written until the end, so
#	even if it's too long, it will be overwritten with the right data eventually.
sub fatal {
   ($msg) = @_;
   print "<p><b>Fatal error: $msg</b>\n";
   print "\n</body></html>\n";
   &open_log;
   print LOG "Fatal error: $msg\n\n";
   if ($orig_datasize) {					# Data file may have been written on.
	truncate(DATA,$orig_datasize); } 			# If so, get rid of the new part.
   exit;
}

sub open_log {							# Helper to avoid opening log before needed.
	return if ($logfile eq "");
	$logfile = ">>$basedir/$logfile";
	open(LOG,$logfile);
	$logfile = "";
# Get the date (used only for the log file)
   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
   if ($sec < 10) { $sec = "0$sec"; }
   if ($min < 10) { $min = "0$min"; }
   if ($hour < 10) {$hour = "0$hour"; }
   if ($mon < 10) { $mon = "0$mon"; }
   if ($mday < 10) {$mday = "0$mday"; }
   $year += 1900;
   $year =~ s/^\d\d//;
   $month = ($mon + 1);

   $shortdate = "$month/$mday/$year at $hour\:$min\:$sec";		# Switch to shorter format

}

sub bylen {
            $xx = length($b) - length($a);
         }

#END OF SCRIPT
