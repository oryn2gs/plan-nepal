const lat = 27.716367;
const lng = 85.311636;

var map = L.map("map").setView([lat, lng], 13);
console.log(293572);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// ? custom icon with images
// var customIcon = L.icon({
//   iconUrl:
//     "https://www.flaticon.com/free-icon/location_1483336?term=marker&page=1&position=7&origin=search&related_id=1483336",
//   iconSize: [30, 30],
//   iconAnchor: [15, 30],
// });

// ? custom icon with html
// var customIcon = L.divIcon({
//   className: "custom-div-icon",
//   html: '<div class="icon-content"><i class="fa-solid fa-location-dot"></i></div>',
//   iconSize: [100, 100],
// });

var marker = L.marker([lat, lng]).addTo(map);
marker.bindPopup("Plan Nepal Pvt ltd");

console.log(map);
