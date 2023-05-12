
function addtowishlist(clicked_id){
  // console.log(clicked_id);
$.ajax({
    url: "/api/addtowishlist",
    dataType:"json",
    data: {
      productID:clicked_id
    },
    contentType:false,
    // processData:false,
    type:"GET",
    success: function( result ) {
        console.log(result);
        var pid = document.getElementById(`wr${result.pid}`);
        var pid2 = document.getElementById(`ww${result.pid}`);
        pid.style.display = "block";
        pid2.style.display = "none";
        document.getElementById("message2").innerHTML = result.message;
        document.getElementById("messagediv").style.display = "block";
        // console.log(result);
    },
    error: function(result){
      document.getElementById("message2").innerHTML = result["responseJSON"]["error"];
        document.getElementById("messagediv").style.display = "block";
    }
  });
}


function removefromwishlist(clicked_id){
  // console.log(clicked_id);

    // console.log("function called!")
$.ajax({
    url: "/api/removefromwishlist",
    dataType:"json",
    data: {
      productID:clicked_id
    },
    contentType:false,
    // processData:false,
    type:"GET",
    success: function( result ) {
        console.log(result);
        var pid = document.getElementById(`wr${result.pid}`);
        var pid2 = document.getElementById(`ww${result.pid}`);
        pid.style.display = "none";
        pid2.style.display = "block";
        document.getElementById("message2").innerHTML = result.message;
        document.getElementById("messagediv").style.display = "block";

    },
    error: function(result){
      document.getElementById("message2").innerHTML = result["responseJSON"]["error"];
        document.getElementById("messagediv").style.display = "block";
    }
  });
}

function addtocart(clicked_id){
  // console.log(clicked_id);
$.ajax({
    url: "/api/addtocart",
    dataType:"json",
    data: {
      productID:clicked_id
    },
    contentType:false,
    // processData:false,
    type:"GET",
    success: function( result ) {
        document.getElementById(result.pid).style.display = "none"
        document.getElementById(`s${result.pid}`).style.display = "block"
        document.getElementById("message2").innerHTML = result.message;
        document.getElementById("messagediv").style.display = "block";
        // console.log(result);
    },
    error: function(result){
      document.getElementById("message2").innerHTML = result["responseJSON"]["error"];
        document.getElementById("messagediv").style.display = "block";
    }
  });
}

