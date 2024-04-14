const userInput = document.getElementById("userInput");
const routeType = document.getElementById("routeType");
const srcInput = document.getElementById("srcInput");
const dstInput = document.getElementById("dstInput");
const calBtn = document.getElementById("calBtn");
const ul = document.getElementById("autocomplete")
const form = document.getElementById("input-form")
const routeData = document.getElementById("routeData");
const routeInfoButtons = document.querySelectorAll(".routeInfoButton");

//const savedRouteButton = document.getElementById("savedRoutes");

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
    constructor(source, destination, type, encodedRoute, routeInfo, color)  //encodedRoute is an array and routeInfo is a nodelist
    {
        this.source=source;
        this.destination=destination;
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
            // div.style.backgroundColor= this.color;
            routeData.appendChild(div);
        })
        routeData.style.display = "block";
    }

    displaySavedRouteInfo()
    {
        var div = document.createElement("div");
        div.classList.add("route1Steps");
        var ul = document.createElement("ul");
        ul.classList.add("list-group");
        ul.classList.add("list-group-flush");
        ul.classList.add("list-group-numbered");
        this.routeInfo.forEach(str=>{
            var li = document.createElement("li");
            li.classList.add("list-group-item");
            li.textContent=str;
            ul.appendChild(li);
        })
        div.append(ul);
        routeData.appendChild(div);
        routeData.style.display = "block";
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
        routeInfoButtons.forEach(button=>{
            routeData.append(button);
        })
    }
}

var routeContainer=[]; //array to store Route objects
var savedRoutes =[];

srcInput.addEventListener('input', ()=>{autocomplete(srcInput)});
dstInput.addEventListener('input', ()=>{autocomplete(dstInput)}); 

form.addEventListener('submit', function(event){
    event.preventDefault();
    calBtn.disabled = true;
    setTimeout(()=>{
        calBtn.disabled=false;
    },3000);
    var src = srcInput.value;
    var dst = dstInput.value;

    if(routeContainer.length>0)
    {
        routeContainer.forEach(element=>{
            element.removeAllInfo();
        })
        routeContainer=[];
    }
    savedRoutes.forEach((ele)=>{
        ele.removeAllInfo();
    })

    var currentTime= new Date;
    var options ={hour12:false, hour:"2-digit", minute:"2-digit"};
    var time = currentTime.toLocaleTimeString(undefined, options);
    if (time.trim()>"00:00" && time.trim()<"06:00")
        {
            type="drive";
        }
    else
        {
            console.log("there");
        }

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
                if(tempElement.querySelectorAll(`.route${i}Steps > .list-group-item`)!=null)
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
                var route = new Route(src,dst,type,encoded_route,steps[i],colors[i]);
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
                var route= new Route(src,dst,type,encodedRoute,steps[i],colors[i]);
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
                // calBtn.style.display="none";
                var li = document.createElement('li');
                li.classList.add("list-group-item");
                li.textContent=data.results[loop].ADDRESS;
                if(Input.value.trim()==li.textContent.trim())
                {
                    return;
                }
                ul.appendChild(li);

                li.addEventListener('click', (event)=>{ //add address to input box

                    Input.value = event.target.textContent;
                    ul.innerHTML ="";
                    ul.style.display ='none';
                    // calBtn.style.display="inline";
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

function saveRoute(routeNum)
{
    var routeName = prompt("Enter the name of the route: ");
    if(routeName==null)
    {
        routeName = "saved route";
    }
    var route = routeContainer[routeNum-1];
    var routeInfoStr=[];
    route.routeInfo[0].querySelectorAll(".list-group-item").forEach(element=>
    {
        routeInfoStr.push(element.textContent);
    })

    var form = new FormData();
    form.append('name', routeName);
    form.append('source', route.source);
    form.append('destination',route.destination);
    form.append('routeType',route.routeType);
    form.append('encodedRoute',JSON.stringify(route.encodedRoute));
    form.append('routeInfo',JSON.stringify(routeInfoStr));

    fetch("/",{         //route to be filled
        method: "POST",
        body: form
    }).then(res=>{
        return res.text();
    }).then(txt=>{
        console.log(txt);
    });
}

function loadRoutes()
{
    var menu = document.querySelector(".offcanvas-body");
    menu.innerHTML="";
    savedRoutes.forEach((ele)=>{
        ele.removeAllInfo();
    })
    fetch("/getRoute").then(res=>{
        return res.json();
    }).then(data=>{
        savedRoutes =[];
        var allRoutes = data.routes;
        var counter = 1;
        allRoutes.forEach(element=>{
            var route = new Route(element.source, element.destination, element.routeType, element.encodedRoute, element.routeInfo,"red");
            savedRoutes.push(route);
            var div=document.createElement('div');
            var delBtn = document.createElement('button');

            div.textContent= `${counter}: ${element.name}`;
            counter++;

            div.appendChild(delBtn);

            //separate delBtn with elements
            div.style.display = 'flex';
            div.style.justifyContent = 'space-between'; 

            //bootstrap for div
            div.classList.add('rounded'); 
            div.classList.add('border');
            div.classList.add('p-3');
            
            //bootstrap for delBtn
            delBtn.classList.add('btn-close');
            delBtn.classList.add('text-reset'); //inherit colour from parent class
            delBtn.setAttribute('type', 'button');
            delBtn.setAttribute('aria-label', 'Close');

                
            div.addEventListener('click',function(event){
                routeContainer.forEach(element=>{
                    element.removeAllInfo();
                })
                savedRoutes.forEach((ele)=>{
                    ele.removeAllInfo();
                })
                var routeNum = parseInt(event.target.textContent[0])-1;
                var route = savedRoutes[routeNum];
                route.displaySavedRouteInfo();
                route.displayRouteLine();

            })
            menu.appendChild(div);
        })
    })
}
