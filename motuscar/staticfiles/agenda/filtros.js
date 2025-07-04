document.addEventListener("DOMContentLoaded", function () {
    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('comuna');
    const especialidadSelect = document.getElementById('especialidad');
    const servicioSelect = document.getElementById('servicio');

    //FILTRO REGION-COMUNA
    regionSelect.addEventListener("change", function () {
        const selectedRegion = this.value;
        const comunas = COMUNAS_POR_REGION[selectedRegion] || [];   //mostrar solo comunas de la region selecc.
        
        comunaSelect.innerHTML = '<option value="">Cualquiera Comuna</option>';
        
        if (comunas.length > 0) {
            comunas.forEach(comuna => {
                const option = document.createElement("option");
                option.value = comuna;
                option.textContent = comuna;
                comunaSelect.appendChild(option);
            });
            comunaSelect.disabled = false;
        } else {
            comunaSelect.disabled = true;
        }
    });

    //FILTRO ESPECIALIDAD-SERVICIOS
    especialidadSelect.addEventListener("change", function () {
        const selectedEspecialidad = this.value;
        const servicios = SERVICIOS_POR_ESPECIALIDAD[selectedEspecialidad] || [];
        
        servicioSelect.innerHTML = '<option value="">Cualquiera Servicio</option>';
        
        if (servicios.length > 0) {
            servicios.forEach(servicio => {
                const option = document.createElement("option");
                option.value = servicio.id;
                option.textContent = servicio.nombre;
                servicioSelect.appendChild(option);
            });
            servicioSelect.disabled = false;
        } else {
            servicioSelect.disabled = true;
        }
    });

    if (regionSelect.value) {
        regionSelect.dispatchEvent(new Event('change'));
    }
    
    if (especialidadSelect.value) {
        especialidadSelect.dispatchEvent(new Event('change'));
    }
});