/***********************************************************************************
*	(c) Ger Versluis 2000 version 5.41 24 December 2001	          *
*	For info write to menus@burmees.nl		          *
*	You may remove all comments for faster loading	          *		
***********************************************************************************/

	var NoOffFirstLineMenus=13;			// Number of first level items
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
	var StartTop=190;				// Menu offset x coordinate
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
	var Arrws=['../tri.gif',5,10,'../tridown.gif',10,5,'../trileft.gif',5,10];	// Arrow source, width and height

function BeforeStart(){return}
function AfterBuild(){return}
function BeforeFirstOpen(){return}
function AfterCloseAll(){return}


// Menu tree
//	MenuX=new Array(Text to show, Link, background image (optional), number of sub elements, height, width);
//	For rollover images set "Text to show" to:  "rollover:Image1.jpg:Image2.jpg"

Menu1=new Array("Home","../index.html","",0,20,160);

Menu2=new Array("Member Benefits","../benefits.html","",0);
	
Menu3=new Array("News & Events","../events.html","",4);
	Menu3_1=new Array("General Events","../genevents.html","",0,20,160);
	Menu3_2=new Array("Fleet Events","../events.html","",5);
		Menu3_2_1=new Array("Carolinas","../events.html#CarolinasEvents","",0,20,180);
		Menu3_2_2=new Array("Southeast","../events.html#CentralGulfEvents","",0);
		Menu3_2_3=new Array("Chesapeake","../events.html#ChesapeakeEvents","",0);
		Menu3_2_4=new Array("Gulf Coast","../events.html#GCFleetEvents","",0);
		Menu3_2_5=new Array("Northeast","../events.html#NEFleetEvents","",0);
	Menu3_3=new Array("News","../news.html","",0);
	Menu3_4=new Array("MASTHEAD","https://cdsoamasthead.org/","",0);

Menu4=new Array("Fleets","../fleets.html","",5);
	Menu4_1=new Array("Carolinas","../fleets.html#FleetCarolinas","",0,20,160);
	Menu4_2=new Array("Southeast","../fleets.html#FleetCentralGulf","",0);
	Menu4_3=new Array("Chesapeake","../fleets.html#FleetChesapeake","",0);
	Menu4_4=new Array("Gulf Coast","../fleets.html#FleetGulfCoast","",0);
	Menu4_5=new Array("Northeast","../fleets.html#FleetNortheast","",0);

Menu5=new Array("Alberg Fellows","../AlbergFellows.html","",0);
	
Menu6=new Array("Chandlery Items <img src='../images/www.gif'>","http://www.companycasuals.com/CDSOAchandlery/start.jsp","",2,35,60);
	Menu6_1=new Array("CDSOA Chandlery","http://www.companycasuals.com/CDSOAchandlery/start.jsp","",0,20,160);
	Menu6_2=new Array("More Cape Dory Stuff","../more_cd_stuff.html","",0);
	
