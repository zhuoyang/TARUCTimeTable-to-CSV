var express = require('express')
var multer  = require('multer')
var spawn = require("child_process").spawn;
var path = require('path')
const port = 3000

var storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'tmp/')
    },
    filename: function (req, file, cb) {
      cb(null, file.fieldname + '-' + Date.now() + ".html")
    }
  })
  
var upload = multer({ storage: storage })
var app = express()


app.post('/upload', upload.single('timetable'), function (req, res, next) {
    console.log(req.file.filename)
    var process = spawn('python', ["timetable.py", "\\tmp\\"+req.file.filename])
    console.log("spawn success")
    process.stdout.on('data', (data) =>{
      if (data.toString() == 1)
      {
        res.download(path.join(__dirname, 'tmp', req.file.filename.slice(0, -5) + '.csv'), 'timetable.csv');
      }
    })

    
})

app.use(express.static('public'))

app.listen(port, ()=>{
      console.log("Server started at port " + port)
})