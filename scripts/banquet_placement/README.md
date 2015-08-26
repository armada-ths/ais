# Banquet Placement
<pre>
This is the placement generator for the Niwen legacy system.

How to use:
1. Make sure that the blackbox placement algorithm is running,
   by SSH:ing into niwen.armada.nu (falken.armada.nu) and going to 
   /var/www/bordsplacering.armada.nu/www/ and typing the command 
   "rackup". This can be put in a linux 'screen' to keep the server 
   running.

2. Get gasque_attendances.json from the Banquet/Export to placement 
   button in Niwen. Save to this folder.

3. Get gasque_tables.json from the Banquet/Tables/Export Tables to 
   placement button in Niwen. Save to this folder.

4. Run the script with "python banquet_placement.py"

5. This will take about 10-15 minutes depending on the number of people 
   attending.

6. An output file "placement.json" will be generated, copy the content 
   of this file into the "Import placement" window, as text.
   (The window says "ID in order of placement (comma separated)",
   That is not correct)

7. All done!
