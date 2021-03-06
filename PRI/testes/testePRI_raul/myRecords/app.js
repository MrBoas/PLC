var express = require('express');
var path = require('path');
var logger = require('morgan');
var createError = require('http-errors');
var cookieParser = require('cookie-parser');
var bodyParser = require("body-parser")
var mongoose = require("mongoose")

//---------------------------------------------------------------------------
// var tweet = require('./routes/tweet');
var api = require('./routes/api/records');
//---------------------------------------------------------------------------


var app = express();

// Base de Dados
mongoose.connect('mongodb://127.0.0.1:27017/myrecord', { useNewUrlParser: true })
  .then(() => console.log('Mongo ready: ' + mongoose.connection.readyState))
  .catch(() => console.log('Erro na conexão à BD.'))
//--------------------------------------------------------------------------------------


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())
// app.use(express.static(path.join(__dirname, 'public')));



// DEFINIR IST0////////////////////////////////////
// app.use('/', tweet);
app.use('/api',api)
////////////////////////////////////////////////


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
