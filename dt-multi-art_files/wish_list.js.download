function debounceNew(fn, wait) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), wait);
  };
}

class dTX_WhistList {

    constructor() {
        this.wishListData = [];

        this.LOCAL_STORAGE_WISHLIST_KEY = 'shopify-wishlist';
        this.LOCAL_STORAGE_DELIMITER = ',';
    }

    setListLocalStorageKey(LOCAL_STORAGE_WISHLIST_KEY, LOCAL_STORAGE_DELIMITER) {
        this.LOCAL_STORAGE_WISHLIST_KEY = LOCAL_STORAGE_WISHLIST_KEY;
        this.LOCAL_STORAGE_DELIMITER = LOCAL_STORAGE_DELIMITER;
    }

    setupGrid(listType) {
        var wishlist = this.getWishlist();

        var requests = wishlist.map(function (handle) {
            var productTileTemplateUrl = '/products/' + handle + '?view=json';

            var getProductsList =  this.getProductResponse(productTileTemplateUrl);

            return getProductsList;
        }.bind(this));
      

       return Promise.all(requests).then(function (responses) {
              var wishlistProductCards = responses.join('%$$%');
              var wishlistProductCards = wishlistProductCards;

              var a_wishlistRecords = wishlistProductCards.split("%$$%");

              let recordsObj = [];

              if (Array.isArray(a_wishlistRecords) && a_wishlistRecords.length) {
                  var index = 0;
                  a_wishlistRecords.forEach(record => {
                      var a_record = record.split("~~");

                      var recordObj = {
                              id:             a_record[0],
                              product_title:  a_record[1],
                              product_handle: a_record[2],
                              product_image:  a_record[3],
                              vendor:         a_record[4],
                              type:           a_record[5],
                              money_price:    a_record[6],
                              price_min:      a_record[7],
                              price_max:      a_record[8],
                              available:      a_record[9],
                              price_varies:   a_record[10],
                              variant_id:     a_record[11],
                              variant_title:  a_record[12],
                              sku:            a_record[13],
                              quantity:       "1",
                              product_url:    '/products/'+a_record[2]
                      };

                      recordsObj[index] = recordObj;

                      index = index + 1;

                  });

              }

              return recordsObj;

         }).then(function(data) {
         
             this.wishListData = data;  
         
             return data;

         }.bind(this));

    }

    getWishListRecords()
    {
        return this.wishListData;
    }

    getCompareListRecords()
    {
        return this.wishListData;
    }

    getProductResponse(url) {

       var responseResult = axios.get(url)
          .then((response) => {
                var text = response.data;
                text = text.replace(/^\s*[\r\n]/gm, '');
                // console.log(text); 

                return text;
           });
           
        return responseResult;
        
      
//       var responseResult =  getDTProduct(url);
      
//       alert(responseResult);

//       return responseResult;
      
    }

    getTotalCount() {
		return this.getWishlist().length;
    }
  
    getWishlist() {
        var wishlist = localStorage.getItem(this.LOCAL_STORAGE_WISHLIST_KEY) || false;
        if (wishlist) return wishlist.split(this.LOCAL_STORAGE_DELIMITER);
        return [];
    }

    setWishlist(array) {
        var wishlist = array.join(this.LOCAL_STORAGE_DELIMITER);
        if (array.length) localStorage.setItem(this.LOCAL_STORAGE_WISHLIST_KEY, wishlist);
        else localStorage.removeItem(this.LOCAL_STORAGE_WISHLIST_KEY);
        return wishlist;
    }

    updateWishlist(handle) {
        var wishlist = this.getWishlist();
        var indexInWishlist = wishlist.indexOf(handle);
        if (indexInWishlist === -1) wishlist.push(handle);
        else wishlist.splice(indexInWishlist, 1);
        return this.setWishlist(wishlist);
    }

    removeWhishlist(handle) {
        var wishlist = this.getWishlist();

        wishlist = this.remove(wishlist, handle);

        return this.setWishlist(wishlist);  
    }

    resetWishlist() {
        return this.setWishlist([]);
    }

