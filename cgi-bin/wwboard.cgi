#!/usr/bin/perl
##############################################################################
# WWWBoard                      Version 2.0 ALPHA 2                          #
# Copyright 1996 Matt Wright    mattw@worldwidemart.com                      #
# Created 10/21/95              Last Modified 12/15/00 by Walt Bilofsky      #
# Scripts Archive at:           http://www.worldwidemart.com/scripts/        #
# Installed as Cape Dory bboard http://www.toolworks.com/capedory/bboard     #
# Mods Copr. 1996-1999 Walt Bilofsky bilofsky@toolworks.com                  #
##############################################################################
# COPYRIGHT NOTICE                                                           #
# Copyright 1996 Matthew M. Wright  All Rights Reserved.                     #
#                                                                            #
# WWWBoard may be used and modified free of charge by anyone so long as      #
# this copyright notice and the comments above remain intact.  By using this #
# code you agree to indemnify Matthew M. Wright from any liability that      #  
# might arise from it's use.                                                 #  
#                                                                            #
# Selling the code for this program without prior written consent is         #
# expressly forbidden.  In other words, please ask first before you try and  #
# make money off of my program.                                              #
#                                                                            #
# Obtain permission before redistributing this software over the Internet or #
# in any other medium.  In all cases copyright and header must remain intact.#
##############################################################################

# Modifications: (by Walt Bilofsky - bilofsky@toolworks.com)
#   11/2/01 - add picture and link icons
#   12/15/00 - add TYC race board.
#   4/11/99 - Check for no added text in reply, and FS/WTB messages.
#   4/10/99 - Add file locking, and checking for stutter on the Post button.
#   4/3/99 - Add message display from packed database file
#   3/27/99 - Change <!-- word: n--> to <!--w:n--> to save space
#	(backwards compatible to old files)
#   12/19/98 - add counter to CD post (now commented out)
#   1/15/98 - add TYC race board
#   9/24/97 - email address in header
#   Preview before posting
#   Mail subscription
#   Quoted text in italics
#   List most recent messages
#   Support multiple boards
#   Search messages for keywords
#   Allow splitting large message index files

###########################################################################
# Configure Options

$show_faq = 1;          # 1 - YES; 0 = NO
$allow_html = 1;        # 1 = YES; 0 = NO
$quote_text = 1;        # 1 = YES; 0 = NO
$subject_line = 0;      # 0 = Quote Subject Editable; 1 = Quote Subject 
                        #   UnEditable; 2 = Don't Quote Subject, Editable.
$use_time = 0;          # 1 = YES; 0 = NO
$mail_posts = 0;		# 1 = Mail to subscribers, 2 = just mail summary, 0 = don't mail
$body_wrap = "ON";      # Word wrap in message body input window: ON or OFF
$body_width = 70;       # Width of message body input window
$debugargs = 0;         # 1 = Print args to form when debugging
$num_to_show = 30;      # Nr arguments for "Show recent posts"
$titles_only = 0;		# Message titles only in index file (for read-only board)
$short_tags = 1;		# Abbreviates tags in message list - saves about 12% of space in index file
$use_logfile = 0;		# 1 = Record poster in logfile; otherwise goes into the message itself.

# Done
###########################################################################

# Define Variables

$board = $ENV{'QUERY_STRING'};

#$board = "localtest";   #### For debugging on local machine only!

if ($board =~ s/&(\d+)//) {	# If called with boardname&argument
	$msg_to_disp = $1;	#  the argument is the number of a message to display
	}

# Defaults - may be changed for a particular board.

$cgi_url = "http://www.capedory.org/cgi-bin/wwboard.cgi";
$background = $fbackground = "";
$mesgdir = "messages";
$datafile = "data.txt";
@mesgfiles = ( "index.html" );
$mesglink = "index.html";	 # Where mesgfile is referenced from baseurl
$faqfile = "faq.htm";
$posturl = "post.htm";	         # URL for posting new messages, from baseurl
$domain = "toolworks.com";       # for email return address
$subscurl = "subscribe.htm";	 # Web page for subscribing to email
$logfile = "findlog.txt";

$dbasefile = "msgdbase.txt";	 # Packed database files for displaying a message
$indexfile = "index.bin";

$FS = "\275";			 # Field separator
$SS = "\274";			 # Section separator

$basedir = "/home/toolwo5/public_html";
$baseurl = "http://www.toolworks.com";

($top, $responses, $insert, $end) = ("top", "responses", "insert", "end");
($top, $responses, $insert, $end) = ("t", "r", "i", "e") if ($short_tags);

$ext = "html";
$LOCK_EX = 2;
$LOCK_UN = 8;

