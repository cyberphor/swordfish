document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('sf-menu-toggle');
  const sidebar = document.getElementById('sf-sidebar');

  if (toggle && sidebar) {
    toggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });

    // Close sidebar when a nav link is clicked on mobile
    sidebar.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth <= 768) {
          sidebar.classList.remove('open');
        }
      });
    });
  }
});
