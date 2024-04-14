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

marker = []

function displayCarparkLocation(carpark_coordinates)
{
//  I am not sure how leaflet takes in coordinates and plots on webpage. please help.
    marker.push(L.marker(carpark_coordinates,{icon:dstIcon}).addTo(map.map_setup));
    return;
}