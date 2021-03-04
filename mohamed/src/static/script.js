var activeNavItem = $('.nav-item');
activeNavItem.click(function(){
  activeNavItem.removeClass('active');
  $(this).addClass('active');
});
$('v-pills-home-tab a[href="#profile"]').tab('show') // Select tab by name