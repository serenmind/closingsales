$(function() {
  'use strict';
  var title = $('#id_title'),
      state = $('#id_state'),
      address = $('#id_address'),
      zipcode = $('#id_zipcode');
  var category = $('#id_category');
  var subcategory = $('#id_subcategory');
  var description = $('#id_description');
  var adDate = $('#id_start_date');
  var latitude = $('#id_latitude');
  var longitude = $('#id_longitude');
  var shopType = $('#id_shoptype');

  function addRemoveError(jqObj, isAdittion) {
    if (isAdittion) {
      jqObj.parents('.form-group').addClass('has-error');
      return
    }
    jqObj.parents('.form-group').removeClass('has-error');
  }


  description.wysihtml5({
    'image': false
  });
  var date = new Date();
  var endDate = moment().add(5, 'd');
  
  adDate.daterangepicker({
    minDate: date,
    startDate: date,
    endDate:endDate
  });

  $('#id_opening_hour').timepicker({
      showInputs: false,
      defaultTime: '8:00 AM'
  });

  $('#id_closing_hour').timepicker({
      showInputs: false,
      defaultTime: '18:00 PM'
  });

  function buildOptions(data, container) {
    container.empty()
    for (var i = 0; i < data.length; i++) {
      var option = data[i];
      var options = $('<option>', {
        val: option.id,
        text: option.name
      });
      container.append(options);
    }
  }

  var currentShoptype = undefined;
  var categoryData = [{name: 'Select Category', id: ''}];
  var subcategoryData = [{name: 'Select SubCategory', id: ''}];
  $(document).on('change', '#id_shoptype', function(evt) {
    var selected = $(evt.target).val();
    if (selected.trim() == '') {
      buildOptions(categoryData, category);
      buildOptions(subcategoryData, subcategory);
    } else if (selected && selected != currentShoptype) {
      $.ajax({
        url: '/api/shoptypes/' + selected + '/categories/',
      }).then(function(data) {
        data.unshift({name: 'Select Category', id: ''});
        buildOptions(data, category);
      }, function(err) {
        console.log('err' + err);
      })
    }
    currentShoptype = selected;
  });


  var currentCategory = undefined;
  category.on('change', function(evt) {
    var selected = $(evt.target).val();

    if (selected.trim() == '') {
      buildOptions(subcategoryData, subcategory);
    } else if (selected && selected != currentCategory) {
      $.ajax({
        url: '/api/categories/' + selected + '/subcategories/'
      }).then(function(data) {
        data.unshift({name: 'Select SubCategory', id: ''});
        buildOptions(data, subcategory);
      }, function(err) {
        console.log('error' + err)
      })
    }
    currentCategory = selected;
  })

  

  var map;

  function initMap() {
    var myLatLng = {lat: 	52.520008, lng: 13.404954};
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 	52.520008, lng: 13.404954},
      zoom: 8
    });
    var marker;
    google.maps.event.addListener(map, 'click', function(evt) {
      var latLang = new google.maps.LatLng(evt.latLng.lat(), evt.latLng.lng());
      if (marker) return false;
      marker = new google.maps.Marker({
        position: latLang,
        map: map,
        draggable: true,
        title: $('#id_title').val()
      });
      latitude.val(marker.getPosition().lat());
      longitude.val(marker.getPosition().lng());
      google.maps.event.addListener(marker, 'dragend', function(evt) {
        latitude.val(marker.getPosition().lat());
        longitude.val(marker.getPosition().lng());
      });
    });
  }
  

  $(document).on('change', '[data-required="true"]', function(evt) {
    var el = $(evt.target)
    if (el.val().trim() !== '') {
      addRemoveError(el);
    }
  });

  $(document).on('click', '#create-ad-btn', function(evt) {
    evt.preventDefault();
    var elems = $('[data-required="true"]');
    var errorOcr = false;
    for (var i=0; i < elems.length; i++) {
      var el = $(elems[i])
      if (el.val().trim() == '') {
        addRemoveError(el, true);
        errorOcr = true;
        break;
      }
      addRemoveError(el);
    }
    if (errorOcr) return
    if (latitude.val() == '' || longitude.val() == "") {
      $('#myModal').modal('show');
      return
    }

    $('#advertisement-new-form').submit();
    window.initMap = initMap;
  });
})
