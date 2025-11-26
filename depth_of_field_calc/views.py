from django.shortcuts import render
from django.http import JsonResponse
from .models import Sensor
import json
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    sensors = Sensor.objects.all()
    return render(request, "home.html", {'sensors': sensors})

@login_required
def calculate_dof(request):
    """
    Calculate depth of field using the formula:
    DOF = 2 * (f^2 * c * u * (u - f)) / (u^2 - f^2)
    where:
    - f = focal length (mm)
    - c = circle of confusion (mm)
    - u = subject distance (mm)
    
    Near distance = u - (u^2 * f * c) / (f^2 + u * f * c)
    Far distance = u + (u^2 * f * c) / (f^2 - u * f * c)
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            focal_length = float(data.get('focal_length'))
            aperture = float(data.get('aperture'))
            subject_distance = float(data.get('subject_distance')) * 1000  # Convert to mm
            sensor_id = int(data.get('sensor_id'))
            
            sensor = Sensor.objects.get(id=sensor_id)
            coc = sensor.coc
            
            # Effective focal length for aperture
            f_number = aperture
            
            # Using standard DOF formulas
            # Hyperfocal distance
            H = (focal_length ** 2) / (f_number * coc) + focal_length
            
            # Near distance
            near = (subject_distance * (H - focal_length)) / (H + subject_distance - 2 * focal_length)
            
            # Far distance
            if subject_distance < H:
                far = (subject_distance * (H - focal_length)) / (H - subject_distance)
            else:
                far = float('inf')
            
            # Total DOF
            dof = far - near if far != float('inf') else "∞"
            
            # Convert back to meters for display
            near_m = near / 1000
            far_m = far / 1000 if far != float('inf') else "∞"
            dof_m = dof / 1000 if dof != "∞" else "∞"
            
            return JsonResponse({
                'success': True,
                'near_distance': round(near_m, 3),
                'far_distance': round(far_m, 3) if isinstance(far_m, float) else far_m,
                'dof': round(dof_m, 3) if isinstance(dof_m, float) else dof_m,
                'sensor_name': sensor.name,
                'coc': coc
            })
        except (ValueError, Sensor.DoesNotExist) as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)