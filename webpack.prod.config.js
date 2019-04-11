const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

const config = require('./webpack.base.config.js');

config.mode = 'production';

config.output.path = require('path').resolve('./wanikani/static/dist');

config.plugins = config.plugins.concat([
  new BundleTracker({filename: './webpack-stats-prod.json'}),

  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
  }}),
]);

config.optimization = {
  minimizer: [
    // we specify a custom UglifyJsPlugin here to get source maps in production
    new UglifyJsPlugin({
      cache: true,
      parallel: true,
      uglifyOptions: {
        compress: false,
        ecma: 6,
        mangle: true
      },
      sourceMap: true
    })
  ]
};

module.exports = config;
