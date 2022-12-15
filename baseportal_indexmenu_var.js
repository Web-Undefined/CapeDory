/***********************************************************************************
*	(c) Ger Versluis 2000 version 5.41 24 December 2001	          *
*	For info write to menus@burmees.nl		          *
*	You may remove all comments for faster loading	          *		
***********************************************************************************/

	var NoOffFirstLineMenus=12;			// Number of first level items
	var LowBgColor='#000099';			// Background color when mouse is not over
	var LowSubBgColor='#000099';			// Background color when mouse is not over on subs
	var HighBgColor='#CC0000';			// Background color when mouse is over
	var HighSubBgColor='#CC0000';			// Background color when mouse is over on subs
	var FontLowColor='white';			// Font color when mouse is not over
	var FontSubLowColor='white';			// Font color subs when mouse is not over
	var FontHighColor='white';			// Font color when mouse is over
	var FontSubHighColor='white';			// Font color subs when mouse is over
	var BorderColor='white';			// Border color
	var BorderSubColor='white';			// Border color for subs
	var BorderWidth=1;				// Border width
	var BorderBtwnElmnts=1;			// Border between elements 1 or 0
	var FontFamily="Verdana, Arial, Helvetica, sans-serif"	// Font family menu items
	var FontSize=8;				// Font size menu items
	var FontBold=1;				// Bold menu items 1 or 0
	var FontItalic=0;				// Italic menu items 1 or 0
	var MenuTextCentered='left';			// Item text position 'left', 'center' or 'right'
	var MenuCentered='left';			// Menu horizontal position 'left', 'center' or 'right'
	var MenuVerticalCentered='static';		// Menu vertical position 'top', 'middle','bottom' or static
	var ChildOverlap=.012;				// horizontal overlap child/ parent
	var ChildVerticalOverlap=.125;			// vertical overlap child/ parent
	var StartTop=155;				// Menu offset x coordinate
	var StartLeft=10;				// Menu offset y coordinate
	var VerCorrect=0;				// Multiple frames y correction
	var HorCorrect=0;				// Multiple frames x correction
	var LeftPaddng=3;				// Left padding
	var TopPaddng=2;				// Top padding
	var FirstLineHorizontal=0;			// SET TO 1 FOR HORIZONTAL MENU, 0 FOR VERTICAL
	var MenuFramesVertical=1;			// Frames in cols or rows 1 or 0
	var DissapearDelay=1000;			// delay before menu folds in
	var TakeOverBgColor=1;			// Menu frame takes over background color subitem frame
	var FirstLineFrame='navig';			// Frame where first level appears
	var SecLineFrame='space';			// Frame where sub levels appear
	var DocTargetFrame='space';			// Frame where target documents appear
	var TargetLoc='';				// span id for relative positioning
	var HideTop=0;				// Hide first level when loading new document 1 or 0
	var MenuWrap=1;				// enables/ disables menu wrap 1 or 0
	var RightToLeft=0;				// enables/ disables right to left unfold 1 or 0
	var UnfoldsOnClick=0;			// Level 1 unfolds onclick/ onmouseover
	var WebMasterCheck=0;			// menu tree checking on or off 1 or 0
	var ShowArrow=1;				// Uses arrow gifs when 1
	var KeepHilite=1;				// Keep selected path highligthed
	var Arrws=['http://www.capedory.org/tri.gif',5,10,'http://www.capedory.org/tridown.gif',10,5,'http://www.capedory.org/trileft.gif',5,10];	// Arrow source, width and height

function BeforeStart(){return}
function AfterBuild(){return}
function BeforeFirstOpen(){return}
function AfterCloseAll(){return}


// Menu tree
//	MenuX=new Array(Text to show, Link, background image (optional), number of sub elements, height, width);
//	For rollover images set "Text to show" to:  "rollover:Image1.jpg:Image2.jpg"

Menu1=new Array("Home","http://www.capedory.org/index.html","",0,20,160);

Menu2=new Array("Member Benefits","http://www.capedory.org/benefits.html","",0);
	
