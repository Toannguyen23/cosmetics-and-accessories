

console.log("Minh Toan cute")
const monthName = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

$("#commentForm").submit(function(e){
    e.preventDefault();
    let dt = new Date();
    let time = dt.getDay() + " " + monthName[dt.getUTCMonth()] + " " + dt.getFullYear();

    $.ajax({
        data : $(this).serialize(),
        method : $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(res){
            console.log("Comment saved in DB")
            if(res.bool == true){
                $("#review-res").html("Đánh giá của bạn đã được lưu")
                $(".hide-review-form").hide()

              let  _html = '<div class="media mb-4 review-list">'
                _html += '<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIf4R5qPKHPNMyAqV-FjS_OTBB8pfUV29Phg&s" style="width:45x; height: 45px;>'
                _html += '<div class="media-body">'
                _html += '<h6>'+ res.context.user +'<small> - <i>'+ time +'</i></small></h6>'
                _html += '<div class="text-primary mb-2">'  
                

                    _html += '<p>'+ res.context.rating +' <i class="fas fa-star"></i></p>'

                
                // _html += '<p> <i class="fas fa-star"></i></p>'
                _html += '</div>'
                _html += '<p>' + res.context.review + '</p>'
                _html += '</div>'
                _html += '</div>'
                
                $("#list-review").prepend(_html)

            location.reload()
            }

            
        }
    })
})

$(document).ready(function(){
    $(".filter-checkbox,  #btn-filter-check").on("click", function(){
        console.log("Checked successed")

        let filter_object = {}
        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            // console.log("Filter value is: ", filter_value);
            // console.log("Filter object is: ", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key +']:checked')).map(function(e){
                return e.value;
            })
            
        })

        console.log("Filter object is: ", filter_object);
        $.ajax({
            url: "/filter-products",
            data: filter_object,
            dataType: "json",
            beforeSend: function(){
                console.log("Dữ liệu đang gửi đi....");
            },
            success: function(res){
                console.log(res);
                console.log("Lọc dữ liệu thành công....");
                $("#filterd-product").html(res.data);
            }
        })
        
    })

    $("#max_price").on("blur", function () {
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();
    
        if(current_price < parseInt(min_price)|| current_price > parseInt(max_price)){
            min_price = Math.round(min_price * 100) /100
            max_price = Math.round(max_price * 100) /100
            

            alert("Vui lòng nhập giá cả hợp lệ từ " + min_price + " đến " + max_price)
            $(this).val(min_price)
            $("#range").val(min_price)
            $(this).focus()

            return false
        }
        
        

    })
    $(".add-to-cart-btn").on("click", function(){
        let this_val = $(this)
        let index = this_val.attr("data-index")
        let quantity = parseInt($(".product-quantity-" + index).val())
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = parseInt($(".product-price-" + index).text())
        let product_pid = $(".product-pid-" + index).val()
        let product_image = ($(".product-image-" + index).val())
    
    
    
    
        console.log("Quantity: ", quantity);
        console.log("Product title: ", product_title);
        console.log("Product id: ", product_id);
        console.log("Product price: ", product_price);
        console.log("type of", typeof(product_price))
        console.log("this value btn: ", this_val);
        console.log("Image: ", product_image, typeof(product_image));
        console.log("Pid: ", product_pid);
    
    
    
    
        $.ajax({
            url: "/add-to-cart",
            data: {
                'id': product_id,
                'qty': quantity,
                'pid': product_pid,
                'image': product_image,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("adding data");
                
            },
            success: function(res){
                this_val.html("✔")
                console.log("Successfully");
                $("#cart-item-count").text(res.totalCartItems)
            }
        })
    
    
    })
    
    $(document).on("click",".delete-product", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("Product id", product_id)

           $.ajax({
            url: "/delete-from-cart",
            data:{
                "id": product_id,
                },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(res){
                console.log("successful to delete");
                
                this_val.show()
                $("#cart-item-count").text(res.totalCartItems)
                $("#cart-list").html(res.data)
                location.reload()
            }
    })

 
   
    })
       //update san pham
       $(document).on("click",".update-product", function(){

        let product_id = $(this).attr("data-product")
        let product_qty = $(".product-qty-" + product_id).val()
        let this_val = $(this)
    
        console.log("Product id", product_id)
        console.log("Product qty", product_qty)


           $.ajax({
            url: "/update-from-cart",
            data:{
                "id": product_id,
                   "qty": product_qty,
    
                },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            beforeSend: function(){
                this_val.html("✔")
            },
            success: function(res){
                console.log("successful to delete");
                
                this_val.show()
                $("#cart-item-count").text(res.totalCartItems)
                $("#cart-list").html(res.data)
                location.reload()
            }
    })

 
   
    })
    
    $(document).on("click", ".make-default-address", function (){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("id: ", id);
        console.log("Btn: ", this_val);
        
        $.ajax({
            url: "/make-default-address",
            data:
            {
                "id": id,
            },
            dataType: "json",
            success: function (){
                console.log("sucessfully...")
                if (Response.boolean == true){
                    $(".check").hide()
                    $(".action-btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()
                    
                }
            }

           

        })
        location.reload();

    })

    $(document).on("click", ".add-to-wishlist", function(){
        product_id = $(this).attr("data-product-item")
        this_val = $(this)

        console.log("Product id: ", product_id);
        console.log("btn val: ", this_val);

        $.ajax({
            url: '/add-to-wishlist',
            data: {
                "id": product_id,
            },
            dataType: "json",
            success: function(res){
                this_val.html("✔")
                if(res.bool == true){
                    console.log("added successfully");
                    
                }
                
            }
        })
        
    })

    $(document).on("click", ".remove-wishlist", function(){

        let wishlist_id = $(this).attr("wishlist-id")
        let this_val = $(this)

        console.log("Wishlist id is: ", wishlist_id)
        console.log("Btn value: ", this_val);
        
        $.ajax({
            url: '/remove-from-wishlist',
            data: {
                "id": wishlist_id,
            },
            dataType: "json",

            beforeSend: function(){
                console.log("Deleting wishlist....");
                
            },
            success: function(res){
                $("#wishlist-list").html(res.data)

                location.reload()
            }
        })
    })

    $(document).on("submit", "#contactForm", function(e){
        e.preventDefault();
        console.log("Đã gửi đi");
        let full_name = $("#full_name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()

        console.log("Name", full_name);
        console.log("Email", email);
        console.log("Phone", phone);
        console.log("Subject", subject);
        console.log("Message", message);

        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "fullname": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message
            },
            dataType: "json",
            beforeSend: function(res){
                console.log("Sending to server....")
            },
            success: function(res){
                $(".header-form").hide()
                $("#contactForm").hide()
                
            }
        })
        
    })
 
})


