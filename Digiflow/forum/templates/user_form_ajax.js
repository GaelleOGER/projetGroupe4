$('#login').click(function(e) {
    console.log("bouton cliqué")
    e.preventDefault()
    $.ajax({
        url: '/api/token/',
        type: 'POST',
        dataType: 'json',
        data: {
            'username': $("input[name='username']").val(),
            'password': $("input[name='password']").val(),
        },
        success: function(e) {
            cons  fd.append('password', $("input[name='password']").val())ole.log('créations et acces au token')
            console.log(e)
            console.log(e.access)
            window.localStorage.setItem('access', e.access)
            window.localStorage.setItem('refresh', e.refresh)
            var fd = new FormData()
            fd.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value)
            fd.append('username', $("input[name='username']").val())

            $.ajax({
                    url: '/login/submit/',
                    type: 'POST',
                    contentType: false,
                    processData: false,
                    headers: {
                                Authorization: 'Bearer ' + window.localStorage.getItem('access'),
                            },
                    data: fd,
                    success: function(response) {
                        console.log('utilisateur authentifié')
                        console.log(response)
                        window.location.href = '/home/'

                        },
                    error: function(response) {
                        console.log('non authentifié')
                        console.log(response)
                        },
                    })
            },
        error: function(e) {
            console.log('non authentifié')
            },
    })
  });