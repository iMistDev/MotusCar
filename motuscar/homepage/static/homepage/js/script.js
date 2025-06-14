document.addEventListener('DOMContentLoaded', () => {
    function toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('main-content');
        const sidebarIcon = document.getElementById('sidebar-icon');

        if (sidebar && mainContent && sidebarIcon) {
            sidebar.classList.toggle('hidden');
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('full');
            sidebarIcon.className = sidebar.classList.contains('hidden') ? 'fa-solid fa-bars' : 'fa-solid fa-xmark';
        } else {
            console.error('No se encontraron uno o más elementos: sidebar, main-content o sidebar-icon');
        }
    }

    function handleResize() {
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('main-content');
        const sidebarIcon = document.getElementById('sidebar-icon');

        if (sidebar && mainContent && sidebarIcon) {
            if (window.innerWidth > 768) {
                sidebar.classList.remove('hidden', 'active');
                mainContent.classList.remove('full');
                sidebarIcon.className = 'fa-solid fa-bars';
            } else {
                sidebar.classList.add('hidden');
                sidebar.classList.remove('active');
                mainContent.classList.add('full');
                sidebarIcon.className = 'fa-solid fa-bars';
            }
        } else {
            console.error('No se encontraron uno o más elementos en resize: sidebar, main-content o sidebar-icon');
        }
    }

    const sidebarBtn = document.querySelector('.sidebar-btn');
    if (sidebarBtn) {
        sidebarBtn.addEventListener('click', toggleSidebar);
    } else {
        console.error('No se encontró el botón .sidebar-btn');
    }

    window.addEventListener('resize', handleResize);
    handleResize();
});