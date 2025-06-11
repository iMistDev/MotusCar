from django import forms
from core.models.agenda import Agenda
from datetime import date, datetime, timedelta
from core.models.disponibilidad import DisponibilidadMecanico

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['hora_inicio']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            # horas disponibles en base a la disponibilidad del mec
            dia_semana = instance.fecha.weekday()
            disponibilidad = DisponibilidadMecanico.objects.filter(
                mecanico=instance.mecanico,
                dia_semana=dia_semana,
                disponible=True
            ).first()
            
            if disponibilidad:
                # genera opciones de hora en base a la disponibilidad
                horas_disponibles = []
                hora_actual = disponibilidad.hora_inicio
                while hora_actual < disponibilidad.hora_fin:
                    horas_disponibles.append(hora_actual.strftime('%H:%M'))
                    hora_actual = (datetime.combine(date.today(), hora_actual) + timedelta(minutes=30)).time()
                
                self.fields['hora_inicio'].widget = forms.Select(
                    choices=[(h, h) for h in horas_disponibles]
                )
    
    def clean(self):
        cleaned_data = super().clean()
        if 'hora_inicio' in cleaned_data and self.instance.servicio:
            # actualiza hora_fin basada en la duracion del servicio elegido
            # esto se usara para que las horas no se solapen (o se pisen) unas con otras
            nueva_hora_inicio = cleaned_data['hora_inicio']
            if isinstance(nueva_hora_inicio, str):
                nueva_hora_inicio = datetime.strptime(nueva_hora_inicio, '%H:%M').time()
            
            duracion = self.instance.servicio.duracion_estimada
            cleaned_data['hora_fin'] = (
                datetime.combine(date.today(), nueva_hora_inicio) + duracion
            ).time()
        
        return cleaned_data
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha.weekday() == 6:  # 6 = domingo
            raise forms.ValidationError("No se puede agendar citas los domingos")
        return fecha