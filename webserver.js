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

  function fileFilter (req, file, cb) {

    // The function should call `cb` with a boolean
    // to indicate if the file should be accepted
    if (path.extname(file.originalname) !== 'html')
      cb(null, true)
    else
      cb(new Error('Must be html file'))
  
  }
  
var upload = multer({ storage: storage , limits:{fileSize:100000}, fileFilter: fileFilter})
var app = express()


app.post('/upload', upload.single('timetable'), function (req, res, next) {
    var process = spawn('python', ["timetable.py", "\\tmp\\"+req.file.filename, "node"])
    process.stdout.on('data', (data) =>{
      if (data.toString() == 1)
      {
        res.download(path.join(__dirname, 'tmp', req.file.filename.slice(0, -5) + '.csv'), 'timetable.csv'); 
      } else {
        console.log(data.toString())
      }

    })

    process.stderr.on('data', (err) => {
      next(err)
    })

    
})

app.use(express.static('public'))

app.listen(port, ()=>{
      console.log("Server started at port " + port)
})