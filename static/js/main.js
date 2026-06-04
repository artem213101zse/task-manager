// Task Manager - Custom JavaScript (loaded from static files)

document.addEventListener('DOMContentLoaded', function() {
  // Mobile navigation toggle
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', function() {
      mobileMenu.classList.toggle('open');
      const isOpen = mobileMenu.classList.contains('open');
      menuBtn.setAttribute('aria-expanded', isOpen);
      menuBtn.innerHTML = isOpen 
        ? '<span class="text-xl">✕</span>' 
        : '<span class="text-xl">☰</span>';
    });

    // Close menu when clicking a link
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        menuBtn.innerHTML = '<span class="text-xl">☰</span>';
      });
    });
  }

  // Live search enhancement on task list (if search input exists)
  const searchInput = document.querySelector('input[name="q"]');
  const filterForm = document.querySelector('form[method="get"]');

  if (searchInput && filterForm) {
    let debounceTimer;
    searchInput.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        // Only auto-submit on desktop or after user stops typing
        if (window.innerWidth > 640) {
          filterForm.submit();
        }
      }, 450);
    });

    // Add a small hint on mobile
    if (window.innerWidth <= 640) {
      searchInput.placeholder = 'Поиск... (нажмите Применить)';
    }
  }

  // Confirm delete on task list page (progressive enhancement)
  document.querySelectorAll('a[href*="/delete/"]').forEach(deleteLink => {
    deleteLink.addEventListener('click', function(e) {
      const taskTitle = this.closest('.task-card')?.querySelector('h3')?.textContent?.trim() || 'эту задачу';
      if (!confirm(`Удалить задачу «${taskTitle}»? Это действие нельзя отменить.`)) {
        e.preventDefault();
      }
    });
  });

  // Optional: keyboard shortcut hint (press / to focus search)
  document.addEventListener('keydown', function(e) {
    if (e.key === '/' && document.activeElement.tagName === 'BODY') {
      if (searchInput) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
    }
  });

  // Small polish: add 'data-loaded' for potential future CSS animations
  document.documentElement.setAttribute('data-loaded', 'true');
});

// Expose a small helper if needed in future
window.TaskManager = {
  refreshFilters: () => {
    const form = document.querySelector('form[method="get"]');
    if (form) form.submit();
  }
};
