const userInput = document.getElementById("userInput");
const routeType = document.getElementById("routeType");
const srcInput = document.getElementById("srcInput");
const dstInput = document.getElementById("dstInput");
const calBtn = document.getElementById("calBtn");
const ul = document.getElementById("autocomplete")
const form = document.getElementById("input-form")
const colors = ["red", "blue"];

var dstIcon = L.icon({
    iconUrl: '/static/images/dstIcon.png',

    iconSize:[38,38],
    iconAnchor:[19,38],
    popupAnchor:[0,-38]
})

srcInput.addEventListener('input', ()=>{autocomplete(srcInput)});
dstInput.addEventListener('input', ()=>{autocomplete(dstInput)});

form.addEventListener('submit', function(event){
    event.preventDefault();
    type = routeType.value;

    const formData = new FormData(this);
    fetch("/route_planner",{
        method: "POST",
        body: formData
    }).then(res => {
        return res.json()
    }).then(data=>{
        if(type == "pt")
        {
            for(var i=0; i<2;i++)
            {
                var encoded_route =[];
                data.plan.itineraries[i].legs.forEach((element)=>{
                    encoded_route.push(element.legGeometry.points);
                })
                encoded_route.forEach(element=>{
                    var decoded = L.PolylineUtil.decode(element);
                    var polyline = L.polyline(decoded, {color: colors[i]}).addTo(map.map_setup);
                })
            }
        }
        else
        {
            var encoded = data.route_geometry;
            var decoded = L.PolylineUtil.decode(encoded);
            var end = decoded.slice(-1)[0];
            L.marker(end,{icon:dstIcon}).addTo(map.map_setup);
            var polyline = L.polyline(decoded,{color: "red"}).addTo(map.map_setup);
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
