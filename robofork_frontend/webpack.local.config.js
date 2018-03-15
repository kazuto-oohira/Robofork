const path = require('path')
const webpack = require('webpack')
const bundleTracker = require('webpack-bundle-tracker')

const config = require('./webpack.base.config.js')

config.output = {
  path: path.resolve(__dirname, '../robofork_app/static/robofork_app/js/'),
  publicPath: 'http://localhost:8001/static/robofork_app/js/',
  filename: 'operation_plan_detail.js',
};

config.plugins = config.plugins.concat([
  new bundleTracker({filename: './webpack-stats.json'}),
]);

config.devServer = {
  port: 8001,
  historyApiFallback: true,
  noInfo: true,
  overlay: true,
};

config.devtool = '#eval-source-map';

module.exports = config;
