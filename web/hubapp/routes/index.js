
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'Home' });
};

exports.doors = function(req, res){
  res.render('doors', { title: 'Doors' });
};

exports.luminosity = function(req, res){
  res.render('luminosity', { title: 'Luminosity' });
};

exports.temperature = function(req, res){
  res.render('temperature', { title: 'Temperature' });
};

exports.lights = function(req, res){
  res.render('lights', { title: 'Lights' });
};