if ($board eq "cd") {
   $basedir = "/home/toolwo5/public_html/cdsoa";
   $baseurl = "http://www.capedory.org";
   @mesgfiles = ( "index.html", "oldmsgs.html" );
   $dir = "bboard";
   $title = "The Cape Dory Board";
   $background = " bgcolor=\"#FFFFFF\" text=\"#000066\" ";
   $fbackground = "$background background=\"/cgi-bin/rand_image.cgi\"";
   $posturl = "cdbbpost.htm";	 # URL for posting new messages, from baseurl
   $num_to_show = 40;
#   $counterfile = "/home/httpd/vhosts/toolworks.com/httpdocs/counters/data/cdbboard";
   $screen_for_sale = "#forsale";               # Indicates no replies to for-sale/wtb allowed.
   $use_logfile = 1;
   $pixicon = "pic.gif";
   $linkicon = "link.gif";
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
elsif ($board eq "tyccrew") {
   $baseurl = "http://www.tyc.org";
   $domain = "tyc.org";       # for email return address
   $basedir = "/home/httpd/vhosts/toolworks.com/httpdocs/tyc";
   $dir = "racecrew";
   $title = "TYC Crew Finder";
   $background = " bgcolor=\"#FFFFFF\" background=\"http://www.tyc.org/images/bg.gif\"";
   $fbackground = $background;
   $mail_posts = 1;
   }
elsif ($board eq "test") {
   @mesgfiles = ( "index.html", "oldmsgs.html" );
   $dir = "testboard";
   $cgi_url = "/cgi-bin/testboard.cgi";
   $background = $fbackground = " BGCOLOR=\"#FFFFE8\"";
   $title = "TEST Message Board";
   $pixicon = "pic.gif";
   $linkicon = "link.gif";
   }
elsif ($board eq "tide") {
   $dir = "bilofsky/tidetool/board";
   $title = "French Tide Tool Message Board";
   $background = $fbackground = " BGCOLOR=\"#D5EBF0\"";
   $mail_posts = 1;
   }
elsif ($board eq "localtest") {
#  This option is for testing on your own machine, not an Internet host.
#  Get the argument list by running testboard on the ISP, paste it in here, 
#    add the $FORM{ "action" } you want, duplicate your board directory on your home
#    machine, and run this script using PERL.  Should work ...
   $basedir = ".";
   $dir = "";
   $title = "TEST Message Board";
   $background = $fbackground = " BGCOLOR=\"#FFFFE8\"";
   }
elsif ($board eq "wvbr") {
   $dir = "wvbr/board";
   $title = "WVBR Alumni Message Board";
   $background = $fbackground = " BGCOLOR=\"#FFFFE8\"";
   $mail_posts = 2;
   }
else { &fatal_error("Unknown Message Board: $board",
   "Internal error: Please <a href=\"mailto:bilofsky\@toolworks.com\">notify the Webmaster.  Error code <$board></a>.");
   }

$basedir = "$basedir/$dir";
$baseurl = "$baseurl/$dir";
$nbtitle = $title;
$nbtitle =~ s/ /&nbsp;/g;

# filenames for mailer program 

$mailprog = '/usr/lib/sendmail';
$subscribe = 'email.txt';

$user_ID = "$ENV{'REMOTE_HOST'}; $ENV{'REMOTE_ADDR'}";	# To ID multiple consecutive posts.

# Done
###########################################################################

if ($msg_to_disp) {				# If displaying a message from packed database
	if (&get_packed_variables) {		# Fetch variables from the packed file
		&new_file; }			# Print out in HTML
	else { 					# If msg still in file, display it line by line
		open(MSG,"$basedir/$mesgdir/$msg_to_disp.$ext") ||
			fatal_error("File not found","The message you requested ($msg_to_disp\.$ext) is no longer available.");
 		print "Content-type: text/html\n\n";
		while ($i = <MSG>) {		# except make local hrefs refer to $basedir since we're in cgi-bin
			$i =~ s/(href|src)=\"(?!(\/|#|http:|ftp:|mailto:))/$1=\"$baseurl\/$mesgdir\//ig;
			print $i;
		}	}
	exit;
	}

# Get the Data Number
&get_number;

# Get Form Information
&parse_form;

# Put items into nice variables
&get_variables;

# View recently posted messages 2/97 WB
if ($FORM{'action'} eq "View Recent Posts") { &viewrecent; }

#Don't allow posting a blank body.
if ($errorflag == 2) { 
   &fatal_error("No Message",
      "Sorry - you can't post a blank message.<p>Use the [Back] button in your browser to return to the previous page, and enter your message in the &quot;Message&quot; field.");
   }

# View Before Posting Modification
if ($FORM{'action'} ne "post") {
  &view_post;
}

# If an error got past the preview, tell the user now.
if ($errorflag) { &error; }


# Get the Data Number
flock(NUMBER,$LOCK_EX);				# Lock the data file.
&get_number_again;				# Refresh the data (in case we slept through a post)
if ($last_user == $user_ID			# If the post is by the same user (suspicious)
    && $last_post_time > time - 15) {	#  within the last 15 seconds (VERY suspicious)
	&fatal_error("Itchy Finger","Looks like you hit the \"Post\" button more than once.\
  Your message posted successfully the first time, so please don't hit it again.\n\
  <hr size=3 width=75%>\n\
  <center>[ <a href=\"$baseurl/$mesglink\">$title</a> ]</center>\n\
  <hr size=3 width=75%>\n");
	}

# Open the new file and write information to it.
&new_file;

# Open the Main WWWBoard File to add link
&main_page;

# Now Add Thread to Individual Pages
if ($num_followups >= 1) {
   &thread_pages;
}

# Increment Number
&increment_num;

# Email the post to subscribers
if ($mail_posts != 0) {
    &email_post;
}

# Return the user HTML
&return_html;

############################
# Get Data Number Subroutine

sub get_number {
   open(NUMBER,"+<$basedir/$datafile") || die $!;
   $num = <NUMBER>;
   $numnum = ++$num;
}
sub get_number_again {
   seek(NUMBER,0,0);
   $num = <NUMBER>;
   $last_user = <NUMBER>;
   $last_post_time = <NUMBER> || time - 1000;
   $num++;
}

sub increment_num {
   seek(NUMBER,0,0);
   print NUMBER "$num\n";				# Put most recent poster's ID info on number file.
   $i = time;						#  and posting time.
   print NUMBER "$user_ID\n$i\n\n\n";
   close(NUMBER);						# This unlocks the file.
}

#######################
# Parse Form Subroutine

sub parse_form {

   # Get the input
   if ($debugargs != 2) {
       read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
#     $buffer = $ENV{'QUERY_STRING'};
   }

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
      else {
         unless ($name eq 'body') {
            $value =~ s/<([^>]|\n)*>//g;
         }
      }

      if ($debugargs != 2) {
          $FORM{$name} = $value;
      } else {    
          $value =~ s/\n/\\n/g;
          $value =~ s/\@/\\\@/g;
          print "\$FORM\{ &quot;$name&quot; \} = &quot;$value&quot;;<br>\n";
   }  }

}

###############
# Get Packed Variables
#	Retrieves information to display a message from a packed file
#	Returns 1 for success, 0 if message is still in a text file.

