const path = require('path');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin')
const BundleTracker = require('webpack-bundle-tracker');

const config = {
  context: __dirname,

  entry: {
    signup: './events/static/js/signup.js',
    event_form: './events/static/js/event_form.js'
  },

  output: {
    path: path.resolve('./ais_static/bundles/'),
    filename: "[name]-[hash].js",
  },

  watchOptions: {
    poll: 300,
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
