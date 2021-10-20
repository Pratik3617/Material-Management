$(document).ready(function(){

    $.getJSON("/fetchallStates",function(data){

         $.each(data,function(index,item){

            $('#state').append($('<option>').text(item[1]).val(item[0]))
         })
    })

    $('#state').change(function(){
        $('#city').empty()
        $('#city').append($('<option>').text('- City -'))
        $.getJSON("/fetchallCities",{"state":$('#state').val()},function(data){

            $.each(data,function(index,item){
                $('#city').append($('<option>').text(item[2]).val(item[1]))
            })
        })
    })

    $('#picture').change(function(){
        let file=picture.files[0]
        pic.src=URL.createObjectURL(file)
    })

    $.getJSON('/categoryjson',function(data){
        $.each(data,function(index,item){
            $('#cid').append($('<option>').text(item[1]).val(item[0]));
        })
    });

    $('#cid').change(function(){
        $('#scid').empty()
        $('#scid').append($('<option>').text('- SELECT SUBCATEGORY -'))
        $.getJSON('/subcategoryjson',{'cid':$('#cid').val()},function(data){
            $.each(data,function(index,item){
                $('#scid').append($('<option>').text(item[2]).val(item[1]));
            })
        });
    })

    $('#scid').change(function(){
        $('#pid').empty()
        $('#pid').append($('<option>').text('- SELECT PRODUCT -'))
        $.getJSON('/productjson',{'scid':$('#scid').val()},function(data){
            $.each(data,function(index,item){
                $('#pid').append($('<option>').text(item[3]).val(item[2]));
            })
        })
    })


    $('#pid').change(function(){
        $('#fpid').empty()
        $('#fpid').append($('<option>').text('- SELECT FINAL PRODUCT -'))
        $.getJSON('/fetchallFinalProduct',{'pid':$('#pid').val()},function(data){
            alert(data)
            $.each(data,function(index,item){
                $('#fpid').append($('<option>').text(item[4]).val(item[3]));
            })
        })
    })

    $.getJSON("/fetchallSupplier",function(data){

         $.each(data,function(index,item){
            alert(data)
            $('#sid').append($('<option>').text(item[1]).val(item[0]))
         })
    })

})