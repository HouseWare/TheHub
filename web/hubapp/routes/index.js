
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'HouseWare', door: 'asdf', light: 'asdf', temperature: 'asdf', battery: 'asdf', version: 'asdf' });
};
