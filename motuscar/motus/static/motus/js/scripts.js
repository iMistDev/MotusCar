// SECCIÓN ANIMACIÓN (BORRAR SI NO UTILIZAR PERO BORRAR PRIMERO EN HTML)
window.addEventListener('load', function() {
    setTimeout(function() {
        document.querySelector('.loading-overlay').style.display = 'none';
    }, 2000);
});

// FIN SECCIÓN ANIMACIÓN

//Botón Hamburguesa
document.addEventListener('DOMContentLoaded', function() {
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const dropdownMenu = document.getElementById('dropdown-menu');
    
    if (hamburgerBtn && dropdownMenu) {
        hamburgerBtn.addEventListener('click', function() {
            dropdownMenu.classList.toggle('active');
            
            // Cambiar icono al abrir/cerrar
            const icon = this.querySelector('i');
            if (dropdownMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
        
        // Cerrar menú al hacer clic fuera de él
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.menu-hamburguesa')) {
                dropdownMenu.classList.remove('active');
                const icon = hamburgerBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
});