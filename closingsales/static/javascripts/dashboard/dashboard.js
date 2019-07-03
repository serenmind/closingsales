(function() {
  $(function() {
    $('#sidebar-dashboard-menu').tree();
    var path = document.location.pathname

    $("a[href$='"+ path +"']").parent('li').addClass('active');
  });
}());
