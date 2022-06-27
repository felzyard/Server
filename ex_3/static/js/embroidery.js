// replace the image in contact us page by changing src of productShow img
function show_product() {
    var selectElement = document.getElementById("listby");
    var url = selectElement.options[selectElement.selectedIndex].getAttribute('rel');
    document.getElementById('productShow').src = url;
}
// help function for saving the origin color
function getOriginalColor(){
    var r = document.querySelector(':root');
    var rs = getComputedStyle(r);
  return rs.getPropertyValue('--extraBrightPink');
}
// function that change background color of summary
var counter = 0;
function createContactButton(){
    var summaryElement = document.getElementById("Summary");
    let originalColor = getOriginalColor();
    summaryElement.style.backgroundColor = counter % 2 === 0 ? "#f4acb7" : originalColor;
    counter++;
}

