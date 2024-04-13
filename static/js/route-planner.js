const userInput = document.getElementById("userInput");
const routeType = document.getElementById("routeType");
const srcInput = document.getElementById("srcInput");
const dstInput = document.getElementById("dstInput");
const calBtn = document.getElementById("calBtn");
const ul = document.getElementById("autocomplete")
const form = document.getElementById("input-form")
const routeData = document.getElementById("routeData");

const colors = ["red", "blue","green"];
var dstIcon = L.icon({
    iconUrl: '/static/images/dstIcon.png',

    iconSize:[38,38],
    iconAnchor:[19,38],
    popupAnchor:[0,-38]
})
var startIcon = L.icon({
    iconUrl: '/static/images/startIcon.png',

    iconSize:[38,38],
    iconAnchor:[19,38],
    popupAnchor:[0,-38]
})

class Route
{
    constructor(type, encodedRoute, routeInfo, color)  //encodedRoute is an array and routeInfo is a nodelist
    {
        //this.source=source;
        //this.destination=destination;
        this.routeType=type;
        this.routeInfo = routeInfo;
        this.encodedRoute = encodedRoute;
        this.color = color
        this.polyline=[];
        this.marker =[];
    }

    decodeRoute()
    {
        var decodedRoute = [];
        this.encodedRoute.forEach(element=>{
            var decoded = L.PolylineUtil.decode(element);
            decodedRoute.push(decoded);
        })

        return decodedRoute;
    }

    displayRouteLine()
    {
        var decodedRoute=this.decodeRoute(this.encodedRoute);
        decodedRoute.forEach(element=>{
            this.polyline.push(L.polyline(element, {color: this.color}).addTo(map.map_setup));
        })

        var start = decodedRoute[0][0]
        var end = decodedRoute.slice(-1)[0][decodedRoute.slice(-1)[0].length-1]; //slice extract an array starting from the last element
        this.marker.push(L.marker(end,{icon:dstIcon}).addTo(map.map_setup));
        this.marker.push(L.marker(start,{icon:startIcon}).addTo(map.map_setup));
        return;
    }

    displayRouteInfo()
    {
        this.routeInfo.forEach(div=>{
            div.style.backgroundColor= this.color;
            routeData.appendChild(div);
        })
    }

    removeAllInfo()
    {
        if (this.polyline.length!=0)
        {
            this.polyline.forEach(element=>{
                map.map_setup.removeLayer(element);
            })
        }

        if(this.marker.length!=0)
        {
            this.marker.forEach(element=>{
                map.map_setup.removeLayer(element);
            })
        }

        routeData.innerHTML="";
    }
}

var routeContainer=[]; //array to store Route objects

srcInput.addEventListener('input', ()=>{autocomplete(srcInput)});
dstInput.addEventListener('input', ()=>{autocomplete(dstInput)});

form.addEventListener('submit', function(event){
    event.preventDefault();
    if(routeContainer.length>0)
    {
        routeContainer.forEach(element=>{
            element.removeAllInfo();
        })
        routeContainer=[];
    }
    
    type = routeType.value;

    const formData = new FormData(this);
    fetch("/route-planner",{
        method: "POST",
        body: formData
    }).then(res => {
        return res.json()
    }).then(data=>{
        if(data.template)
        {
            var steps=[];
            const tempElement = document.createElement("div");
            tempElement.innerHTML = data.template;
            for(var i=1;i<=3;i++)
            {
                if(tempElement.querySelectorAll(`.route${i}Steps`)!=null)
                    steps.push(tempElement.querySelectorAll(`.route${i}Steps`));
            }
        }
        if(type == "pt")
        {
            for(var i=0; i<steps.length;i++)
            {
                var encoded_route =[]; 
                data.route_response.plan.itineraries[i].legs.forEach((element)=>{
                    encoded_route.push(element.legGeometry.points);
                })
                var route = new Route(type,encoded_route,steps[i],colors[i]);
                routeContainer.push(route);
            }
        }
        else 
        {
            var encoded =[];
            encoded.push(data.route_response.route_geometry);
            if(data.route_response.phyroute!=undefined){
                encoded.push(data.route_response.phyroute.route_geometry);
            }
            if(data.route_response.alternativeroute!=undefined){
                encoded.push(data.route_response.alternativeroute[0].route_geometry);
            }

            for(var i=0;i<encoded.length;i++){
                var encodedRoute = [];
                encodedRoute.push(encoded[i]);
                var route= new Route(type,encodedRoute,steps[i],colors[i]);
                routeContainer.push(route);
            }
        }
        routeContainer.forEach(element=>
        {
            element.displayRouteInfo();
            element.displayRouteLine();
        })
    }).catch(error=>{console.error(error)});

})
function autocomplete(Input){
    ul.innerHTML=""; //on each input clear ul
    var input = Input.value;
    if(input.length<3) //if input<3 no suggestions
    {
        ul.style.display ='none';
        calBtn.style.display="inline";
    }
    else
    {
        fetch(`https://www.onemap.gov.sg/api/common/elastic/search?searchVal=${input}&returnGeom=Y&getAddrDetails=Y`).then(res =>{
            return res.json();
        }).then(data =>{
            if(data.results.length==0) 
                {
                    return;
                }
            for(var loop=0;loop<5;loop++) //auto-complete 5 addresses
            {
                calBtn.style.display="none";
                var li = document.createElement('li');
                li.classList.add("list-group-item");
                li.textContent=data.results[loop].ADDRESS;
                ul.appendChild(li);

                li.addEventListener('click', ()=>{ //add address to input box

                    Input.value = li.textContent;
                    ul.innerHTML ="";
                    ul.style.display ='none';
                    calBtn.style.display="inline";
                    return;

                })

                if(data.results[loop+1]==undefined)
                {
                    break;
                }
            }
            ul.style.display="inline";
            return;
        })

    }
}

function calRoute()
{
    console.log("Do route calculation");
}