Menu3=new Array("News & Events","http://www.capedory.org/events.html","",3);
	Menu3_1=new Array("General Events","http://www.capedory.org/genevents.html","",0,20,160);
	Menu3_2=new Array("Fleet Events","http://www.capedory.org/events.html","",5);
		Menu3_2_1=new Array("Carolinas","http://www.capedory.org/events.html#CarolinasEvents","",0,20,180);
		Menu3_2_2=new Array("Chesapeake","http://www.capedory.org/events.html#ChesapeakeEvents","",0);
		Menu3_2_3=new Array("Great Lakes","http://www.capedory.org/events.html#GLFLeetEvents","",0);
		Menu3_2_4=new Array("Gulf Coast","http://www.capedory.org/events.html#GCFleetEvents","",0);
		Menu3_2_5=new Array("Northeast","http://www.capedory.org/events.html#NEFleetEvents","",0);
	Menu3_3=new Array("News","http://www.capedory.org/news.html","",0);

Menu4=new Array("Fleets","http://www.capedory.org/fleets.html","",5);
	Menu4_1=new Array("Carolinas","http://www.capedory.org/fleets.html#FleetCarolinas","",0,20,160);
	Menu4_2=new Array("Chesapeake","http://www.capedory.org/fleets.html#FleetChesapeake","",0);
	Menu4_3=new Array("Great Lakes","http://www.capedory.org/fleets.html#FleetGreatLakes","",0);
	Menu4_4=new Array("Gulf Coast","http://www.capedory.org/fleets.html#FleetGulfCoast","",0);
	Menu4_5=new Array("Northeast","http://www.capedory.org/fleets.html#FleetNortheast","",0);

Menu5=new Array("Chandlery","http://www.capedory.org/stuff.html","",7);
	Menu5_1=new Array("CDSOA Logo Items","http://www.capedory.org/stuff.html","",0,20,160);
	Menu5_2=new Array("Non-CDSOA Logo Items","http://www.capedory.org/stuff.html#moreCDstuff","",0);
	Menu5_3=new Array("Books","http://www.capedory.org/stuff.html#moreCDstuff","",0);
	Menu5_4=new Array("Half Hull Scale Models","http://www.capedory.org/stuff.html#moreCDstuff","",0);
	Menu5_5=new Array("Port Rain Shields","http://www.capedory.org/stuff.html#moreCDstuff","",0);
	Menu5_6=new Array("Bronze Port Screens","http://www.capedory.org/stuff.html#moreCDstuff","",0);
	Menu5_7=new Array("Builders Plates","http://www.capedory.org/stuff.html#moreCDstuff","",0);
	

