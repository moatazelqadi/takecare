% rebase('layout.tpl', title=title, year=year)

<h2>{{ title }}.</h2>


<p><h3>The problem</h3>
When I got out of my home in the southeast to visit a friend in Point cook, Google maps app was smart enough to notice a 5 minutes delay in the city. Not a big deal, right?
By the time I reached the CONGESTION, it took my 1 hour to get through. The maps app noticed that drivers were moving slow at that point, but didn't know that there is an underlying cause: a road incident that is causing more and more delay.
<br/>
I wanted to avoid these situations, so I created the "Take Care"  app.  A mobile friendly web application. The idea is to check the driving route ahead: check for road closures (reported by Vicroads) Check for other emergencies (like fallen trees or fire incidents), and also check for unfavourable weather (thunderstorms, damaging hail, etc…) and even for accident hotspots, the reason behind the last one being an accident I had on my way home 30 minutes after buying my car (it wasn't my fault, but at least on the first day, I'd really like to avoid accident hotspots).
</p>
<p><h3>The solution</h3>
The Take care! application is built as a web interface, and a server backend. The web interface uses Google maps to route between 2 addresses. The route is then sent to the application backend which converts the route into different GIS formats (For example Open WFS, and ESRI Feature Layer using different coordinate systems). The server then checks for problems along the route using APIs, and returns the report to the web interface that displays it.
</p>
<p><h3>The implementation</h3>
Both application ends are now created and published. In terms of checking problems along the route, the server actively checks the road closures API from Vicroads, as well as the Victorian government emergency service. For the demonstration purpose, only a subset of data from 29 July is used( in order not to violate any copyrights, the data is not updated).

Due to time constraints, the BOM API isn't checked (although similar code is already implemented on the server). Also, analysing crash hotspots wasn't finalised, a step needed before publishing these hotspots to a GIS service to be checked using the existing code.
</p>

<p><h3>More technical details</h3>
The application is built on the Bottle Python web framework. The application is adapted from the Visual Studio Bottle web application template, and is published on Azure app services. 
The Victorian government emergency service snapshot data was imported as geojson to ESRI arcgis online feature layer. This feature layer, along with Vicroads WFS API are used by the python code in the Bottle server to check the route for problems. 
Spatial Analysis for crash hotspots was attempted using kernel density in ArcGIS desktop, but due to the high number of crashes in urban centres, the heatmap shows whole cities as "hotspots" which is true, but more granularity is needed for proper driving advice.
</p>
<p>A possible test case is<em> 1 dickens street, elwood To glen huntley road</em></p>
<p>
Safe Drive everyone, and take care!
</p>
