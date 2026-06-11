/**
 * Admin Panel – Base JavaScript
 * Sidebar toggle, alerts, global search, & utility functions
 */

document.addEventListener('DOMContentLoaded', function () {

    // ── Sidebar Toggle (mobile) ──
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const overlay = document.getElementById('sidebar-overlay');

    function openSidebar() {
        sidebar.classList.add('open');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (menuToggle) menuToggle.addEventListener('click', openSidebar);
    if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
    if (overlay) overlay.addEventListener('click', closeSidebar);


    // ── Auto-dismiss alerts ──
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(function () { alert.remove(); }, 300);
        }, 5000);
    });


    // ── Delete confirmation ──
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            var message = el.getAttribute('data-confirm') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });


    // ── Modal helpers ──
    window.openModal = function (id) {
        var modal = document.getElementById(id);
        if (modal) modal.classList.add('open');
    };

    window.closeModal = function (id) {
        var modal = document.getElementById(id);
        if (modal) modal.classList.remove('open');
    };

    // ── Open Edit Modal ──
    window.openEditModal = function (productId) {
        // Reset modal to loading state
        document.getElementById('product-modal-title').textContent = 'Edit Product';
        document.getElementById('btn-save-product').textContent    = 'Update Product';

        // Clear all fields first
        document.getElementById('product-form').reset();

        // Fetch product data from Django
        fetch('/admin_panel/products/' + productId + '/edit/')
            .then(function (res) {
                if (!res.ok) throw new Error('Failed to fetch product data');
                return res.json();
            })
            .then(function (data) {
                const img = document.getElementById('current-product-image');

                if (data.image_url) {
                    img.src = data.image_url;
                    img.style.display = 'block';
                } else {
                    img.style.display = 'none';
                }
                document.getElementById('prod-name').value      = data.name      || '';
                document.getElementById('prod-old-price').value = data.old_price || '';
                document.getElementById('prod-new-price').value = data.new_price || '';
                document.getElementById('prod-brand').value  = data.brand_id || '';
                document.getElementById('prod-badge').value     = data.badge     || '';
                document.getElementById('prod-desc').value      = data.description || '';

                // Checkboxes
                document.getElementById('prod-is-active').checked   = data.is_active;
                document.getElementById('prod-is-featured').checked = data.is_featured;

                // Point form action to edit URL
                document.getElementById('product-form').action =
                    '/admin_panel/products/' + productId + '/edit/';

                openModal('product-modal');
            })
            .catch(function (err) {
                console.error('Edit modal error:', err);
                alert('Could not load product data. Please try again.');
            });
    };

    // ── Open Add Modal (reset form to blank) ──
    document.getElementById('btn-add-product')?.addEventListener('click', function () {
        const img = document.getElementById('current-product-image');
        img.src = '';
        img.style.display = 'none';
        document.getElementById('product-modal-title').textContent = 'Add New Product';
        document.getElementById('btn-save-product').textContent    = 'Save Product';
        document.getElementById('product-form').reset();
        document.getElementById('product-form').action = '/admin_panel/products/add/';
        openModal('product-modal');
    });

    // Close modals on overlay click
    document.querySelectorAll('.modal-overlay').forEach(function (overlay) {
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) {
                overlay.classList.remove('open');
            }
        });
    });

    // Close modals on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.open').forEach(function (m) {
                m.classList.remove('open');
            });
            closeSidebar();
        }
    });

});