sub get_packed_variables {
	$dbasefile = "$basedir/$dbasefile";
	$indexfile = "$basedir/$indexfile";

	if (!open(INDEX,"$indexfile") 
		  || read(INDEX,$last_packed_msg,4) != 4				# Read last file number
		  || !($last_packed_msg = unpack("l",$last_packed_msg))) {
	    &fatal_error("File Missing",
		"The database file $indexfile is missing or bad.  Please notify the system administrator."); }
	open(DATA,"$dbasefile") || &fatal_error("File Missing",
		"The database file $dbasefile is missing.  Please notify the system administrator.");
	binmode(INDEX);
	return 0 if ($msg_to_disp > $last_packed_msg);
	$last_packed_msg = 

	&packed_msg_error 
		if &get_packed_message($msg_to_disp);		# Get variables from the main message
 	$num = $m_number;
      $long_date = $m_date;
      $name = $m_name;
	$email = $m_email;
      $subject = $m_subject;
	$body = $m_body;
	$followup_list = $m_followups;
	$body =~ 								# Fix URLs as best we can away from cgi-bin
 		s/(href|src)=\"(?!(\/|#|http:|ftp:|mailto:))/$1=\"$baseurl\/$mesgdir\//ig;

      if ($followup = $m_replyto) {
		$last_message = $followup;
		&packed_msg_error 
			if &get_packed_message($followup);		# Get variables from the reply-to message
      	$origdate = $m_date;
     		$origname = $m_name;
		$origemail = $m_email;
      	$origsubject = $m_subject;
		}
	$body =~ s/$FS/\n/g;						# Put newlines back in the body
	$followup_list =~ s/$FS/\n/g;					#  and followup list
   	$hidden_body = "$body";						# For formatting in the printout
   	$hidden_body =~ s/</&lt;/g;
   	$hidden_body =~ s/>/&gt;/g;
   	$hidden_body =~ s/"/&quot;/g;
	return 1;
	}

sub get_packed_message {
   	($msg_num) = @_;
	if (!seek(INDEX,4*$msg_num,0) 				# Seek to the position of the message number
		  || read(INDEX,$offset,4) != 4			# Read the offset
		  || !($offset = unpack("l",$offset)) 		#  and it better be there.
		  || !seek(DATA, $offset ,0)				# Seek to the actual message text
		  || !( $msg_line = <DATA> )) {			#  and it better be there.
			return ($m_errcode = 1);			# Or return 1 = missing
		 	 }
	if (! ($msg_line =~ /(\d+):(.*?)$FS(.*?)$FS(.*?)$FS(.*?)$FS(.*?)$SS(.*?)$SS(.*)/o)) {
		return ($m_errcode = 2);				# Bad format - return 2
		}
	$m_number = $1;
	$m_subject = $2;
	$m_name = $3;
	$m_email = $4;
	$m_replyto = $5;
	$m_date = $6;
	$m_body = $7;
	$m_followups = $8;
	return 0;
}

sub packed_msg_error {
	if ($m_errcode == 1) {
		&fatal_error("Message Missing",
		  "Message number $msg_num is missing from $indexfile in the database.  Please notify the system administrator.");
	 	}
	  elsif ($m_errcode == 2) {
		&fatal_error("Bad Message Format",
		  "Message number $msg_num is garbled in the database.  Please notify the system administrator.<p>Message text: $msg_line");
	}	}

###############
# Get Variables

sub get_variables {

   $errorflag = 0;

   if ($FORM{'followup'}) {
      $followup = "1";
      @followup_num = split(/,/,$FORM{'followup'});
      $num_followups = @followups = @followup_num;
      $last_message = pop(@followups);
      $origdate = "$FORM{'origdate'}";
      $origname = "$FORM{'origname'}";
      $origsubject = "$FORM{'origsubject'}";
      $origemail = "$FORM{'origemail'}";
   }
   else {
      $followup = "0";
   }

   if ($FORM{'name'}) {
      $name = "$FORM{'name'}";
      $name =~ s/"//g;
      $name =~ s/<//g;
      $name =~ s/>//g;
      $name =~ s/\&//g;
      &check_arglen($name,"Your name",30);
   }
   else {
       if ($titles_only == 0) { $errorflag = 1; }
      $name = "";
   }

   if ($FORM{'email'} =~ /.*\@.*\..*/) {
      $email = "$FORM{'email'}";
      &check_arglen($email,"Your email address",60);
   }

   if ($FORM{'subject'}) {
      $subject = "$FORM{'subject'}";
      $subject =~ s/\&/\&amp\;/g;
      $subject =~ s/"/\&quot\;/g;
      &check_arglen($subject,"The subject",75);
   }
   else {
      $errorflag = 1;
      $subject = "";
   }

   if ($FORM{'url'} && !($FORM{'url_title'})) {
	$FORM{'url_title'} = $FORM{'url'}; }
   if ($FORM{'url'} =~ /.*\:.*\..*/ && $FORM{'url_title'}) {
      $message_url = "$FORM{'url'}";
      $message_url_title = "$FORM{'url_title'}";
   } elsif ($FORM{'url'}) {
	&fatal_error("Bad Link URL","There appears to be an error in your link URL.  Please use the [Back] button on your browser to check it.<p>If you receive this message in error, please notify the webmaster.");
   }
   if ($FORM{'img'} =~ /.*tp:\/\/.*\..*/) {
      $message_img = "$FORM{'img'}";
   } elsif ($FORM{'img'}) {
	&fatal_error("Bad Image URL","There appears to be an error in your image URL.  Please use the [Back] button on your browser to check it.<p>If you receive this message in error, please notify the webmaster.");
   }
	
   if ($FORM{'body'}) {
      $body = "$FORM{'body'}";
      $body =~ s/\cM//g;
      $body =~ s/\n\n/<p>/g;
      $body =~ s/\n/<br>/g;

      # Bug fix - 1/23/97 - restore quotes to get past WebSurfer
      $body =~ s/~qq~/&quot;/g;

      $body =~ s/&lt;/</g; 
      $body =~ s/&gt;/>/g; 
      $body =~ s/&quot;/"/g;
   }
   else {
      $errorflag = 2;
      $body = "";
   }

   $hidden_body = "$body";
   $hidden_body =~ s/</&lt;/g;
   $hidden_body =~ s/>/&gt;/g;
   $hidden_body =~ s/"/&quot;/g;

   ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

   if ($sec < 10) {
      $sec = "0$sec";
   }
   if ($min < 10) {
      $min = "0$min";
   }
   if ($hour < 10) {
      $hour = "0$hour";
   }
   if ($mon < 10) {
      $mon = "0$mon";
   }
   if ($mday < 10) {
      $mday = "0$mday";
   }
   $year += 1900;
   $year =~ s/^\d\d//;
   $month = ($mon + 1);

   if ($use_time == 1) {
      $date = "$hour\:$min\:$sec $month/$mday/$year";
   }
   else {
      $date = "$month/$mday/$year";
   }
   chop($date) if ($date =~ /\n$/);

   $long_date = "$month/$mday/$year at $hour\:$min";		# Switch to shorter format
}      

