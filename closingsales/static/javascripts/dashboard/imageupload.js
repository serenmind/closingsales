$(function () {
  'use strict';
  utils.isAdblockerActive(function(result) {
    if (result) {
      $("#adblocker-detect").css({'display': 'block'});
      toastr.warning('Ad Blocker detected. Please diasable ad blocker on this page.');
      $("#upload-btn").attr('disabled', 'disabled');
    }
  });
  var fileUpload = $("#fileupload");
  $(document).on('click', '.btn-danger', function(evt) {
    evt.preventDefault();
    var tr = $(evt.currentTarget).parents("tr");
    var id = tr.find("img").data("id");
    var yes = confirm("Are you sure you want to delete this image");
    if (!yes) return
    $.ajax({
      url: '/api/adimages/' + id + '/',
      method: 'DELETE',
      success: function(arg) {
        console.log("sucess");
        tr.remove();
        toastr.info('Image Deleted Sucessfully.')
      },
      error: function(err) {
        toastr.warning('Image Cannot be Deleted.')
      }
    });
  });

  var uploadedImagesContainer = $('#uploaded-images-container');
  $(".js-upload-photos").click(function () {
    fileUpload.click();
  });

  fileUpload.fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
      toastr.info('Image Uploaded sucessfully');
      setTimeout(function() {
        window.location = window.location.href;
      }, 500);

    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      if (data.result.is_valid) {
        uploadedImagesContainer.append(
          $("<tr>").append($("<td>").append($('<img>', {
            'data-id': data.id,
            'class': 'img-responsive pad',
            src: data.result.url
          })).append('<button class="btn btn-danger"><i class="fa fa-times-circle"></i></button>'))
        );
      }
    }

  });

});