    isAddedIntoList(handle) {
        var wishlist = this.getWishlist();  
        
        return wishlist.includes(handle);
    }

    remove(arr) {
        var what, a = arguments, L = a.length, ax;
        while (L > 1 && arr.length) {
            what = a[--L];
            while ((ax= arr.indexOf(what)) !== -1) {
                arr.splice(ax, 1);
            }
        }
        return arr;
    };
}


async function getDTProduct(url) {
    
 
    try {
      let res = await fetch(url);

      return res.text().then(function (text) {      
        return text;
      });

        
    } catch (error) {
        console.log(error);
    }
}

class dTXWhishList extends HTMLElement {
    constructor() {
      super();

      this.dTWhistList = new dTX_WhistList();

      this.debouncedOnSubmit = debounceNew((event) => {
        this.onSubmitHandler(event);
      }, 500);


      this.addWishList = this.querySelector('.add-wishlist');      

      if (this.addWishList.hasAttribute("data-product_handle")) {
      	this.productHandle = this.addWishList.getAttribute('data-product_handle');

        this.addWishList.addEventListener('click', this.debouncedOnSubmit.bind(this));

      	this.initLoad();
      }
      
      /*
      this.productHandle = this.addWishList.getAttribute('data-product_handle');

      this.addWishList.addEventListener('click', this.debouncedOnSubmit.bind(this));

      this.initLoad();
      */
    }

    onSubmitHandler(event) {
        event.preventDefault();

        if (this.dTWhistList.isAddedIntoList(this.productHandle)) {
            window.location = "/pages/wishlist";
        } else {
            this.addWishList.classList.add("adding");

            this.dTWhistList.updateWishlist(this.productHandle);

            setTimeout(this.postAdd.bind(this), 4000);
        }
    }

    postAdd() {
      /*
        document.querySelector(".dtxc-wishlist-count").setAttribute(
          'count', 
          this.dTWhistList.getTotalCount()
        );
      */  

       document.querySelector(".dt-wishlist-cnt").setAttribute(
          'count', 
          this.dTWhistList.getTotalCount()
       );

      var COUNT_WISH_LIST = this.dTWhistList.getTotalCount();
      
      var setWishListCountNew = function(COUNT_WISH_LIST) {
          if (document.querySelector('.dt-wishlist-cnt')) {

              var cnt = COUNT_WISH_LIST;

              var elementList = document.querySelectorAll(".dt-wishlist-cnt");
              elementList.forEach((element) => {
                if (cnt > 0 ) {
                    element.innerHTML = cnt;
                    //element.style.display = 'block';
                } else {
                    element.innerHTML = 0;
                   // element.style.display = 'none';
                }
             });      
          }

      };

      setWishListCountNew(COUNT_WISH_LIST);
      
        
      this.addWishList.classList.remove("adding");
      this.addWishList.classList.add("added");   
    }

    initLoad() {
        if (this.dTWhistList.isAddedIntoList(this.productHandle)) {
            this.addWishList.classList.add("added");
        }    
    }
}    

customElements.define('dtx-wishlist', dTXWhishList);

function makeTimer() {

  $('.product-deal-count').each(function() {
   
    var endTime = new Date($(this).attr('data-end-time'));		
    endTime = (Date.parse(endTime) / 1000);

    var now = new Date();
    now = (Date.parse(now) / 1000);

    var timeLeft = endTime - now;
    
    if(timeLeft > 0) {
      var days = Math.floor(timeLeft / 86400); 
      var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
      var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
      var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

      if (hours < "10") { hours = "0" + hours; }
      if (minutes < "10") { minutes = "0" + minutes; }
      if (seconds < "10") { seconds = "0" + seconds; }

      $(this).find(".days").html(days + "<span>Days</span>");
      $(this).find(".hours").html(hours + "<span>Hrs</span>");
      $(this).find(".minutes").html(minutes + "<span>Mins</span>");
      $(this).find(".seconds").html(seconds + "<span>Secs</span>");	
      
    } else {
      $(this).find(".notice").html("<span>Expired</span>");
    }
    
  });

}

setInterval(function() { makeTimer(); }, 1000);
    