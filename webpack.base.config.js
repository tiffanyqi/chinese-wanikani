var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: './wanikani/static/js/index.jsx',

  output: {
    path: path.resolve('./wanikani/static/bundles/'),
    filename: '[name]-[hash].js',
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    rules: [{
      test: /\.jsx$/,
      exclude: /node_modules/,
      use: [{
        loader: 'babel-loader', // transform jsx into js
      }]
    }]
  },

  resolve: {
    modules: ['node_modules', 'bower_components'],
    extensions: ['*', '.js', '.jsx']
  },
}