Menu6=new Array("Where to Look","http://www.capedory.org/cdsoalook.html","",9);
	Menu6_1=new Array("Groups & Publications","http://www.capedory.org/cdsoalook-groupsNpubs.html","",5,32,208);
		Menu6_1_1=new Array("Magazine Articles & Reviews","http://www.capedory.org/cdsoalook-groupsNpubs.html#magarticles","",0,32,208);
		Menu6_1_2=new Array("Online Manuals & Brochures","http://www.capedory.org/cdsoalook-groupsNpubs.html#onlinemanuals","",5);
			Menu6_1_2_1=new Array("CD Owners Manuals","http://www.capedory.org/cdsoalook-groupsNpubs.html#onlinemanuals","",0,32,180);
			Menu6_1_2_2=new Array("Engine/Transmission Manuals","http://www.capedory.org/cdsoalook-groupsNpubs.html#enginemanuals","",0);
			Menu6_1_2_3=new Array("Other Online Engine Resources","http://www.capedory.org/cdsoalook-groupsNpubs.html#enginesonline","",0);
			Menu6_1_2_4=new Array("Line Drawings","http://www.capedory.org/cdsoalook-groupsNpubs.html#linedrawings","",0);
			Menu6_1_2_5=new Array("Cradle/Trailer Plans","http://www.capedory.org/cdsoalook-groupsNpubs.html#cradleplans","",0);
		Menu6_1_3=new Array("Other Cape Dory Groups & Publications","http://www.capedory.org/cdsoalook-groupsNpubs.html#GroupsPubs","",0);
		Menu6_1_4=new Array("Other Owners Associations for Alberg-designed Boats","http://www.capedory.org/cdsoalook-groupsNpubs.html#ownersassoc","",0);
		Menu6_1_5=new Array("Special Sailing/Boating Programs","http://www.capedory.org/cdsoalook-groupsNpubs.html#BoatingPrograms","",0);
	Menu6_2=new Array("Parts & Supplies","http://www.capedory.org/cdsoalook.html","",7);
		Menu6_2_1=new Array("Most Requested CD Parts & Supplies","http://www.capedory.org/cdsoalook.html#PartsSupplies","",0,32,208);
		Menu6_2_2=new Array("Mfrs. of Orig. Equipment","http://www.capedory.org/cdsoalook-suppliers.html","",0);
		Menu6_2_3=new Array("Alternative Mfrs. of Marine Equipment","http://www.capedory.org/cdsoalook-alt_suppliers.html","",0);
		Menu6_2_4=new Array("Marine Stores","http://www.capedory.org/cdsoalook-stores.html","",4);
			Menu6_2_4_1=new Array("Boating Equipment & Supplies","http://www.capedory.org/cdsoalook-stores.html#boatingsupplies","",0,32,180);
			Menu6_2_4_2=new Array("Spars & Rigging","http://www.capedory.org/cdsoalook-stores.html#rigging","",0);
			Menu6_2_4_3=new Array("Navigational Needs","http://www.capedory.org/cdsoalook-stores.html#navneeds","",0);
			Menu6_2_4_4=new Array("Rent or Buy Used","http://www.capedory.org/cdsoalook-stores.html#rentals","",0);
		Menu6_2_5=new Array("Sailmakers","http://www.capedory.org/cdsoalook-sailmakers.html","",0);
		Menu6_2_6=new Array("Teak Lumber & Plywood","http://www.capedory.org/cdsoalook-teak.html","",0);
		Menu6_2_7=new Array("Related Cape Dory Businesses","http://www.capedory.org/cdsoalook.html#CDbusinesses","",0);
	Menu6_3=new Array("Animated Knots by Grog <img src='http://www.capedory.org/images/www.gif'>","http://www.animatedknots.com/indexboating.php?LogoImage=LogoCapeDory.jpg&Website=www.capedory.org","",0);
	Menu6_4=new Array("Buy or Sell your boat or used gear","http://www.capedory.org/cdsoalook-boats4sale.html","",0);
	Menu6_5=new Array("Boat Transport","http://www.capedory.org/cdsoalook-boats4sale.html#boat_transport","",0);
	Menu6_6=new Array("PHRF Handicaps","http://www.capedory.org/phrf.html","",0);
	Menu6_7=new Array("Renaming Your CD <img src='http://www.capedory.org/images/www.gif'>","http://www.48north.com/mr_offline/denaming.htm","",0);
	Menu6_8=new Array("U.S. Coast Guard, Safety Resources & Weather","http://www.capedory.org/CG-safety.html","",2);
		Menu6_8_1=new Array("U.S. Coast Guard & Marine Safety","http://www.capedory.org/CG-safety.html#USCG","",0,32,180);
		Menu6_8_2=new Array("Weather & Navigation Resources","http://www.capedory.org/CG-safety.html#WeatherNav","",0);
	Menu6_9=new Array("CDSOA Link Exchange","http://www.capedory.org/cd-link-exchange.html","",0);
	
Menu7=new Array("CD Message Board","http://www.capedory.org/board/","",0);

Menu8=new Array("Cape Dory Info","http://www.capedory.org/cdinfo.html","",4);
	Menu8_1=new Array("History of CD Yachts","http://www.capedory.org/cdinfo.html#history","",0,20,208);
	Menu8_2=new Array("Manufacturing History","http://www.capedory.org/cdmfd.html","",0);
	Menu8_3=new Array("Current State of Manufacture","http://www.capedory.org/cdinfo.html#mfr","",0);
	Menu8_4=new Array("CD Boat Specs","http://www.capedory.org/cdinfo.html#specs","",2);
		Menu8_4_1=new Array("Performance Statistics Compared  <img src='http://www.capedory.org/images/www.gif'>","http://www.image-ination.com/sailcalc.html","",0,40,208);
		Menu8_4_2=new Array("Performance Terms Explained  <img src='http://www.capedory.org/images/www.gif'>","http://www.johnsboatstuff.com/Articles/design.htm","",0);

Menu9=new Array("CD Owners Web Sites","http://www.capedory.org/cdownersweb.html","",0);

Menu10=new Array("Cape Dory Registry <img src='http://www.capedory.org/images/www.gif'>","http://baseportal.com/cgi-bin/baseportal.pl?htx=/CDSOA/CD_Boat_Registry","",0,35,160);

Menu11=new Array("Contact Us","http://www.capedory.org/contactus.html","",0,20,160);

Menu12=new Array("<img src='http://www.capedory.org/images/30drawing_trans.gif' width='160' height='211'>","http://www.capedory.org/cdinfo.html#specs","",0,211,160);