###############################
# View Post Subroutine Add-On #
###############################
sub open_log {							# Helper to avoid opening log before needed.
	return if ($logfile eq "");
	$logfile = ">>$basedir/$logfile";
	open(LOG,$logfile);
	$logfile = "";
}

sub view_post {

# Don't allow the hacker to post.
#    $remote_addr = $ENV{'REMOTE_ADDR'};
#    if ( $remote_addr =~ /205\.130\.32\./) { 
#	open_log();
#	print LOG "Forbidden poster access at $long_date from host: $ENV{'REMOTE_HOST'} Address: $ENV{'REMOTE_ADDR'}\n"; 
#	print LOG "$body\n";
#	die(); }

    $preview_title = "Review Your Message"; 
    if ($errorflag) { $preview_title = "Please Enter Missing Information"; }

# Screen message for things to object to, like no text entered in reply, or
# violation of for-sale/want-to-buy posting netiquette.

   if ($followup) {
        if ($body =~ /^(?!:)/ || $body =~ /<(p|br)>(?!(:|$))/ ) { }
          else {        $no_reply_text = 1;
                        $preview_title = "No Text Entered";
        }               }
   if ($screen_for_sale) {
        if ($followup) {
           if ($origsubject =~ /(for sale|wanted|want to buy)/i && $origemail) {
                $preview_title = "Can You Email This Instead?";
                $for_sale_text = "Is this a reply to a For Sale or Want to Buy message? \
To conserve resources, <a href=\"$baseurl/$faqfile$screen_for_sale\">our rules</a> suggest that you\
reply to such messages by <a href=\"mailto:$origemail\">mailing to the poster</a> instead.";
           }    }
         elsif ($subject =~ /(for sale|wanted|want to buy)/i && !$email) {
                $preview_title = "Please Include Email Address";
                $for_sale_text = "Is this a For Sale or Want to Buy message? \
According to <a href=\"$baseurl/$faqfile$screen_for_sale\">our rules</a>, we'd really like you to include an \
email address so people don't have to post messages to reply.\n";
   }            }

   print "Content-type: text/html\n\n";

   # Bug fix - 1/23/97 - replace quotes to get past WebSurfer
   $diddled_body = $hidden_body;
   $diddled_body =~ s/&quot;/~qq~/g;

   print "<html><head><title>$preview_title</title></head>\n";
   print "<body $background>\n";
# Debug - print the form args now
   if ($debugargs == 1) {
      $debugargs = 2;
      &parse_form;
   }
   print "<p><center><h1><b>$preview_title</b></h1></center>\n";
   if ($for_sale_text) {
	print "<p><center><b>$for_sale_text</b></center>\n";
	}
   if ($no_reply_text) {
	print "<p><center><b>You didn't enter any text in your reply.\n";
	print "<br>You may use your browser's [Back] button to do that now.\n";
	print "<p>(If you did enter text, make sure there wasn't a ':' at the start of your lines - that's used to indicate the original message text.</b></center>\n";
	}
    elsif ($errorflag) {
        print "<p><center><b>You may use your browser's [Back] button to make changes,\n";
        print "or fill in the missing data below before you</b></center>\n";
        }
     else { print "<p><center><b>You may use your browser's [Back] button to make changes, or</b></center>\n"; }
   print "<form method=POST action=\"$cgi_url?$board\">\n";
   print "<input type=hidden name=\"action\" value=\"post\">\n";
   if ($name ne "") { print "<input type=hidden name=\"name\" value=\"$name\">\n"; }
   if ($email ne "") { print "<input type=hidden name=\"email\" value=\"$email\">\n"; }
   if ($subject ne "") { print "<input type=hidden name=\"subject\" value=\"$subject\">\n"; }
   print "<input type=hidden name=\"body\" value=\"$diddled_body\">\n";
   print "<input type=hidden name=\"url\" value=\"$FORM{'url'}\">\n";
   print "<input type=hidden name=\"url_title\" value=\"$FORM{'url_title'}\">\n";
   print "<input type=hidden name=\"img\" value=\"$FORM{'img'}\">\n";
   print "<input type=hidden name=\"origsubject\" value=\"$FORM{'origsubject'}\">\n";
   print "<input type=hidden name=\"origname\" value=\"$FORM{'origname'}\">\n";
   print "<input type=hidden name=\"origemail\" value=\"$FORM{'origemail'}\">\n";
   print "<input type=hidden name=\"origdate\" value=\"$FORM{'origdate'}\">\n";
   print "<input type=hidden name=\"followup\" value=\"$FORM{'followup'}\">\n";
   if (!$no_reply_text) {					# If we're letting them post
     print "<p><center><input type=submit value=\"Post Your Message\"></center>\n";
     print "<p><center>(Please wait for post to complete - stopping and restarting can cause multiple posts.)</center>\n";
     }
   print "<hr size=3 width=75%>\n";
  
   print "<center><h1>$subject</h1></center>\n";
 if ($titles_only == 0) {
   print "<ul><li><b>Name:</b> ";
   if ($name ne "") { print $name; }
    else { print "<b>Missing - Fill in: </b><input type=text name=\"name\" size=50>"; }
   print "</li>\n<li><b>E-Mail: </b> ";
   if ($email ne "") { print $email; }
    else { print "(Missing or incorrect; you may fill in (optional): </b><input type=text name=\"email\" value=\"$FORM{'email'}\" size=30> )"; }
   print "</li>\n";
   print "<li><b>Subject:</b> ";
   if ($subject ne "") { print $subject; }
    else {
      print "<b>Missing - Fill in: </b><input type=text name=\"subject\" ";
      if ($followup != 0) { print "value=\"Re: $origsubject\" "; }
      print "size=50>";
      }
   print "</li>\n";
   if ($followup != 0) {
      print "<li><b>In Reply to:</b> <a href=\"$last_message\.$ext\">$origsubject</a> posted by ";
      if ($origemail) {
         print "<a href=\"$origemail\">$origname</a> on $origdate:</li>\n";
      }
      else {
         print "$origname on $origdate:</li>\n";
      }
   }
   print "</ul><p>\n";
   if ($message_img) {
      print "<center><img src=\"$message_img\"></center><p>\n";
   }
 }  # End if titles_only
#  print "$body<p>\n";
   &print_message_body;

   if ($message_url) {
      print "<b>Link:</b> <a href=\"$message_url\">$message_url_title</a>\n";
   }
   print "</form></body></html>\n";
   exit;
}

