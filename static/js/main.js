let currentUrl = window.location.pathname + window.location.search;

function loadContent(url, push = true) {
    if (url === currentUrl && push) return;
    $('#content').html(`
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="mt-2 text-muted">Cargando...</p>
        </div>
    `);
    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'html',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        success: function(data) {
            $('#content').html(data);
            if (push) {
                history.pushState({ url: url }, '', url);
                currentUrl = url;
            }
            initPageScripts();
        },
        error: function(xhr) {
            if (xhr.status === 403) {
                window.location.href = '/login/';
            } else {
                $('#content').html(`
                    <div class="alert alert-danger m-4">
                        <h4>Error al cargar la página</h4>
                        <p>${xhr.responseText || 'Intente nuevamente.'}</p>
                        <button onclick="loadContent('/agricola/productos/')" class="btn btn-primary">Volver al inicio</button>
                    </div>
                `);
            }
        }
    });
}

function submitForm(form, url) {
    const formData = new FormData(form);
    const submitBtn = $(form).find('button[type="submit"]');
    submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm"></span> Procesando...');
    $.ajax({
        url: url,
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        success: function(response) {
            if (response.redirect) {
                loadContent(response.redirect);
                showAlert('success', 'Operación exitosa.');
            } else if (typeof response === 'string') {
                $('#content').html(response);
            }
        },
        error: function(xhr) {
            submitBtn.prop('disabled', false).html(submitBtn.data('original-text') || 'Enviar');
            if (xhr.status === 400) {
                $('#content').html(xhr.responseText);
            } else {
                showAlert('danger', 'Error al procesar la solicitud.');
            }
        }
    });
    return false;
}

function showAlert(type, message) {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    const alertContainer = $('#content .alert-container');
    if (alertContainer.length) {
        alertContainer.html(alertHtml);
    } else {
        $('#content').prepend(`<div class="row"><div class="col-md-12">${alertHtml}</div></div>`);
    }
    setTimeout(() => $('.alert').alert('close'), 5000);
}

function initPageScripts() {
    $('form.ajax-form').off('submit').on('submit', function(e) {
        e.preventDefault();
        submitForm(this, this.action);
    });
    $('[data-bs-toggle="tooltip"]').each(function() {
        new bootstrap.Tooltip(this);
    });
    $('[data-bs-toggle="dropdown"]').each(function() {
        if (typeof bootstrap !== 'undefined' && !this._bs_dropdown) {
            this._bs_dropdown = new bootstrap.Dropdown(this);
        }
    });
}

$(document).ready(function() {
    initPageScripts();
    $(document).on('click', 'a.nav-link:not([data-bs-toggle]):not([data-no-spa]), a:not([data-bs-toggle]):not([data-no-spa])', function(e) {
        const href = $(this).attr('href');
        if (href && href.startsWith('/') && !href.startsWith('//') && !$(this).attr('target') && !$(this).hasClass('no-spa')) {
            e.preventDefault();
            loadContent(href);
        }
    });
});

window.addEventListener('popstate', function(e) {
    if (e.state && e.state.url) {
        loadContent(e.state.url, false);
    } else {
        loadContent(window.location.pathname, false);
    }
});
