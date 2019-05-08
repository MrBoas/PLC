var express = require('express');
var axios = require('axios');
var fs = require('fs');
var path = require('path');
var router = express.Router();

/* GraphDB endpoint */
var endpoint = 'http://localhost:7200/repositories/projetoBeta'


/* GET Saved Querys list interface. */
router.get('/', function(req, res, next) {
  // res.send('Give a query name');
  var url = 'http://localhost:7200/rest/sparql/saved-queries'
  axios.get(url)
    .then(response => {
      console.log('PEDIDO: GraphDB Saved Querys')
      var html = '<h2>GraphDB Saved Querys</h2>'+'<ol>'
      for (i in response.data) {
        var name = response.data[i].name
        html = html.concat('<li><a href="http://localhost:4005/query/'+name+'">' + name + '</li></a>')
      }
      html = html+'</ol>'
      res.send(html)
    })
    .catch(err => console.log('ERROR returning Saved Querys list : ' + err))
});

/* GET any savedQuery. */
router.get('/:savedQuery', function(req, res, next) {
  var url = 'http://localhost:7200/rest/sparql/saved-queries?name='
  var encodedName = encodeURIComponent(req.params.savedQuery)
  // console.log(encodedName)
  axios.get(url+encodedName)
    .then(response => {
      var query = response.data.body
      var encoded = encodeURIComponent(query)
      console.log('PEDIDO: '+encodedName+' (Saved Query auto)')
      // console.log('Query: \n' + response.data.body)

      axios.get(endpoint + '?query=' + encoded, {
        headers: { Accept: 'application/sparql-results+json' }
      })
      .then(response => res.jsonp(response.data))
      .catch(err => console.log('ERRO: ' + err));
    })
    .catch(err => console.log('ERRO: ' + err))
});


/* GET getClasses. */
router.get('/others/getClasses', function(req, res, next) {
  var encoded = encodeURIComponent('select * where { ?s a owl:Class }')

  console.log('PEDIDO: getClasses')
  // console.log('Query: \n' + query);
  // console.log('Encoded: \n' + encoded);

  axios.get(endpoint + '?query=' + encoded, {
    headers: { Accept: 'application/sparql-results+json' }
  })
  .then(response => res.jsonp(response.data))
  .catch(err => console.log('ERRO: ' + err));
});

/* GET getNumClasses (Saved Query) */
router.get('/others/getNumClasses', function (req, res, next) {
  var url = 'http://localhost:7200/rest/sparql/saved-queries?name='
  var encodedName = encodeURIComponent('conta_classes')
  axios.get(url+encodedName)
    .then(response => {
      var query = response.data.body
      var encoded = encodeURIComponent(query)
      console.log('PEDIDO: getNumClasses (Saved Query)')
      // console.log('Query: \n' + response.data.body)

      axios.get(endpoint + '?query=' + encoded, {
        headers: { Accept: 'application/sparql-results+json' }
      })
      .then(response => res.jsonp(response.data))
      .catch(err => console.log('ERRO: ' + err));
    })
    .catch(err => console.log('ERRO: ' + err))
});



module.exports = router;