#####################
# New File Subroutine
#	Modified 4/99 Walt Bilofsky to also reconstruct and display a message
#		from the packed database (when $msg_to_dsp is the message number).

sub new_file {

   if (!$msg_to_disp) {						# Writing a file - open it
  	open(NEWFILE,">$basedir/$mesgdir/$num\.$ext") || die $!;
	}
   else {								# Displaying from database - prepare it
 	open(NEWFILE,'>-');					# Write to STDOUT.
	print NEWFILE "Content-type: text/html\n\n";
	}

   print NEWFILE "<html>\n";
   print NEWFILE "  <head>\n";
   print NEWFILE "    <title>$subject</title>\n";
# Modify to include the poster's broswer.
   print NEWFILE "    <meta name=\"generator\" content=\"";
   print NEWFILE $ENV{'HTTP_USER_AGENT'};
   print NEWFILE "\">\n";
# Following line prints info on poster
   if (!$use_logfile) {
	   print NEWFILE "<!-- Posted from Host: $ENV{'REMOTE_HOST'} Address: $ENV{'REMOTE_ADDR'} -->\n"; }

# Hack to put counter into message file.
#   if ( $board eq "cd" && open(DATA,"$counterfile")) {
#	$counter = <DATA>;
#	print NEWFILE "<!-- Counter $counter ";
#     print NEWFILE "Remote Host: $ENV{'REMOTE_HOST'} Remote Address: $ENV{'REMOTE_ADDR'} 
#	print NEWFILE -->\n";
#	}

  print NEWFILE "  </head>\n";
   print NEWFILE "  <body $background>\n";
   print NEWFILE "    <center>\n";
   print NEWFILE "      <h1>$subject</h1>\n";
   print NEWFILE "    </center>\n";
   print NEWFILE "<hr size=3 width=75%>\n";
 if ($titles_only == 0) {
   print NEWFILE "<center>";
   if (!msg_to_disp) {
	print NEWFILE "[&nbsp;<a href=\"#postfp\">Post&nbsp;a&nbsp;Reply</a>&nbsp;]\n";
	}
   print NEWFILE "[&nbsp;<a href=\"$baseurl/$mesglink\">$nbtitle</a>&nbsp;]\n";
   if ($show_faq == 1) {
      print NEWFILE "[&nbsp;<a href=\"$baseurl/$faqfile\">How&nbsp;to&nbsp;Use&nbsp;This&nbsp;Board</a>&nbsp;]\n";
      }
   print NEWFILE "</center>\n";
   print NEWFILE "<hr size=3 width=75%><p>\n<UL>\n";
 }  # End if titles_only

 if ($titles_only == 0) {
   print NEWFILE "<LI><em>Posted by: </em>";

   if ($email) {
      print NEWFILE "<a href=\"mailto:$email\">$name ($email)</a> on $long_date";
   }
   else {
      print NEWFILE "$name on $long_date";
   }
   if ($followup != 0) {
      print NEWFILE "</LI>\n<LI><em>In Reply to: </em><a href=\"$cgi_url?$board&$last_message\">$origsubject</a> posted by ";

      if ($origemail) {
         print NEWFILE "<a href=\"mailto:$origemail\">$origname</a> on $origdate\n";
      }
      else {
         print NEWFILE "$origname on $origdate\n";
      }
   }
   print NEWFILE "</LI></UL><p>\n";
   if ($message_img) {
      print NEWFILE "<center><img src=\"$message_img\"></center><p>\n";
   }
 }  # End if titles_only

#   print NEWFILE "$body\n";
# Modification to put old message in italics
   @chunks_of_body = split(/\&lt\;p\&gt\;/,$hidden_body);
   foreach $chunk_of_body (@chunks_of_body) {
      @lines_of_body = split(/\&lt\;br\&gt\;/,$chunk_of_body);
      foreach $line_of_body (@lines_of_body) {
# Walt 2/97: Restore punctuation (to allow HTML again)
         $line_of_body =~ s/&lt;/</g; 
         $line_of_body =~ s/&gt;/>/g; 
         $line_of_body =~ s/&quot;/"/g;
         if (index($line_of_body,":") == 0) { print NEWFILE "<i>$line_of_body</i>"; }
           else { print NEWFILE $line_of_body; }
         print NEWFILE "<br>\n";
      }
      print NEWFILE "<p>";
   }
   print NEWFILE "\n";

if ($titles_only == 0) {
   if ($message_url) {
      print NEWFILE "<ul><li><a href=\"$message_url\">$message_url_title</a></ul>\n";
   }
   print NEWFILE "<hr size=3 width=75%>\n";
   print NEWFILE "<a name=\"followups\"><i>Follow-ups:</i></a><br>\n";

#### Reconstruct and display followup from packed database.
   if ($msg_to_disp) {							# If displaying from database
	while ($followup_list =~ />(\d+)</) {			# Replace each msg number in followups
		$m_num = $1;
		if (($i = &get_packed_message($m_num)) == 2) {	# Get variables from the message
			&packed_msg_error; }				# Fatal error if garbled
		 elsif ($i == 1) { 					# May be missing
			$fup = "<i>(Deleted message)</i>"; }
		 else {							# Otherwise replace number with complete reference
              $fup = "<a href=\"$cgi_url?$board&$m_num\">$m_subject</a> <b>$m_name</b> <i>$m_date</i>\n";
		  }
		$followup_list =~ s/>$m_num</>$fup</;
		}
										# Fix remaining file refs to not point to cgi-bin
 	$followup_list =~ s/<a href=\"(\d+).$ext/<a href=\"$baseurl\/$mesgdir\/$1.$ext/g;
	print NEWFILE $followup_list;					# and print the list
      print NEWFILE "<br><hr size=3 width=75%><p>\n";
	print NEWFILE "<center><i><font size=-1>This is an archived message, so no more followups can be posted.\n";
	print NEWFILE "Post a new message instead.</i></font>\n</center><p>\n";
	}
   else {									# If building a file, do ALL this stuff
	print NEWFILE "<ul><!--$insert:$num-->\n";			# (matching '}' is WAY down)
      print NEWFILE "</ul><!--$end:$num-->\n";
      print NEWFILE "<br><hr size=3 width=75%><p>\n";
      print NEWFILE "<a name=\"postfp\"><i>Post a Follow-up:</i></a><p>\n";
      print NEWFILE "<form method=POST action=\"$cgi_url?$board\">\n";
      print NEWFILE "<input type=hidden name=\"followup\" value=\"";
      if ($followup != 0) {
         foreach $followup_num (@followup_num) {
           print NEWFILE "$followup_num,";
           }
	}
     print NEWFILE "$num\">\n";
     print NEWFILE "<input type=hidden name=\"origname\" value=\"$name\">\n";
     if ($email) {
        print NEWFILE "<input type=hidden name=\"origemail\" value=\"$email\">\n";
     }
     print NEWFILE "<input type=hidden name=\"origsubject\" value=\"$subject\">\n";
     print NEWFILE "<input type=hidden name=\"origdate\" value=\"$long_date\">\n";
     print NEWFILE "Name: <input type=text name=\"name\" size=50><br>\n";
     print NEWFILE "E-Mail: <input type=text name=\"email\" size=50><p>\n";
     if ($subject_line == 1) {
      if ($subject_line =~ /^Re:/) {
         print NEWFILE "<input type=hidden name=\"subject\" value=\"$subject\">\n";
         print NEWFILE "Subject: <b>$subject</b><p>\n";
      }
      else {
         print NEWFILE "<input type=hidden name=\"subject\" value=\"Re: $subject\">\n";
         print NEWFILE "Subject: <b>Re: $subject</b><p>\n";
      }
     } 
     elsif ($subject_line == 2) {
      print NEWFILE "Subject: <input type=text name=\"subject\" size=50><p>\n";
     }
     else {
      if ($subject =~ /^Re:/) {
         print NEWFILE "Subject: <input type=text name=\"subject\"value=\"$subject\" size=50><p>\n";
      }
      else {
         print NEWFILE "Subject: <input type=text name=\"subject\" value=\"Re: $subject\" size=50><p>\n";
      }
     }
     print NEWFILE "Comments:<br>\n";
     print NEWFILE "<textarea name=\"body\" WRAP=$body_wrap COLS=$body_width ROWS=10>\n";
     if ($quote_text == 1) {
      @chunks_of_body = split(/\&lt\;p\&gt\;/,$hidden_body);
      foreach $chunk_of_body (@chunks_of_body) {
         @lines_of_body = split(/\&lt\;br\&gt\;/,$chunk_of_body);
         foreach $line_of_body (@lines_of_body) {
            print NEWFILE ": $line_of_body\n";
         }
         print NEWFILE "\n";
      }
     }
     print NEWFILE "</textarea>\n";
     print NEWFILE "<p>\n";
     print NEWFILE "Optional Link URL: <input type=text name=\"url\" size=50><br>\n";
     print NEWFILE "Optional Link Title: <input type=text name=\"url_title\" size=48><br>\n";
     print NEWFILE "Optional Image URL: <input type=text name=\"img\" size=49><p>\n";
     print NEWFILE "<input type=submit value=\"Preview Your Message\"> <input type=reset>\n";
     print NEWFILE "</form>\n";
     print NEWFILE "<p><hr size=3 width=75%>\n";
     }									# End the code for writing a file, not screen
   print NEWFILE "<center>";
   if (!$msg_to_disp) {
	print NEWFILE "[&nbsp;<a href=\"#postfp\">Post&nbsp;a&nbsp;Reply</a>&nbsp;]\n";
	}
   print NEWFILE "[&nbsp;<a href=\"$baseurl/$mesglink\">$nbtitle</a>&nbsp;]\n";
   if ($show_faq == 1) {
      print NEWFILE "[&nbsp;<a href=\"$baseurl/$faqfile\">How&nbsp;to&nbsp;Use&nbsp;This&nbsp;Board</a>&nbsp;]\n";
      }
 }  # End if titles_only

 print NEWFILE "</body></html>\n";
 if (!$msg_to_disp) { 
	close(NEWFILE); 
	if ($use_logfile) {
		open_log();
		print LOG "$long_date: Message $num posted from host: $ENV{'REMOTE_HOST'} Address: $ENV{'REMOTE_ADDR'}\n"; 
		}
	}
}

