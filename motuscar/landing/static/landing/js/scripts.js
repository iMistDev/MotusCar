// Ocultar loader después de 2 segundos
window.addEventListener('load', function() {
    setTimeout(function() {
        document.querySelector('.loading-overlay').style.display = 'none';
    }, 2000);
});

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

// Carrusel del Hero
document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');
    
    if (slides.length > 0 && indicators.length > 0 && prevBtn && nextBtn) {
        let currentIndex = 0;
        let interval;
        
        function updateCarousel() {
            slides.forEach((slide, index) => {
                slide.classList.toggle('active', index === currentIndex);
            });
            
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentIndex);
            });
        }
        
        function nextSlide() {
            currentIndex = (currentIndex + 1) % slides.length;
            updateCarousel();
        }
        
        function prevSlide() {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            updateCarousel();
        }
        
        // Event listeners
        nextBtn.addEventListener('click', nextSlide);
        prevBtn.addEventListener('click', prevSlide);
        
        // Iniciar carrusel automático
        function startAutoSlide() {
            interval = setInterval(nextSlide, 5000);
        }
        
        function stopAutoSlide() {
            clearInterval(interval);
        }
        
        // Pausar al interactuar
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.addEventListener('mouseenter', stopAutoSlide);
            hero.addEventListener('mouseleave', startAutoSlide);
        }
        
        startAutoSlide();
        updateCarousel();
    }
});

// Mockpage IA
document.addEventListener('DOMContentLoaded', () => {
    const phrases = [
        '¿Te ayudo en algo?',
        '¿Estás buscando algo?',
        '¿Necesitas un Mecánico?',
        '¿En qué puedo asistirte?',
        '¡Estoy aquí para ayudarte!',
        '¿Tienes alguna duda?',
        '¿Te gustaría saber más sobre los servicios?',
        '¿Cómo puedo hacer tu día más fácil?',
        '¿Buscas algún repuesto?'
    ];

    const assistButtonContainer = document.querySelector('.assist-button-container');
    
    if (assistButtonContainer) {
        let tooltip = null;
        let scrollHandler = null;

        function getRandomPhrase() {
            return phrases[Math.floor(Math.random() * phrases.length)];
        }

        function adjustTooltipPosition() {
            if (!tooltip) return;
            
            const buttonRect = assistButtonContainer.getBoundingClientRect();
            const tooltipRect = tooltip.getBoundingClientRect();
            const margin = 20;

            let left = buttonRect.left + buttonRect.width / 2 - tooltipRect.width / 2;
            let top = buttonRect.top - tooltipRect.height - 10;

            // Ajustar si se desborda por la izquierda
            if (left < margin) left = margin;

            // Ajustar si se desborda por la derecha
            if (left + tooltipRect.width + margin > window.innerWidth) {
                left = window.innerWidth - tooltipRect.width - margin;
            }

            // Si no hay espacio arriba, mostrar debajo del botón
            if (top < margin) {
                top = buttonRect.bottom + 10;
            }

            tooltip.style.left = `${left}px`;
            tooltip.style.top = `${top}px`;
        }

        assistButtonContainer.addEventListener('mouseenter', () => {
            // Crear tooltip si no existe
            if (!tooltip) {
                tooltip = document.createElement('div');
                tooltip.classList.add('assist-tooltip');
                tooltip.textContent = getRandomPhrase();
                document.body.appendChild(tooltip);
                
                // Esperamos un frame para forzar el reflow
                requestAnimationFrame(() => {
                    adjustTooltipPosition();
                    tooltip.classList.add('fade-in');
                });
                
                // Añadir listener para scroll
                scrollHandler = () => adjustTooltipPosition();
                window.addEventListener('scroll', scrollHandler);
            }
        });

        assistButtonContainer.addEventListener('mouseleave', () => {
            if (tooltip) {
                tooltip.remove();
                tooltip = null;
                if (scrollHandler) {
                    window.removeEventListener('scroll', scrollHandler);
                }
                scrollHandler = null;
            }
        });
    }
});