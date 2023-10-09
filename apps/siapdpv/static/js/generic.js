function mostrarNotificacion(icono, position, mensaje) {
    // icono :'success', 'error', 'warning', 'info'
    // 'top-end': muestra la notificación en la esquina superior derecha de la pantalla.
    // 'top-start': muestra la notificación en la esquina superior izquierda de la pantalla.
    // 'bottom-end': muestra la notificación en la esquina inferior derecha de la pantalla.
    // 'bottom-start': muestra la notificación en la esquina inferior izquierda de la pantalla.
    // 'center': muestra la notificación en el centro de la pantalla.
    const Toast = Swal.mixin({
        toast: true,
        position: position,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        onOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        },

    })

    Toast.fire({
        icon: icono,
        title: mensaje
    })
}


function enviarAjax(url, metodo, datos, success, error) {
    $.ajax({
        url: url,
        type: metodo,
        data: datos,
        dataType: 'json',
        success: success,
        error: error
    });
}

// Función para obtener el valor de una cookie por su nombre
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