###############################
# Email the new Post Subroutine

sub email_post {
  
   open(EMAIL,"$basedir/$subscribe") || &fatal_error("System error (mailing list)",
        "Your post <b>has</b> been added.  But there was an error emailing it to email subscribers. Don\'t worry - but please notify the message board's administrator.\n");

   @recipient = <EMAIL>;
   close(EMAIL);
   $recipient = "@recipient";
   $recipient =~ s/\n/ /g;

# Now send mail to $recipient
   open (MAIL, "|$mailprog $recipient") || &fatal_error("System error (mail program)",
        "Your post <b>has</b> been added.  But there was an error emailing it to email subscribers. Don\'t worry - but please notify the message board's administrator.\n");
   print MAIL "To: mailinglist\@toolworks.com\n";
   print MAIL "From: $title\@$domain\n";
   print MAIL "Subject: Message Posted - $subject\n";
   if ($mail_posts == 1) {		# If only printing summaries, don't allow reply-to
        print MAIL "Reply-To: $email\n";
        }
   print MAIL "This is in response to your request to be notified of new messages posted on the $title\n";
   print MAIL "  \n";
   print MAIL "$name posted ";
   print MAIL ($mail_posts == 1 ? "the following" : "a");
   print MAIL " message with the subject \"$subject\".\n";
   if ($mail_posts == 1) {
        print MAIL "  \n";
	  $body = $FORM{'body'};
        $body =~ s/<p>/\n\n/g;
        $body =~ s/<br>/\n/g;
        $body =~ s/~qq~/\"/g;
        print MAIL "$body\n\n";
	  if ($email) { print MAIL "Reply to: $email\n\n"; }
       }
   else {
        print MAIL "\nTo view the message, browse to: $baseurl/$mesgdir/$num\.$ext.\n\n";
       }
#   print MAIL "# Entered from $ENV{'REMOTE_HOST'} ($ENV{'REMOTE_ADDR'}) with $ENV{'SERVER_PROTOCOL'}.\n";
   print MAIL "\nTo unsubscribe to these mailings, browse to: $baseurl/$subscurl.\n";
   close (MAIL);
}

