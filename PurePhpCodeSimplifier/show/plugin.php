<?php
//
// ZoneMinder web zone view file, $Date$, $Revision$
// Copyright (C) 2001-2008 Philip Coombes
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//


if ( !canView( 'Monitors' ) )
{
    $view = "error";
    return;
}

$mid = validInt($_REQUEST['mid']);
$zid = !empty($_REQUEST['zid'])?validInt($_REQUEST['zid']):0;


if ( $zid > 0 ) {
   $newZone = dbFetchOne( 'SELECT * FROM Zones WHERE MonitorId = ? AND Id = ?', NULL, array( $mid, $zid) );
} else {
   $view = "error";
   return;
}
$monitor = dbFetchMonitor ( $mid );
// Only allow certain filename characters (not including a period) to prevent directory traversal.
$plugin = preg_replace('/[^-a-zA-Z0-9]/', '', $_REQUEST['pl']);

$plugin_path = dirname(ZM_PLUGINS_CONFIG_PATH)."/".$plugin;

$focusWindow = true;

xhtmlHeaders(__FILE__, translate('Plugin') );


$pluginOptions=array(
    'Enabled'=>array(
          'Type'=>'select',
          'Name'=>'Enabled',
          'Choices'=>'yes,no',
          'Value'=>'no'
          )
     );

$optionNames=array();
if(file_exists($plugin_path."/config.php"))
{
   include_once($plugin_path."/config.php");
}

$sql='SELECT * FROM PluginsConfig WHERE MonitorId=? AND ZoneId=? AND pluginName=?';
foreach( dbFetchAll( $sql, NULL, array( $mid, $zid, $plugin ) ) as $popt )
{
   if(array_key_exists($popt['Name'], $pluginOptions)
      && $popt['Type']==$pluginOptions[$popt['Name']]['Type']
      && $popt['Choices']==$pluginOptions[$popt['Name']]['Choices']
      )
   {
      $pluginOptions[$popt['Name']]=$popt;
      array_push($optionNames, $popt['Name']);
   } else {
      dbQuery('DELETE FROM PluginsConfig WHERE Id=?', array( $popt['Id'] ) );
   }
}
foreach($pluginOptions as $name => $values)
{
   if(!in_array($name, $optionNames))
   {
      $popt=$pluginOptions[$name];
      $sql="INSERT INTO PluginsConfig VALUES ('',?,?,?,?,?,?,?)";
      dbQuery($sql, array( $popt['Name'], $popt['Value'], $popt['Type'], $popt['Choices'], $mid, $zid, $plugin ) );
   }
}

$PLANG=array();
if(file_exists($plugin_path."/lang/".$user['Language'].".php")) {
   include_once($plugin_path."/lang/".$user['Language'].".php");
}

function pLang($name)
{
   global $PLANG;
   if(array_key_exists($name, $PLANG))
      return $PLANG[$name];
   else
      return $name;
}






echo translate('Monitor');echo $monitor['Name'];echo translate('Zone');echo $newZone['Name'];echo translate('Plugin');echo validHtmlStr($plugin);


echo $_SERVER['PHP_SELF'];
echo $view;

echo $mid;
echo $zid;
echo validHtmlStr($plugin);





foreach($pluginOptions as $name => $popt)
{
   
echo pLang($name);
   
   switch($popt['Type'])
   {
      case "checkbox":
         echo "CHECKBOX";
         break;
      case "select":
         $pchoices=explode(',',$popt['Choices']);
            

echo $popt['Name'];echo $popt['Name'];
            
            foreach($pchoices as $pchoice)
            {
               $psel="";
               if($popt['Value']==$pchoice)
                  $psel="selected";
               
echo $pchoice;echo $psel;echo pLang($pchoice);
               
            }
            


         
         break;
      case "text":
      default:
         echo "DEFAULT";
   }
   

   
}



echo translate('Save');if (!canEdit( 'Monitors' ) || (false && $selfIntersecting)) {;};
echo translate('Cancel');






?>