//them phan khac vao o trang product-detal

// $("#add-to-cart-btn").on("click", function(){
//     let quantity = parseInt($("#product-quantity").val())
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#product-price").text()
//     let this_val = $(this)

//     console.log("Quantity: ", quantity);
//     console.log("Product title: ", product_title);
//     console.log("Product id: ", product_id);
//     console.log("Product price: ", product_price);
//     console.log("type of", typeof(product_price))
//     console.log("this value btn: ", this_val);

//     $.ajax({
//         url: "/add-to-cart",
//         data: {
//             'id': product_id,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("adding data");
            
//         },
//         success: function(res){
//             this_val.html("đã thêm vào")
//             console.log("Successfully");
//             $("#cart-item-count").text(res.totalCartItems)
//         }
//     })
    

// })

//o trang index

// $(".add-to-cart-btn").on("click", function(){
//     let this_val = $(this)
//     let index = this_val.attr("data-index")
//     let quantity = parseInt($(".product-quantity-" + index).val())
//     let product_title = $(".product-title-" + index).val()
//     let product_id = $(".product-id-" + index).val()
//     let product_price = parseInt($(".product-price-" + index).text())
//     let product_pid = $(".product-pid-" + index).val()
//     let product_image = ($(".product-image-" + index).val())




//     console.log("Quantity: ", quantity);
//     console.log("Product title: ", product_title);
//     console.log("Product id: ", product_id);
//     console.log("Product price: ", product_price);
//     console.log("type of", typeof(product_price))
//     console.log("this value btn: ", this_val);
//     console.log("Image: ", product_image, typeof(product_image));
//     console.log("Pid: ", product_pid);




//     $.ajax({
//         url: "/add-to-cart",
//         data: {
//             'id': product_id,
//             'qty': quantity,
//             'pid': product_pid,
//             'image': product_image,
//             'title': product_title,
//             'price': product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("adding data");
            
//         },
//         success: function(res){
//             this_val.html("✔")
//             console.log("Successfully");
//             $("#cart-item-count").text(res.totalCartItems)
//         }
//     })


// })

