You'll need a json file with all the hotspots in it, you can get this by going to https://etl.dewi.org and signing up or logging in.

![image](https://user-images.githubusercontent.com/88957612/215394022-cac18106-5602-4419-a74c-a8a0faa979f8.png)

After this youll want to click the "+ New" on the top right and select "SQL Query".

![image](https://user-images.githubusercontent.com/88957612/215394201-509375ed-bb34-4b7d-94bc-766eb344d760.png)

Then on line one paste in:
---------------------------------------------------------------------
SELECT gi.*, l.*, st_x(l.geometry) AS long, st_y(l.geometry) AS lat
FROM gateway_inventory gi
INNER JOIN locations l ON gi.location = l.location;
---------------------------------------------------------------------
Then click on the blue play button 

![image](https://user-images.githubusercontent.com/88957612/215394367-6fed0a78-a44b-4a14-b443-b8db5b1f997b.png)

After that you should see on the bottom right a cloud icon, click it and choose JSON 

![image](https://user-images.githubusercontent.com/88957612/215394440-5827a011-7acc-440d-a5c4-492e1fff4d08.png)

Now once that file saves you want to move it to the same directory as the rest of the files, it should look like this

![image](https://user-images.githubusercontent.com/88957612/215394595-b2a79716-9cc4-4238-97da-d7c64ea04229.png)

Now you'll want to install these libraries: flask, folium, json, requests, and math.
Then just run "webapp.py" and search "http://localhost:5000/" inside of your browser.
