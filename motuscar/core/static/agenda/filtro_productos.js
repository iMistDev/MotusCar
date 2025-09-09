document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById('searchInput');
    const categoryButtons = document.querySelectorAll('.category-btn');
    const productos = document.querySelectorAll('.producto-item');

    // FILTRO POR BUSCADOR
    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            const searchText = this.value.toLowerCase();
            productos.forEach(item => {
                const title = item.querySelector('.card-title').textContent.toLowerCase();
                const description = item.querySelector('.card-text').textContent.toLowerCase();
                item.style.display = (title.includes(searchText) || description.includes(searchText)) ? 'block' : 'none';
            });
        });
    }

    // FILTRO POR CATEGORÍA
    if (categoryButtons) {
        categoryButtons.forEach(btn => {
            btn.addEventListener('click', function () {
                categoryButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const selectedCategory = this.dataset.category.toLowerCase();
                productos.forEach(item => {
                    if (selectedCategory === "all" || item.dataset.category === selectedCategory) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
});
