const path = require('path');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const config = {
  context: __dirname,

  entry: {
    event_form: './events/static/js/event_form/index.js',
    signup: './events/static/js/signup/index.js'
  },

  output: {
    path: path.resolve('./ais_static/bundles/'),
    filename: "[name]-[hash].js",
  },

  watchOptions: {
    poll: 500,
    ignored: /node_modules/
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.js'}),
    new CleanWebpackPlugin([path.resolve('./ais_static/bundles/')])
  ],

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  }
};

module.exports = config;