###############################
# Main WWWBoard Page Subroutine

sub main_page {

 $diddit = 0;
 foreach $mesgfile (@mesgfiles) {

   open(MAIN,"$basedir/$mesgfile") || die $!;
   @main = <MAIN>;
   close(MAIN);

   open(MAIN,">$basedir/$mesgfile") || die $!;

   if ($followup == 0) {
      foreach $main_line (@main) {
         if ($main_line =~ /<!--begin-->/) {
            print MAIN "<!--begin-->\n";
            print MAIN "<!--$top:$num--><li><a href=\"$mesgdir/$num\.$ext\">$subject</a>";
            if ($titles_only == 0) { 
                print MAIN " - <b>$name</b>";
                if ($FORM{'img'} && $pixicon) { print MAIN " <img src=\"$pixicon\">"; }
                if ($FORM{'url'} && $linkicon) { print MAIN " <img src=\"$linkicon\">"; }
                print MAIN " <i>$date</i>\n"; 
                print MAIN "(<!--$responses:$num-->0)\n";
                }
              else { print MAIN "<!--$responses:$num-->\n";}
            print MAIN "<ul><!--$insert:$num-->\n";
            print MAIN "</ul><!--$end:$num-->\n";
            $diddit = 1;
         }
         else {
            print MAIN "$main_line";
         }
      }
   }
   else {
      foreach $main_line (@main) {
         $work = 0;
         if ($main_line =~ /<ul><!--(i|insert): ?$last_message-->/) {
            print MAIN "<ul><!--$insert:$last_message-->\n";
            print MAIN "<!--$top:$num--><li><a href=\"$mesgdir/$num\.$ext\">$subject</a> - <b>$name</b>";
            if ($FORM{'img'} && $pixicon) { print MAIN " <img src=\"$pixicon\">"; }
            if ($FORM{'url'} && $linkicon) { print MAIN " <img src=\"$linkicon\">"; }
            print MAIN " <i>$date</i>\n";
            print MAIN "(<!--$responses:$num-->0)\n";
            print MAIN "<ul><!--$insert:$num-->\n";
            print MAIN "</ul><!--$end:$num-->\n";
            $diddit = 2;
         }
         elsif ($main_line =~ /<!--(r|responses): ?(.*)-->(.*)/) {
            $response_num = $2;
            $num_responses = $3;
            $num_responses++;
            foreach $followup_num (@followup_num) {
               if ($followup_num == $response_num) {
                  print MAIN "(<!--$responses:$followup_num-->$num_responses)\n";
                  $work = 1;
               }
            }
            if ($work != 1) {
               print MAIN "$main_line";
            }
         }
         else {
            print MAIN "$main_line";
         }
      }
   }

   close(MAIN);						# Also unlocks
   if ($diddit != 0) { return; }
 }
}  

############################################
# Add Followup Threading to Individual Pages
sub thread_pages {

   foreach $followup_num (@followup_num) {
      #Sanitize file name components for security purposes.
      $followup_num =~ m/^(\S+)$/ || die $!;  $followup_num = $1;

      open(FOLLOWUP,"$basedir/$mesgdir/$followup_num\.$ext");
      @followup_lines = <FOLLOWUP>;
      close(FOLLOWUP);

      open(FOLLOWUP,">$basedir/$mesgdir/$followup_num\.$ext");
      foreach $followup_line (@followup_lines) {
         $work = 0;
         if ($followup_line =~ /<ul><!--(i|insert): ?$last_message-->/) {
            print FOLLOWUP "<ul><!--$insert:$last_message-->\n";
            print FOLLOWUP "<!--$top:$num--><li><a href=\"$num\.$ext\">$subject</a> <b>$name</b>";
            if ($FORM{'img'} && $pixicon) { print FOLLOWUP " <img src=\"../$pixicon\">"; } 
            if ($FORM{'url'} && $linkicon) { print FOLLOWUP " <img src=\"../$linkicon\">"; }
            print FOLLOWUP " <i>$date</i>\n";
            print FOLLOWUP "(<!--$responses:$num-->0)\n";
            print FOLLOWUP "<ul><!--$insert:$num-->\n";
            print FOLLOWUP "</ul><!--$end:$num-->\n";
         }
         elsif ($followup_line =~ /<!--(r|responses): ?(.*)-->(.*)/) {
            $response_num = $2;
            $num_responses = $3;
            $num_responses++;
            foreach $followup_num (@followup_num) {
               if ($followup_num == $response_num) {
                  print FOLLOWUP "(<!--$responses:$followup_num-->$num_responses)\n";
                  $work = 1;
               }
            }
            if ($work != 1) {
               print FOLLOWUP "$followup_line";
            }
         }
         else {
            print FOLLOWUP "$followup_line";
         }
      }
      close(FOLLOWUP);
   }
}

