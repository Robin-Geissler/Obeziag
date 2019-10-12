function setLogin(){
    let {PythonShell} = require('python-shell')
    var path = require('path')

    var user = document.getElementById("user").value
    var password = document.getElementById("password").value

    var options = {
        scriptPath : path.join(__dirname, '/../moodleCrawl/'),
        args : [user,password]
    }

    PythonShell.run('saveLoginData.py', options, function(err,result){
        if(err) throw err;
        console.log('result: %j', result)
    })

    // pychell.on('message', function(message){
    //     swal(message);
    // })
}