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

