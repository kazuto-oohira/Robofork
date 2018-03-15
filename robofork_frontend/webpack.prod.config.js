const path = require('path')
const webpack = require('webpack')
const bundleTracker = require('webpack-bundle-tracker')

const config = require('./webpack.base.config.js')

config.output = {
  path: path.resolve(__dirname, '../robofork_app/static/robofork_app/js/'),
  publicPath: '/static/robofork_app/js/',
  filename: 'operation_plan_detail.js',
};

config.plugins = config.plugins.concat([
  new bundleTracker({filename: './webpack-stats-prod.json'}),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: '"production"',
    },
  }),
  new webpack.optimize.UglifyJsPlugin({
    sourceMap: false,
    compress: {
      warnings: false,
    },
  }),
  new webpack.LoaderOptionsPlugin({
    minimize: true,
  }),
]);

config.devtool = '#source-map';

module.exports = config;
