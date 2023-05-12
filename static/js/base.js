/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidebar").style.width = "300px";
    document.getElementById("main").style.marginLeft = "300px";
    document.getElementById("openbtn").style.display = "none";
  }
  
  /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById("openbtn").style.display = "block";
  }
dropdowncount = {'dropdown1':0,'dropdown3':0};
function dropdown(givenid){
  if (dropdowncount[`${givenid}`] === 0){
    document.getElementById(`${givenid}`).style.height = "max-content";
    document.getElementById(`${givenid}`).style.display = "block";
    dropdowncount[`${givenid}`] = 1;
  }
  else if(dropdowncount[`${givenid}`] === 1){
    document.getElementById(`${givenid}`).style.height = "0%";
    document.getElementById(`${givenid}`).style.display = "none";
    dropdowncount[`${givenid}`] = 0;
  }
}

function closemessages(){
  document.getElementById("messagediv").style.display = "none";
}