############################################
# View recently posted messages
############################################
sub viewrecent {

  if ($FORM{'nposts'}) { $num_to_show = $FORM{'nposts'}; } 
  print "Content-type: text/html\n\n";
  print "<html><head><title>$title - $num_to_show Recent Messages</title></head>\n";
  print "<body $fbackground>\n";
  print "<center><h2>$title</h2></center>\n";
  if ($show_faq == 1) {
      print "<center>[ <a href=\"$baseurl/$posturl\">Post a New Message</a> ] [ <a href=\"$baseurl/$mesglink\">$title</a> ] [ <a href=\"$baseurl/$faqfile\">How to Use This Board</a> ]</center>\n";
   }
   else {
      print "<center>[ <a href=\"$baseurl/$posturl\">Post a New Message</a> ] [ <a href=\"$baseurl/$mesglink\">$title</a> ]</center>\n";
   }
  print "<hr size=3 width=75%><p>\n";
  print "<center><h1>Recent Messages</h1></center>\n";
  
  $messages = 0;
  print "<ol>\n";
  srchfiles: foreach $mesgfile (@mesgfiles) {
    open(MSGS,"$basedir/$mesgfile");
    @lines = <MSGS>;
    close(MSGS);
    foreach $line (@lines) {
      if ($line =~ /^<!--(t|top): ?(\d+)/) {
         if ($2 >= $num - $num_to_show) {
            $skey = $num + 1000 - $2;
            $fullpath = "$baseurl/$mesgdir";
            $line =~ s/$mesgdir/$fullpath/g;
            $line =~ s/img src=\"/img src=\"$baseurl\//g;
            push(@mlines, "<!--$skey--> $line");
            if (($messages += 1) >= $num_to_show) { last srchfiles; }
      }  }
  } }
  if ($messages == 0) { print "<p><center><h2>No Messages Posted Recently</h2></center>\n"; }
  else { print sort @mlines; }
  print "</ol>\n";
  print "</body></html>";
  exit;
}

sub return_html {
   print "Content-type: text/html\n\n";
   print "<html><head><title>Message Added: $subject</title></head>\n";
   print "<body $background>\n";
# Debug - print the form args now
   if ($debugargs == 1) {
      $debugargs = 2;
      &parse_form;
   }
   print "<center><h1>Message Added: $subject</h1></center>\n";
   print "The following information was added to the message board:<p><hr size=3 width=75%><p>\n";

   print "<ul><li><b>Name:</b> $name</li>\n";
   print "<li><b>E-Mail:</b> $email</li>\n";
   print "<li><b>Subject:</b> $subject</li>\n";
   if ($followup != 0) {
      print "<li><b>In Reply to:</b> <a href=\"$last_message\.$ext\">$origsubject</a> posted by ";
      if ($origemail) {
         print "<a href=\"$origemail\">$origname</a> on $origdate</li>\n";
      }
      else {
         print "$origname on $origdate</li>\n";
      }
   }
   print "</ul><p>\n";
   print "<b>Body of Message:</b><p>\n";

   &print_message_body;

   if ($message_url) {
      print "<b>Link:</b> <a href=\"$message_url\">$message_url_title</a><br>\n";
   }
   if ($message_img) {
      print "<b>Image:</b> <img src=\"$message_img\"><br>\n";
   }
   print "<b>Added on Date:</b> $date<p>\n";
   print "<hr size=3 width=75%>\n";
   print "<center>[ <a href=\"$baseurl/$mesgdir/$num\.$ext\">Go to Your Message</a>* ] [ <a href=\"$baseurl/$mesglink\">$title</a> ]</center>\n";
   print "<hr size=3 width=75%>\n";
   print "<p>* - When you return to the main page, if you don't see your message header in the list of messages,\n";
   print "try clicking the Reload button on your Web browser.\n"; 
   print "</body></html>\n";
}

sub fatal_error {
   ($why, $longwhy) = @_;

   print "Content-type: text/html\n\n";
   print "<html><head><title>$title ERROR: $why</title></head>\n";
   print "<body><center><h1>ERROR: $why</h1></center>\n";
   print "<p>$longwhy<p>\n";
   print "</body></html>\n";

   exit;
   }

sub check_arglen {
   ($avar, $aname, $alen) = @_;
   if (length($avar) > $alen) {
     &fatal_error("$aname is Too Long",
        "Sorry - $aname can't be longer than $alen characters.<p>Use the [Back] button in your browser to return to the previous page and make it shorter.");
   } }

sub error {

   print "Content-type: text/html\n\n";
   print "<html><head><title>$title ERROR: Required field missing</title></head>\n";

   if ($FORM{'name'} eq "") {
      print "<body><center><h1>ERROR: No Name</h1></center>\n";
      print "You forgot to fill in the 'Name' field in your posting.<p><hr size=3 width=75%><p>\n";
      }

   if ($FORM{'subject'} eq "") {
      print "<html><head><title>$title ERROR: No Subject</title></head>\n";
      print "<body><center><h1>ERROR: No Subject</h1></center>\n";
      print "You forgot to fill in the 'Subject' field in your posting.<p><hr size=3 width=75%><p>\n";
   }
   print "The necessary fields are: Name, Subject and Message.<p>\n";
   print "Use the [Back] button in your browser to return to the previous form and fill in the missing information.<p>\n";
   print "</body></html>\n";
   exit;
}

sub print_message_body {
   @chunks_of_body = split(/\&lt\;p\&gt\;/,$hidden_body);
   foreach $chunk_of_body (@chunks_of_body) {
      @lines_of_body = split(/\&lt\;br\&gt\;/,$chunk_of_body);
      foreach $line_of_body (@lines_of_body) {
# Walt 2/97: Restore punctuation (to allow HTML again)
         $line_of_body =~ s/&lt;/</g; 
         $line_of_body =~ s/&gt;/>/g; 
         $line_of_body =~ s/&quot;/"/g;
         if (index($line_of_body,":") == 0) { print "<i>$line_of_body</i>"; }
           else { print $line_of_body; }
         print "<br>\n";
      }
      print "<p>";
   }
}