Menu7=new Array("Where to Look","../cdsoalook.html","",9);
	Menu7_1=new Array("Groups & Publications","../cdsoalook-groupsNpubs.html","",5,36,208);
		Menu7_1_1=new Array("Magazine Articles & Reviews","../cdsoalook-groupsNpubs.html#magarticles","",0,32,208);
		Menu7_1_2=new Array("Online Manuals & Brochures","../cdsoalook-groupsNpubs.html#onlinemanuals","",6);
			Menu7_1_2_1=new Array("CD Owners Manuals","../cdsoalook-groupsNpubs.html#onlinemanuals","",0,32,180);
			Menu7_1_2_2=new Array("CD Sales Brochures","../cdsoalook-groupsNpubs.html#salesbrochures","",0);
			Menu7_1_2_3=new Array("Engine/Transmission Manuals","../cdsoalook-groupsNpubs.html#enginemanuals","",0);
			Menu7_1_2_4=new Array("Other Online Engine Resources","../cdsoalook-groupsNpubs.html#enginesonline","",0);
			Menu7_1_2_5=new Array("Line Drawings","../cdsoalook-groupsNpubs.html#linedrawings","",0);
			Menu7_1_2_6=new Array("Cradle/Trailer Plans","../cdsoalook-groupsNpubs.html#cradleplans","",0);
		Menu7_1_3=new Array("Other Cape Dory Groups & Publications","../cdsoalook-groupsNpubs.html#GroupsPubs","",0);
		Menu7_1_4=new Array("Other Owners Associations for Alberg-designed Boats","../cdsoalook-groupsNpubs.html#ownersassoc","",0);
		Menu7_1_5=new Array("Special Sailing/Boating Programs","../cdsoalook-groupsNpubs.html#BoatingPrograms","",0);
	Menu7_2=new Array("Parts & Supplies","../cdsoalook.html","",7);
		Menu7_2_1=new Array("Most Requested CD Parts & Supplies","../cdsoalook.html#PartsSupplies","",0,32,208);
		Menu7_2_2=new Array("Mfrs. of Orig. Equipment","../cdsoalook-suppliers.html","",0);
		Menu7_2_3=new Array("Alternative Mfrs. of Marine Equipment","../cdsoalook-alt_suppliers.html","",0);
		Menu7_2_4=new Array("Marine Stores","../cdsoalook-stores.html","",5);
			Menu7_2_4_1=new Array("Boating Equipment & Supplies","../cdsoalook-stores.html#boatingsupplies","",0,32,180);
			Menu7_2_4_2=new Array("Spars & Rigging","../cdsoalook-stores.html#rigging","",0);
			Menu7_2_4_3=new Array("Navigational Needs","../cdsoalook-stores.html#navneeds","",0);
			Menu7_2_4_4=new Array("Consignment Shops","../cdsoalook-stores.html#consignment","",0);
			Menu7_2_4_5=new Array("Rent or Buy Used","../cdsoalook-stores.html#rentals","",0);
		Menu7_2_5=new Array("Sailmakers & Canvas Shops","../cdsoalook-sailmakers.html","",0);
		Menu7_2_6=new Array("Teak Lumber & Plywood","../cdsoalook-teak.html","",0);
		Menu7_2_7=new Array("Related Cape Dory Businesses","../cdsoalook.html#CDbusinesses","",0);
	Menu7_3=new Array("Animated Knots by Grog <img src='../images/www.gif'>","http://www.animatedknots.com/indexboating.php?LogoImage=LogoCapeDory.jpg&Website=www.capedory.org","",0);
	Menu7_4=new Array("New England Ropes Splicing Guides <img src='../images/www.gif'>","http://www.neropes.com/SplicingGuideChoice.aspx","",0);
	Menu7_5=new Array("Boats/Gear For Sale, Wanted and Boat Transport","../cdsoalook-boats4sale.html","",4);
		Menu7_5_1=new Array("Buy or Sell your boat or used gear","../cdsoalook-boats4sale.html","",0,32,180);
		Menu7_5_2=new Array("Boat Transport","../cdsoalook-boats4sale.html#boat_transport","",0);
		Menu7_5_3=new Array("Trailer Manufacturers","../cdsoalook-boats4sale.html#trailermfrs","",0);
		Menu7_5_4=new Array("Delivery Skippers","../cdsoalook-boats4sale.html#deliveryskippers","",0);
	Menu7_6=new Array("PHRF Handicaps","../phrf.html","",0);
	Menu7_7=new Array("Renaming Your CD <img src='../images/www.gif'>","http://www.48north.com/mr_offline/denaming.htm","",0);
	Menu7_8=new Array("U.S. Coast Guard, Safety Resources & Weather","../CG-safety.html","",2);
		Menu7_8_1=new Array("U.S. Coast Guard & Marine Safety","../CG-safety.html#USCG","",0,32,180);
		Menu7_8_2=new Array("Weather & Navigation Resources","../CG-safety.html#WeatherNav","",0);
	Menu7_9=new Array("CDSOA Link Exchange","../cd-link-exchange.html","",0);
	
Menu8=new Array("CD Message Board","../board/","",0);

Menu9=new Array("Cape Dory Info","../cdinfo.html","",4);
	Menu9_1=new Array("History of CD Yachts","../cdinfo.html#history","",0,20,208);
	Menu9_2=new Array("Manufacturing History","../cdmfd.html","",0);
	Menu9_3=new Array("Current State of Manufacture","../cdinfo.html#mfr","",0);
	Menu9_4=new Array("CD Boat Specs","../cdinfo.html#specs","",2);
		Menu9_4_1=new Array("Performance Statistics Compared  <img src='../images/www.gif'>","http://www.image-ination.com/sailcalc.html","",0,40,208);
		Menu9_4_2=new Array("Performance Terms Explained  <img src='../images/www.gif'>","http://www.johnsboatstuff.com/Articles/design.htm","",0);

Menu10=new Array("CD Owners Web Sites","../cdownersweb.html","",0);

Menu11=new Array("Cape Dory Registry <img src='../images/www.gif'>","https://docs.google.com/spreadsheets/d/1rlZWL3SOxA_hDbODuP_5K1SId78-900Cy4sbWntDxn8/edit?pli=1#gid=0","",0,35,160);

Menu12=new Array("Contact Us","../contactus.html","",0,20,160);

Menu13=new Array("<img src='../images/30drawing_trans.gif' width='160' height='211'>","../cdinfo.html#specs","",0,211,160);