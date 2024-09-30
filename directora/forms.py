from django import forms
from .models import Empleado, Proyecto
import re
from django.contrib.auth.models import User
from .models import Empleado, PerfilUsuario
from django.contrib.auth.models import User, Group
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'departamento', 'fecha_contratacion', 'dpi']
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
        }

    # Validación para el nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre

    # Validación para el apellido
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
            raise forms.ValidationError("El apellido solo debe contener letras.")
        return apellido

    # Validación para el teléfono (solo números)
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r"^\d+$", telefono):
            raise forms.ValidationError("El teléfono solo debe contener números.")
        return telefono

    # Validación para el DPI (solo números)
    def clean_dpi(self):
        dpi = self.cleaned_data.get('dpi')
        if not re.match(r"^\d{13}$", dpi):
            raise forms.ValidationError("El DPI debe contener exactamente 13 números.")
        return dpi

    # Validación para el departamento (solo letras)
    def clean_departamento(self):
        departamento = self.cleaned_data.get('departamento')
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", departamento):
            raise forms.ValidationError("El departamento solo debe contener letras.")
        return departamento

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    # Validación para el nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre

    # Validación para la fecha de inicio
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if fecha_inicio and self.cleaned_data.get('fecha_fin'):
            if fecha_inicio > self.cleaned_data.get('fecha_fin'):
                raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
        return fecha_inicio

    # Validación para la fecha de fin
    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')
        if fecha_fin and self.cleaned_data.get('fecha_inicio'):
            if fecha_fin < self.cleaned_data.get('fecha_inicio'):
                raise forms.ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
        return fecha_fin

class UsuarioEmpleadoForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), empty_label="Seleccione Empleado")
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Seleccione Rol")
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)  # Agregar campo de correo electrónico

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Incluir email en los campos

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Asegurarse de asignar el correo electrónico
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['grupo'])  # Asignar el grupo al usuario
            perfil_usuario = PerfilUsuario(user=user, empleado=self.cleaned_data['empleado'])
            perfil_usuario.save()
        return user