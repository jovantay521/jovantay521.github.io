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
var polyline = [];
var marker=[];

srcInput.addEventListener('input', ()=>{autocomplete(srcInput)});
dstInput.addEventListener('input', ()=>{autocomplete(dstInput)});

form.addEventListener('submit', function(event){
    event.preventDefault();
    routeData.innerHTML="";
    if (polyline.length!=0)
    {
       polyline.forEach(element=>{
        map.map_setup.removeLayer(element);
       })
    }
    if(marker.length!=0)
    {
        marker.forEach(element=>{
            map.map_setup.removeLayer(element);
        })
    }
    type = routeType.value;

    const formData = new FormData(this);
    fetch("/route_planner",{
        method: "POST",
        body: formData
    }).then(res => {
        return res.json()
    }).then(data=>{
        if(data.template)
        {
            const tempElement = document.createElement("div");
            tempElement.innerHTML = data.template;
            const steps = tempElement.querySelectorAll(".routeSteps");
            steps.forEach(div=>{
                routeData.appendChild(div);
            })
        }
        if(type == "pt")
        {
            for(var i=0; i<3;i++)
            {
                var encoded_route =[];
                var decoded_route=[];
                data.route_response.plan.itineraries[i].legs.forEach((element)=>{
                    encoded_route.push(element.legGeometry.points);
                })
                encoded_route.forEach(element=>{
                    var decoded = L.PolylineUtil.decode(element);
                    polyline.push(L.polyline(decoded, {color: colors[i]}).addTo(map.map_setup));
                    decoded_route.push(decoded);
                })
            }
            var start = decoded_route[0][0]
            var end = decoded_route.slice(-1)[0][decoded_route.slice(-1)[0].length-1];
            marker.push(L.marker(end,{icon:dstIcon}).addTo(map.map_setup));
            marker.push(L.marker(start,{icon:startIcon}).addTo(map.map_setup));
        }
        else //add 2 more driving routes
        {
            var encoded =[];
            encoded.push(data.route_response.route_geometry);
            if(data.route_response.phyroute!=undefined){
                encoded.push(data.route_response.phyroute.route_geometry);
            }
            if(data.route_response.alternativeroute!=undefined){
                encoded.push(data.route_response.alternativeroute[0].route_geometry);
            }

            for(var i=0;i<3;i++){
                if(encoded[i]==undefined)
                {break;}
                var decoded = L.PolylineUtil.decode(encoded[i]);
                polyline.push(L.polyline(decoded,{color: colors[i]}).addTo(map.map_setup));
            }

            var start = decoded[0];
            var end = decoded.slice(-1)[0]; //extract an array starting from the last element
            marker.push(L.marker(end,{icon:dstIcon}).addTo(map.map_setup));
            marker.push(L.marker(start,{icon:startIcon}).addTo(map.map_setup));
        }
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
                li.classList.add("li-autocomplete");
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
