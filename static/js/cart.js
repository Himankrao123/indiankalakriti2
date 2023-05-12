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
          var count = document.getElementById(`c${result.pid}`).innerHTML
          document.getElementById(`c${result.pid}`).innerHTML = +count+1
          document.getElementById("message2").innerHTML = result.message;
          document.getElementById("messagediv").style.display = "block";
          document.getElementById("totalamount").innerHTML = result.totalamount;
          // console.log(result);
      },
      error: function(result){
        document.getElementById("message2").innerHTML = result["responseJSON"]["error"];
          document.getElementById("messagediv").style.display = "block";
      }
    });
  }

  function removefromcart(clicked_id){
    // console.log(clicked_id);
  $.ajax({
      url: "/api/removefromcart",
      dataType:"json",
      data: {
        productID:clicked_id
      },
      contentType:false,
      // processData:false,
      type:"GET",
      success: function( result ) {
            var count = document.getElementById(`c${result.pid}`).innerHTML
            document.getElementById(`c${result.pid}`).innerHTML = +count-1
          document.getElementById("message2").innerHTML = result.message;
          document.getElementById("messagediv").style.display = "block";
          document.getElementById("totalamount").innerHTML = result.totalamount;
          // console.log(result);
      },
      error: function(result){
        document.getElementById("message2").innerHTML = result["responseJSON"]["error"];
          document.getElementById("messagediv").style.display = "block";
      }
    });
  }