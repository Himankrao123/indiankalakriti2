
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

function addreview(){
  // console.log(clicked_id);
$.ajax({
    url: "/api/addreview",
    dataType:"json",
    data: {
      productID:document.getElementById("productID").value,
      review:document.getElementById("review").value,
      rating:document.getElementById("rating").value
    },
    contentType:false,
    // processData:false,
    type:"GET",
    success: function( result ) {
        //referesh the page
        location.reload();
        // console.log(result);
    },
    error: function(result){
      document.getElementById("message2").innerHTML = result["responseJSON"]["error"];
      document.getElementById("messagediv").style.display = "block";
    }
  });
}

var rating_count = 5;
function getrating(){

$.ajax({
    url: "/api/getrating",
    dataType:"json",
    data: {
      productID:document.getElementById("productID").value,
      lastrating:rating_count
    },
    contentType:false,
    // processData:false,
    type:"GET",
    success: function( result ) {
        review_div = document.getElementById("reviewdiv").innerHTML;
        for (var i = 0; i < result.rating.length; i++){
          review_div += `<div class="review">\n<p>Review : ${result.rating[i]["review"]}</p>\n<p>Rating : ${result.rating[i]["rating"]}</p>\n<hr>\n</div>`
        }
        document.getElementById("reviewdiv").innerHTML = review_div;
        
    },
    error: function(result){
      if (result["responseJSON"]["error"] == "End of rating"){
        document.getElementById("getratingbtn").style.display = "none";
      }
      else{
        document.getElementById("message2").innerHTML = result["responseJSON"]["error"];
        document.getElementById("messagediv").style.display = "block";
      }
    }
  });
}